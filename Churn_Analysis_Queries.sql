-- =============================================================================
-- PROJECT: Customer Churn & Revenue Analytics (SQL Practice Suite)
-- TARGET DATABASE: ChurnAnalysis_db
-- TARGET TABLE: Clean_Churn_Data
-- AUTHOR: Piash Barua
-- DESCRIPTION:
--     This script contains 15 analytical SQL queries covering core KPIs,
--     customer segmentation, churn distribution, revenue metrics, and 
--     high-value account identification.
-- =============================================================================

USE ChurnAnalysis_db;
GO

-- =============================================================================
-- SECTION 1: CORE EXECUTIVE KPIS
-- =============================================================================

-- Query 1: Total Customer Count
SELECT 
    COUNT(Customer_ID) AS Total_Customers
FROM Clean_Churn_Data;

-- Query 2: Total Churn Volume
SELECT 
    SUM(Churn_Flag) AS Total_Churned_Customers
FROM Clean_Churn_Data;

-- Query 3: Overall Churn Rate (%)
SELECT 
    ROUND(CAST(SUM(Churn_Flag) AS FLOAT) / COUNT(Customer_ID) * 100, 2) AS Churn_Rate_Pct
FROM Clean_Churn_Data;

-- Query 4: Portfolio Average Monthly Charges
SELECT 
    ROUND(AVG(Monthly_Charges), 2) AS Avg_Monthly_Charges
FROM Clean_Churn_Data;

-- Query 5: Portfolio Average Customer Tenure
SELECT 
    ROUND(AVG(Tenure_Months), 1) AS Avg_Tenure_Months
FROM Clean_Churn_Data;


-- =============================================================================
-- SECTION 2: CHURN SEGMENTATION ANALYSIS
-- =============================================================================

-- Query 6: Churn Metrics by Contract Type
SELECT 
    Contract_Type,
    COUNT(Customer_ID) AS Total_Customers,
    SUM(Churn_Flag) AS Churn_Count,
    ROUND(CAST(SUM(Churn_Flag) AS FLOAT) / COUNT(Customer_ID) * 100, 2) AS Churn_Rate_Pct
FROM Clean_Churn_Data
GROUP BY Contract_Type
ORDER BY Churn_Rate_Pct DESC;

-- Query 7: Churn Metrics by Internet Service Provider Format
SELECT 
    Internet_Service,
    COUNT(Customer_ID) AS Total_Customers,
    SUM(Churn_Flag) AS Churn_Count,
    ROUND(CAST(SUM(Churn_Flag) AS FLOAT) / COUNT(Customer_ID) * 100, 2) AS Churn_Rate_Pct
FROM Clean_Churn_Data
GROUP BY Internet_Service
ORDER BY Churn_Rate_Pct DESC;

-- Query 8: Geographic Churn Distribution by State
SELECT 
    State,
    COUNT(Customer_ID) AS Total_Customers,
    SUM(Churn_Flag) AS Churn_Count,
    ROUND(CAST(SUM(Churn_Flag) AS FLOAT) / COUNT(Customer_ID) * 100, 2) AS Churn_Rate_Pct
FROM Clean_Churn_Data
GROUP BY State
ORDER BY Churn_Count DESC;

-- Query 9: Customer Share by Payment Method
SELECT 
    Payment_Method,
    COUNT(Customer_ID) AS Customer_Count,
    ROUND(CAST(COUNT(Customer_ID) AS FLOAT) / (SELECT COUNT(*) FROM Clean_Churn_Data) * 100, 2) AS Customer_Pct
FROM Clean_Churn_Data
GROUP BY Payment_Method
ORDER BY Customer_Count DESC;

-- Query 10: Customer Count & Revenue by Subscription Plan Type
SELECT 
    Subscription_Type,
    COUNT(Customer_ID) AS Customer_Count,
    ROUND(SUM(Customer_Value), 2) AS Total_Revenue
FROM Clean_Churn_Data
GROUP BY Subscription_Type
ORDER BY Customer_Count DESC;


-- =============================================================================
-- SECTION 3: REVENUE & FINANCIAL METRICS
-- =============================================================================

-- Query 11: Top Geographic Markets Ranked by Lifetime Revenue
SELECT 
    State,
    COUNT(Customer_ID) AS Total_Customers,
    ROUND(SUM(Customer_Value), 2) AS Total_Revenue,
    ROUND(AVG(Customer_Value), 2) AS Avg_Revenue_Per_Customer
FROM Clean_Churn_Data
GROUP BY State
ORDER BY Total_Revenue DESC;

-- Query 12: Average Spending Comparison Across Contract Formats
SELECT 
    Contract_Type,
    ROUND(AVG(Monthly_Charges), 2) AS Avg_Monthly_Charges,
    ROUND(AVG(Total_Charges), 2) AS Avg_Total_Charges
FROM Clean_Churn_Data
GROUP BY Contract_Type
ORDER BY Avg_Monthly_Charges DESC;


-- =============================================================================
-- SECTION 4: RISK & SERVICE SUPPORT ANALYSIS
-- =============================================================================

-- Query 13: Demographics Churn Comparison (Senior Citizens vs Adults)
SELECT 
    Senior_Flag,
    COUNT(Customer_ID) AS Total_Customers,
    SUM(Churn_Flag) AS Churn_Count,
    ROUND(CAST(SUM(Churn_Flag) AS FLOAT) / COUNT(Customer_ID) * 100, 2) AS Churn_Rate_Pct
FROM Clean_Churn_Data
GROUP BY Senior_Flag
ORDER BY Churn_Rate_Pct DESC;

-- Query 14: Top 10 Highest Lifetime Value Accounts
SELECT TOP 10
    Customer_ID,
    Customer_Name,
    State,
    Contract_Type,
    Tenure_Months,
    Monthly_Charges,
    Customer_Value
FROM Clean_Churn_Data
ORDER BY Customer_Value DESC;

-- Query 15: Churn Impact Analysis for Accounts Without Technical Support
SELECT 
    Tech_Support,
    COUNT(Customer_ID) AS Customer_Count,
    SUM(Churn_Flag) AS Churn_Count,
    ROUND(CAST(SUM(Churn_Flag) AS FLOAT) / COUNT(Customer_ID) * 100, 2) AS Churn_Rate_Pct
FROM Clean_Churn_Data
WHERE Tech_Support = 'No'
GROUP BY Tech_Support;