# Task 3: Deep-Dive Analysis & Customer Segmentation

This phase focuses on analyzing customer value patterns using **RFM (Recency, Frequency, Monetary) modeling** and building an interactive dashboard for decision-makers.

---

## 👥 Customer Segmentation Breakdown

We categorized **4,321 unique registered customers** into 7 distinct behavioral cohorts:

### 1. Cohort Performance Matrix

| Customer Segment | Customer Count | Base Share | Recency (Avg) | Frequency (Avg) | Monetary (Avg) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Loyal Customers** | 1,165 | 26.96% | 52.8 days | 5.3 orders | £1,911.39 |
| **Lost Customers** | 981 | 22.70% | 290.4 days | 1.1 orders | £231.25 |
| **About to Sleep** | 857 | 19.83% | 134.6 days | 1.2 orders | £339.81 |
| **Champions** | 804 | 18.61% | 15.0 days | 12.3 orders | £6,777.62 |
| **Recent/New Customers** | 205 | 4.74% | 23.4 days | 1.0 orders | £251.98 |
| **At Risk** | 175 | 4.05% | 258.9 days | 3.8 orders | £1,234.56 |
| **Promising Customers** | 134 | 3.10% | 45.2 days | 1.5 orders | £482.11 |

---

## 🚀 Live Interactive Dashboard

We built a full-scale web dashboard using **Streamlit** to allow stakeholders to interactively filter and query these results.

### Features Included:
- **KPI Summary Widgets**: Net Sales, Order Volume, AOV, and Active Customers.
- **Dynamic Filtering**: Sliders to specify country and customer segments.
- **Trend Charts**: Interactive line and bar charts showing hourly order densities and monthly sales.
- **Customer Lookup Database**: Search fields to lookup specific Customer transaction histories.

> [!TIP]
> **How to run the live dashboard:**
> 1. In your terminal, run: `streamlit run task3_dashboard/dashboard.py`
> 2. The app will launch in your browser at `http://localhost:8501`.