# Shipment Analysis Dashboard

## 📊 Project Overview
This project analyzes shipment data to identify delays and optimize costs.

## 🧹 Data Cleaning
- Removed duplicates
- Handled missing values
- Converted date columns
- Created new features:
  - Shipping Days
  - Cost per KG
  - Delay Indicator

## 📈 Insights
- Delay rate ≈ 21%
- بعض المدن فيها تأخير عالي
- بعض routes مكلفة جدًا

## 🤖 Machine Learning
- تم استخدام Random Forest للتنبؤ بالتأخير

## 🚀 Dashboard Features
- KPIs (Total, Delay %, Cost)
- Filters (Status, Destination)
- Charts (Trend, Distribution)
- Delay Analysis
- Cost Optimization

## 🌐 Live Demo
[PUT YOUR LINK HERE]

# 🚚 Shipment Performance Dashboard

## 📌 Overview
This project analyzes shipment data to track performance, detect delays, and optimize costs.  
It includes an interactive dashboard and a machine learning model to predict shipment delays.

---

## 📊 Features
- KPIs (Total Shipments, Avg Shipping Days, Delay %, Total Cost)
- Interactive Filters (Status, Destination)
- Visualizations (Bar, Pie, Line Charts)
- Delay Analysis
- Cost Optimization Insights
- 🌍 Shipments Map
- 🤖 Delay Prediction Model
- 🧠 User Input Prediction (Real-time)

---

## 🤖 Machine Learning
- Model: Random Forest Classifier
- Target: `Is_Delayed`
- Accuracy: ~77%
- Note: Removed `Status` column to avoid data leakage

---

## 🛠️ Tech Stack
- Python
- Pandas
- Plotly
- Streamlit
- Scikit-learn

---

## ▶️ How to Run
```bash
pip install -r requirements.txt
streamlit run app.py