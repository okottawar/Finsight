import streamlit as st
import pandas as pd

def upload_statement():
    """
    Displays a file uploader widget for CSV files and returns the uploaded file.
    """
    return st.file_uploader("Upload your bank statement CSV file", type=["csv"])

def parse_csv_to_df(uploaded_file):
    """
    Parses a CSV file into a structured DataFrame.
    Expected CSV columns:
      "Sr. No.", "Value date", "Transaction Date", "Cheque Number",
      "Transacting Remarks", "Withdrawal Amount", "Deposit Amount", "Balance".
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Convert date columns to datetime objects (assumes MM/DD/YYYY format)
    df["Value_date"] = pd.to_datetime(df["Value date"], format="%m/%d/%Y", errors='coerce')
    df["Transaction_date"] = pd.to_datetime(df["Transaction Date"], format="%m/%d/%Y", errors='coerce')
    
    # Clean numeric columns: remove commas and convert to float
    df["Withdrawal"] = df["Withdrawal Amount"].astype(str).str.replace(",", "").astype(float)
    df["Deposit"] = df["Deposit Amount"].astype(str).str.replace(",", "").astype(float)
    df["Balance"] = df["Balance"].astype(str).str.replace(",", "").astype(float)
    
    # Create a 'Category' column based on the Transacting Remarks
    df["Category"] = df["Transacting Remarks"].apply(categorize_transaction)
    df["Remarks"] = df["Transacting Remarks"]  # Add a consistent column for Remarks
    
    # Create a consistent Sr_No column
    df["Sr_No"] = df["Sr. No."]
    
    return df

def categorize_transaction(remarks):
    """
    Categorizes transactions based on keywords in the transacting remarks.
    Adjust keywords and categories as needed.
    """
    categories = {
        "food": ["restaurant", "cafe", "coffee", "dining"],
        "transport": ["uber", "taxi", "fuel", "metro"],
        "essentials": ["grocery", "supermarket"],
        "utilities": ["electricity", "water", "internet"],
        "salary": ["salary", "bonus", "freelance"],
        "health": ["medical", "hospital", "clinic"],
        "entertainment": ["movie", "concert", "entertainment"]
    }
    
    remarks_lower = remarks.lower() if isinstance(remarks, str) else ""
    for category, keywords in categories.items():
        if any(keyword in remarks_lower for keyword in keywords):
            return category
    return "other"