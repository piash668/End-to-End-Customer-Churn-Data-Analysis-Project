"""
===============================================================================
PROJECT: Customer Churn Data Cleaning & ETL Pipeline
AUTHOR: Piash Barua
DESCRIPTION:
    This script automates an end-to-end Data Cleansing, Feature Engineering,
    and ETL pipeline using Python (Pandas) and SQL Server.
    
    Workflow Steps:
    1. Load raw dirty Excel dataset
    2. Audit missing values and duplicate rows
    3. Remove dirty text placeholders and extra whitespaces
    4. Standardize text casing and categorical labels
    5. Cast data types & filter invalid numerical anomalies
    6. Impute missing values
    7. Perform Feature Engineering (Customer Value, Age/Tenure Buckets, Churn Flags)
    8. Validate clean data schema and distribution
    9. Export processed data to Excel & CSV formats
    10. Dynamic SQL Server Database Creation & Automated Table Ingestion
===============================================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

# =============================================================================
# STEP 1: INITIALIZE FILE PATHS & LOAD RAW DATASET
# =============================================================================
# Dynamically locate the raw data file relative to script location
file_path = Path(__file__).resolve().parent / "Churn_Unclean_Project.xlsx"

print("==================================================")
print("STEP 1: LOADING RAW DATASET")
print("==================================================")
print(f"Target File Path: {file_path}")

# Read Excel file and list available sheets
excel_file = pd.ExcelFile(file_path)
print(f"Detected Sheet Names: {excel_file.sheet_names}")

# Read the primary worksheet
sheet_name = excel_file.sheet_names[0]
df = pd.read_excel(file_path, sheet_name=sheet_name)

print(f"\nSuccessfully loaded sheet: '{sheet_name}'")
print(f"Initial Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Columns List: {list(df.columns)}")
print("\n--- Raw Data Preview (First 5 Rows) ---")
print(df.head())

# =============================================================================
# STEP 2: DATA AUDIT - MISSING VALUES & DUPLICATES DETECTIVE WORK
# =============================================================================
print("\n==================================================")
print("STEP 2: DATA QUALITY AUDIT")
print("==================================================")

# Count initial missing values across columns
print("Missing Values Count per Column:")
missing = df.isnull().sum()
print(missing[missing > 0].to_string() if missing.sum() > 0 else "No null values found initially.")

if (df.isnull().sum() == 0).all():
    print("\nNo missing values found in the dataset.")

# Check for duplicate records
print("\n--- Duplicate Audit ---")
duplicate_count = df.duplicated().sum()
print(f"Total Duplicate Records Identified: {duplicate_count}")

# Remove duplicate rows if detected
if duplicate_count > 0:
    print("\nDuplicate Rows Preview (First 10 duplicates):")
    print(df[df.duplicated(keep=False)].head(10).to_string(index=False))
    
    # Deduplicate in place
    df.drop_duplicates(inplace=True)
    print("\n[ACTION TAKEN] Duplicates successfully purged using df.drop_duplicates().")
else:
    print("No duplicate records found.")

print(f"Shape After Deduplication: {df.shape[0]} rows, {df.shape[1]} columns")

# =============================================================================
# STEP 3: TEXT CLEANING & STRING STANDARDIZATION
# =============================================================================
print("\n==================================================")
print("STEP 3: STRING SANITIZATION & STANDARDIZATION")
print("==================================================")

# 3.1 Replace common dirty string representations with true NumPy NaN values
dirty_placeholders = ["N/A", "NULL", "", " ", "nan", "NaN"]
df.replace(dirty_placeholders, np.nan, inplace=True)
print(f"[ACTION TAKEN] Replaced dirty string placeholders {dirty_placeholders} with np.nan.")

# 3.2 Strip leading/trailing spaces and collapse redundant internal whitespaces
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace(r"\s+", " ", regex=True)
print("[ACTION TAKEN] Stripped whitespaces and standardized string formatting across text columns.")

# 3.3 Apply Proper Title Casing to designated categorical/text columns
title_case_cols = ["Customer_Name", "State", "City", "Subscription_Type", "Contract_Type"]
for col in title_case_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.title()
print(f"[ACTION TAKEN] Applied Title Case formatting to columns: {title_case_cols}")

# 3.4 Standardize Churn indicator column values to uniform 'Yes' / 'No'
if "Churn" in df.columns:
    df["Churn"] = df["Churn"].str.strip().str.upper()
    df["Churn"] = df["Churn"].replace({"YES": "Yes", "NO": "No"})
    print("[ACTION TAKEN] Standardized 'Churn' column values to 'Yes'/'No'.")

# =============================================================================
# STEP 4: TYPE CASTING & DATA ANOMALY FILTERING
# =============================================================================
print("\n==================================================")
print("STEP 4: DATA TYPE CONVERSION & OUTLIER SANITIZATION")
print("==================================================")

# 4.1 Force numeric conversions for financial & demographic metrics
numeric_cols = ["Age", "Tenure_Months", "Monthly_Charges", "Total_Charges"]
for c in numeric_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
print(f"[ACTION TAKEN] Force converted columns to numeric dtypes: {numeric_cols}")

# 4.2 Outlier Filtering: Keep logical age limits (18 to 100 years old)
if "Age" in df.columns:
    initial_rows = len(df)
    df = df[(df["Age"] >= 18) & (df["Age"] <= 100)]
    print(f"[ACTION TAKEN] Filtered invalid Age values. Removed {initial_rows - len(df)} row(s).")

# 4.3 Anomaly Filtering: Remove negative financial charges
if "Monthly_Charges" in df.columns:
    df = df[df["Monthly_Charges"] >= 0]
if "Total_Charges" in df.columns:
    df = df[df["Total_Charges"] >= 0]
print("[ACTION TAKEN] Purged negative charge anomalies from Monthly_Charges and Total_Charges.")

# 4.4 Convert date column to standardized pandas datetime objects
if "Last_Interaction_Date" in df.columns:
    df["Last_Interaction_Date"] = pd.to_datetime(df["Last_Interaction_Date"], errors="coerce")
    print("[ACTION TAKEN] Converted 'Last_Interaction_Date' to datetime64 object.")

# =============================================================================
# STEP 5: IMPUTATION OF MISSING DATA
# =============================================================================
print("\n==================================================")
print("STEP 5: IMPUTING MISSING VALUES")
print("==================================================")

# Categorical missing value imputations
if "Tech_Support" in df.columns:
    df["Tech_Support"] = df["Tech_Support"].fillna("No")

if "Payment_Method" in df.columns:
    df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")

# Numerical missing value imputations using column mean strategy
if "Monthly_Charges" in df.columns:
    df["Monthly_Charges"] = df["Monthly_Charges"].fillna(df["Monthly_Charges"].mean())

if "Tenure_Months" in df.columns:
    df["Tenure_Months"] = df["Tenure_Months"].fillna(df["Tenure_Months"].mean())

if "Age" in df.columns:
    df["Age"] = df["Age"].fillna(df["Age"].mean())

print("[ACTION TAKEN] Categorical NaNs imputed with defaults ('No'/'Unknown').")
print("[ACTION TAKEN] Numerical NaNs imputed using Mean imputation strategy.")

# =============================================================================
# STEP 6: FEATURE ENGINEERING
# =============================================================================
print("\n==================================================")
print("STEP 6: FEATURE ENGINEERING & METRIC GENERATION")
print("==================================================")

# 6.1 Customer Lifetime Revenue Value & Monthly Revenue
if "Monthly_Charges" in df.columns and "Tenure_Months" in df.columns:
    df["Customer_Value"] = df["Monthly_Charges"] * df["Tenure_Months"]
    df["Monthly_Revenue"] = df["Monthly_Charges"]

# 6.2 Binned Tenure Groups (Segmentation for retention analysis)
if "Tenure_Months" in df.columns:
    df["Tenure_Group"] = pd.cut(
        df["Tenure_Months"],
        bins=[0, 12, 24, 48, 72],
        labels=["0-12", "13-24", "25-48", "49-72"]
    )

# 6.3 Demographic Senior Citizen Flag (Senior vs Adult)
if "Age" in df.columns:
    df["Senior_Flag"] = np.where(df["Age"] >= 60, "Senior", "Adult")

# 6.4 Binary Churn Indicator (Numeric flag for machine learning/aggregation)
if "Churn" in df.columns:
    df["Churn_Flag"] = df["Churn"].map({"Yes": 1, "No": 0})

print("Generated New Features:")
print(" - Customer_Value (Monthly_Charges * Tenure_Months)")
print(" - Monthly_Revenue")
print(" - Tenure_Group (0-12, 13-24, 25-48, 49-72 months)")
print(" - Senior_Flag (Senior >= 60, else Adult)")
print(" - Churn_Flag (1 = Yes, 0 = No)")

# =============================================================================
# STEP 7: FINAL DATASET VALIDATION & SCHEMA INSPECTION
# =============================================================================
print("\n==================================================")
print("STEP 7: FINAL DATA QUALITY ASSURANCE")
print("==================================================")

print("\n--- Dataset Info & Dtypes ---")
print(df.info())

print("\n--- Summary Statistics ---")
print(df.describe(include='all').T)

print("\n--- Final Null Values Check ---")
print(df.isnull().sum())

# =============================================================================
# STEP 8: EXPORT CLEANED DATASET TO LOCAL FILES
# =============================================================================
print("\n==================================================")
print("STEP 8: EXPORTING CLEAN DATASETS")
print("==================================================")

output_excel = Path(__file__).resolve().parent / "Clean_Churn_Data.xlsx"
output_csv = Path(__file__).resolve().parent / "Clean_Churn_Data.csv"

# Export cleaned data frames
df.to_excel(output_excel, index=False)
df.to_csv(output_csv, index=False)

print(f"[SUCCESS] Cleaned dataset saved to Excel: {output_excel}")
print(f"[SUCCESS] Cleaned dataset saved to CSV:   {output_csv}")

# =============================================================================
# STEP 9: AUTOMATED SQL SERVER INGESTION (ETL PIPELINE)
# =============================================================================
print("\n==================================================")
print("STEP 9: SQL SERVER DATABASE CREATION & DATA UPLOAD")
print("==================================================")

# SQL Server Instance Connection Details
server_name = r"DESKTOP-8LOAKQG\SQLEXPRESS"
database_name = "ChurnAnalysis_db"

try:
    # Connect to master database to check/create target database dynamically
    master_engine = create_engine(
        f"mssql+pyodbc://@{server_name}/master?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
    )

    # Execute DDL statement to create database if it doesn't exist
    with master_engine.begin() as conn:
        conn.execute(text(f"IF DB_ID('{database_name}') IS NULL CREATE DATABASE [{database_name}];"))
    print(f"[SUCCESS] Checked/Created SQL Server Database: '{database_name}'")

    # Connect to target application database
    db_engine = create_engine(
        f"mssql+pyodbc://@{server_name}/{database_name}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
    )

    # Load cleaned DataFrame into SQL Server table
    df.to_sql("Clean_Churn_Data", db_engine, if_exists="replace", index=False)
    
    print(f"\n[SUCCESS] Data successfully pushed to SQL Server!")
    print(f"Target Database: {database_name}")
    print(f"Target Table:    Clean_Churn_Data")

except Exception as e:
    print("\n[ERROR] SQL Server connection/upload failed.")
    print(f"Details: {e}")
    print("Troubleshooting: Ensure pyodbc & sqlalchemy are installed (pip install sqlalchemy pyodbc)")

print("\n==================================================")
print("ETL PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
print("==================================================")
