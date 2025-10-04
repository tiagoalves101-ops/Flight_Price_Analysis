#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flight_price_analysis.py
Reads 'flight_price.xlsx' from the same folder, runs a quick EDA, and saves plots and a CSV summary
to the same folder. Axes show prices with the ₹ symbol.
"""

from pathlib import Path
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ----------------------------
# Config
# ----------------------------
HERE = Path(__file__).resolve().parent
INPUT_XLSX = HERE / "flight_price.xlsx"   # expects the file in the same folder as this script
OUT_SUMMARY_CSV = HERE / "flight_price_summary.csv"
PLOTS = {
    "price_distribution": HERE / "plot_price_distribution.png",
    "avg_price_by_airline": HERE / "plot_avg_price_by_airline.png",
    "price_vs_duration": HERE / "plot_price_vs_duration.png",
    "price_by_stops": HERE / "plot_price_by_stops.png",
}

# Currency formatter for ₹
rupee_fmt = FuncFormatter(lambda x, _: f"₹{int(x):,}")

# ----------------------------
# Helpers
# ----------------------------
def parse_duration_to_minutes(s: str) -> float:
    """
    Convert strings like '2h 50m', '5h', '45m' to minutes (float).
    Returns NaN if unparsable.
    """
    if not isinstance(s, str):
        return np.nan
    h = m = 0
    h_match = re.search(r"(\d+)\s*h", s)
    m_match = re.search(r"(\d+)\s*m", s)
    if h_match:
        h = int(h_match.group(1))
    if m_match:
        m = int(m_match.group(1))
    if h == 0 and m == 0:
        return np.nan
    return h * 60 + m

def stops_to_int(s: str) -> float:
    """
    Map 'non-stop' -> 0, '1 stop' -> 1, '2 stops' -> 2, else NaN.
    """
    if not isinstance(s, str):
        return np.nan
    if s.strip().lower() == "non-stop":
        return 0
    m = re.search(r"(\d+)\s*stop", s.lower())
    return float(m.group(1)) if m else np.nan

# ----------------------------
# Load
# ----------------------------
if not INPUT_XLSX.exists():
    raise FileNotFoundError(f"File not found: {INPUT_XLSX.name} in {HERE}")

df = pd.read_excel(INPUT_XLSX)

# ----------------------------
# Clean & enrich
# ----------------------------
# Date
if "Date_of_Journey" in df.columns:
    # Many datasets use day-first; safe parse with dayfirst=True
    df["Date"] = pd.to_datetime(df["Date_of_Journey"], dayfirst=True, errors="coerce")
else:
    df["Date"] = pd.NaT

# Duration
if "Duration" in df.columns:
    df["Duration_min"] = df["Duration"].apply(parse_duration_to_minutes)
else:
    df["Duration_min"] = np.nan

# Stops
if "Total_Stops" in df.columns:
    df["Stops"] = df["Total_Stops"].apply(stops_to_int)
else:
    df["Stops"] = np.nan

# Price
if "Price" not in df.columns:
    raise KeyError("Column 'Price' not found in the Excel file.")
df = df[pd.to_numeric(df["Price"], errors="coerce").notna()].copy()
df["Price"] = df["Price"].astype(float)

# Basic columns for grouping
airline_col = "Airline" if "Airline" in df.columns else None

# ----------------------------
# Quick EDA summary
# ----------------------------
summary = {
    "rows": len(df),
    "price_min": float(np.nanmin(df["Price"])) if len(df) else np.nan,
    "price_mean": float(np.nanmean(df["Price"])) if len(df) else np.nan,
    "price_median": float(np.nanmedian(df["Price"])) if len(df) else np.nan,
    "price_max": float(np.nanmax(df["Price"])) if len(df) else np.nan,
    "price_std": float(np.nanstd(df["Price"])) if len(df) else np.nan,
    "nulls_total": int(df.isna().sum().sum()),
    "duration_min_mean": float(np.nanmean(df["Duration_min"])) if "Duration_min" in df else np.nan,
}
pd.Series(summary).to_frame("value").to_csv(OUT_SUMMARY_CSV)

# ----------------------------
# Plots
# ----------------------------
plt.rcParams.update({"figure.dpi": 120, "axes.grid": True, "axes.spines.top": False, "axes.spines.right": False})

# 1) Price distribution
fig1 = plt.figure()
ax1 = fig1.gca()
ax1.hist(df["Price"].dropna(), bins=30)
ax1.set_title("Price Distribution")
ax1.set_xlabel("Price (₹)")
ax1.set_ylabel("Count")
ax1.xaxis.set_major_formatter(rupee_fmt)
fig1.tight_layout()
fig1.savefig(PLOTS["price_distribution"])
plt.close(fig1)

# 2) Average price by airline
if airline_col and df[airline_col].notna().any():
    avg_air = df.groupby(airline_col)["Price"].mean().sort_values(ascending=False)
    fig2 = plt.figure()
    ax2 = fig2.gca()
    avg_air.plot(kind="bar", ax=ax2)
    ax2.set_title("Average Price by Airline")
    ax2.set_xlabel("Airline")
    ax2.set_ylabel("Average Price (₹)")
    ax2.yaxis.set_major_formatter(rupee_fmt)
    fig2.tight_layout()
    fig2.savefig(PLOTS["avg_price_by_airline"])
    plt.close(fig2)

# 3) Price vs duration (scatter)
if df["Duration_min"].notna().any():
    fig3 = plt.figure()
    ax3 = fig3.gca()
    ax3.scatter(df["Duration_min"], df["Price"], s=12, alpha=0.7)
    ax3.set_title("Price vs Duration (minutes)")
    ax3.set_xlabel("Duration (min)")
    ax3.set_ylabel("Price (₹)")
    ax3.yaxis.set_major_formatter(rupee_fmt)
    fig3.tight_layout()
    fig3.savefig(PLOTS["price_vs_duration"])
    plt.close(fig3)

# 4) Price by number of stops (boxplot)
if df["Stops"].notna().any():
    order = sorted(df["Stops"].dropna().unique())
    fig4 = plt.figure()
    ax4 = fig4.gca()
    data_by_stops = [df.loc[df["Stops"] == k, "Price"].dropna().values for k in order]
    ax4.boxplot(data_by_stops, labels=[str(int(k)) for k in order], showfliers=False)
    ax4.set_title("Price by Number of Stops")
    ax4.set_xlabel("Stops")
    ax4.set_ylabel("Price (₹)")
    ax4.yaxis.set_major_formatter(rupee_fmt)
    fig4.tight_layout()
    fig4.savefig(PLOTS["price_by_stops"])
    plt.close(fig4)

print(f"Done.\nSaved summary -> {OUT_SUMMARY_CSV.name}\nSaved plots ->")
for k, p in PLOTS.items():
    if p.exists():
        print(" -", p.name)
