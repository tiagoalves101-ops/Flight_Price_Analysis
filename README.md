
# ✈️ Flight Price Analysis

This project analyzes **flight price data** using Python.  
It performs a quick **Exploratory Data Analysis (EDA)** and generates insightful visualizations — all saved automatically in the same folder.

---

## 🧠 Features
- Reads `flight_price.xlsx` automatically  
- Cleans and prepares data  
- Converts duration and stops to numeric form  
- Displays prices with the **₹ (Indian Rupee)** symbol  
- Exports a CSV summary and multiple plots  

---

## 📊 Generated Plots

| Plot | Description | Preview |
|------|--------------|----------|
| **Price Distribution** | Frequency of flight prices | ![Price Distribution](plot_price_distribution.png) |
| **Average Price by Airline** | Mean price per airline | ![Average Price by Airline](plot_avg_price_by_airline.png) |
| **Price vs Duration** | Relationship between price and trip duration | ![Price vs Duration](plot_price_vs_duration.png) |
| **Price by Stops** | Price variation by number of stops | ![Price by Stops](plot_price_by_stops.png) |

---

## 📊 Statistical summary

| Metric                         | Value      |
| ------------------------------ | ---------- |
| **Minimum Price**              | ₹1,759.00  |
| **Maximum Price**              | ₹79,512.00 |
| **Average Price**              | ₹9,087.06  |
| **Median Price**               | ₹8,372.00  |
| **Price Standard Deviation**   | ₹4,611.14  |
| **Average Duration (minutes)** | 643.09     |

---

## ⚙️ How to Run
```bash
python flight_price_analysis.py
Make sure the file flight_price.xlsx is in the same folder.

📂 Outputs
flight_price_summary.csv

.png plot images with ₹ axis labels

🧰 Tech Stack
Python · Pandas · NumPy · Matplotlib
