# End-to-End-Customer-Churn-Data-Analysis-Project
End-to-end Customer Churn Data Analysis pipeline utilizing Python (Pandas) for ETL &amp; feature engineering, MySQL for querying, and Power BI for interactive dashboard visualization.
---
<img width="893" height="501" alt="PBI Screenshot" src="https://github.com/user-attachments/assets/a906e5d3-11fe-4818-bbc8-18a3b8125c20" />

## 🛠️ Tech Stack & Tools

* **Programming Language:** Python
* **Data Manipulation & ETL:** Pandas, NumPy
* **Database & SQL:** MySQL, SQLAlchemy
* **Data Visualization:** Power BI Desktop
* **Data Sources:** Raw Excel (`Churn_Unclean_Project.xlsx`)

---

## 🔄 Project Architecture & Workflow

[Raw Dirty Excel Data]
│
▼
[Python ETL Pipeline] ──► (Data Cleaning, Handling Missing Values & Feature Engineering)
│
▼
[Cleaned CSV / MySQL] ──► (Relational Data Storage & SQL Analytics)[cite: 2]
│
▼
[Power BI Dashboard]  ──► (DAX Measures, KPI Cards, & Interactive Visuals)   
---

## 🧹 Data Preprocessing & Feature Engineering (Python)

Using **Pandas** and **NumPy**, the raw data underwent extensive data wrangling[cite: 2]:

1. **Handling Missing & Invalid Values:**
   * Removed duplicate records and trimmed leading/trailing whitespace[cite: 2].
   * Standardized placeholder missing values (`N/A`, `NULL`, blank spaces) to `NaN`[cite: 2].
   * Replaced null values in numeric columns (`Age`, `Monthly_Charges`, `Tenure_Months`) with column means[cite: 2].
   * Filtered out invalid records (e.g., negative charges or out-of-range age values)[cite: 2].

2. **Categorical Standardization:**
   * Converted names, states, cities, and subscription fields into Title Case[cite: 2].
   * Unified binary fields (`YES`/`NO` variations mapped to standardized `Yes`/`No`)[cite: 2].

3. **Feature Engineering:**
   * **`Customer_Value`**: Calculated as `Monthly_Charges * Tenure_Months`[cite: 2].
   * **`Tenure_Group`**: Binned customer tenure into distinct buckets (`0-12`, `13-24`, `25-48`, `49-72` months)[cite: 2].
   * **`Senior_Flag`**: Categorized customers as `Senior` ($\ge$ 60 years) or `Adult`[cite: 2].
   * **`Churn_Flag`**: Numeric binary indicator (`1` for `Yes`, `0` for `No`) for modeling and aggregated calculations[cite: 2].

---

## 🗄️ Database Management & SQL Queries

The clean dataset was exported directly to **MySQL** using `SQLAlchemy` for structured querying[cite: 2]:

Key analytical queries included[cite: 2]:
* **Churn Metrics:** Calculating total customer count, total churned customers, and overall churn rate %[cite: 2].
* **Financial Aggregations:** Average monthly charges, revenue per state, and top high-value customers[cite: 2].
* **Behavioral Segmentation:** Customer distribution and churn breakdown across contract types, subscription tiers, internet services, and payment methods[cite: 2].

---

## 📉 Power BI Dashboard & Visual Insights

An interactive **Churn Data Analysis Dashboard** was constructed in Power BI using custom DAX measures[cite: 1, 2].

### 📌 Core KPIs (Key Metrics):
* **Total Customers:** 445[cite: 1]
* **Churned Customers:** 105[cite: 1]
* **Retained Customers:** 340[cite: 1]
* **Overall Churn Rate:** 24% (0.24)[cite: 1]
* **Total Revenue:** $22.16M[cite: 1]
* **Average Tenure:** 35.95 Months[cite: 1]
* **Average Monthly Charges:** $1.36K[cite: 1]

### 💡 Key Findings:
* **Contract Types:** Customers with **Two-Year** contracts showed the highest churn volume (38), followed by One-Year (34) and Month-To-Month (32)[cite: 1].
* **Subscription Tiers:** **Standard** (42) and **Premium** (40) tiers accounted for significantly higher churn than the Basic tier (23)[cite: 1].
* **Internet Services:** Cable (29.5%) and 5G/DSL (26.67% each) were the primary internet connection types among churned users[cite: 1].
* **Payment Methods:** **UPI** (26.67%) and **Credit Card** (23.81%) accounted for the majority of churned payments[cite: 1].

---
## 📂 Project Structure

```text
├── data/
│   ├── Churn_Unclean_Project.xlsx    # Raw dirty dataset[cite: 2]
│   └── Clean_Churn_Data.csv          # Processed clean dataset[cite: 2]
├── scripts/
│   ├── data_cleaning.py              # Python ETL & Data Preprocessing Script[cite: 2]
│   └── sql_analysis.sql              # MySQL practice queries and data extraction[cite: 2]
├── dashboard/
│   ├── Churn_Dashboard.pbix          # Power BI Dashboard File[cite: 1, 2]
│   └── dashboard_preview.png         # Screenshot of the Power BI dashboard[cite: 1]
└── README.md                         # Project documentation

🚀 How to Run This Project
Clone the Repository:

Bash
git clone [https://github.com/your-username/customer-churn-analysis.git](https://github.com/your-username/customer-churn-analysis.git)
cd customer-churn-analysis
Run Data Cleaning Script:

Bash
pip install pandas numpy sqlalchemy pymysql openpyxl
python scripts/data_cleaning.py
Database Setup:

Load Clean_Churn_Data.csv or run the database export code in Python to populate your MySQL database[cite: 2].

Run queries from scripts/sql_analysis.sql[cite: 2].

View Power BI Dashboard:

Open dashboard/Churn_Dashboard.pbix in Power BI Desktop to explore the interactive visual analytics[cite: 1, 2].




