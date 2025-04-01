import pandas as pd
import numpy as np
from scipy import stats

def overall_spending_vs_income(df, start_date=None, end_date=None):
    """
    Calculates overall spending vs. income.
    Optionally filters the data between start_date and end_date.
    Returns a dictionary with total spent, total received, and net balance.
    """
    df_filtered = df.copy()
    if start_date:
        df_filtered = df_filtered[df_filtered["Transaction_date"] >= start_date]
    if end_date:
        df_filtered = df_filtered[df_filtered["Transaction_date"] <= end_date]
    
    total_spent = df_filtered["Withdrawal"].sum()
    total_received = df_filtered["Deposit"].sum()
    net_balance = total_received - total_spent
    return {"Total Spent": total_spent, "Total Received": total_received, "Net Balance": net_balance}

def category_breakdown(df):
    """
    Groups transactions by Category.
    Returns a dictionary with spending (withdrawals) and income (deposits) per category.
    """
    spending = df.groupby("Category")["Withdrawal"].sum().abs()
    income = df.groupby("Category")["Deposit"].sum()
    return {"Spending": spending.to_dict(), "Income": income.to_dict()}

def recurring_transactions(df, threshold=2):
    """
    Identifies recurring transactions based on the 'Remarks' column.
    Only includes transactions where the same remark appears at least 'threshold' times.
    Returns a dictionary summarizing frequency, total withdrawals, and deposits per recurring remark.
    """
    recurring = df.groupby("Remarks").filter(lambda x: len(x) >= threshold)
    recurring_summary = recurring.groupby("Remarks").agg({
        "Withdrawal": "sum", 
        "Deposit": "sum", 
        "Sr_No": "count"
    }).rename(columns={"Sr_No": "Frequency"})
    return recurring_summary.to_dict(orient="index")

def top_transactions(df, top_n=1):
    """
    Finds the largest transactions.
    Returns the top withdrawal(s) and top deposit(s) as dictionaries.
    """
    top_withdrawal = df.nlargest(top_n, "Withdrawal")
    top_deposit = df.nlargest(top_n, "Deposit")
    return {
        "Top Withdrawal": top_withdrawal.to_dict(orient="records"),
        "Top Deposit": top_deposit.to_dict(orient="records")
    }

def anomaly_detection(df, z_thresh=3):
    """
    Detects anomalies using the Z-score method.
    Flags transactions with a Z-score above the specified threshold.
    Returns a list of anomalous transactions.
    """
    # Compute Z-scores (ignoring zeros and filling missing values)
    withdrawal_vals = df["Withdrawal"].replace(0, np.nan).fillna(0)
    deposit_vals = df["Deposit"].replace(0, np.nan).fillna(0)
    
    df['Withdrawal_z'] = np.abs(stats.zscore(withdrawal_vals))
    df['Deposit_z'] = np.abs(stats.zscore(deposit_vals))
    
    anomalies = df[(df['Withdrawal_z'] > z_thresh) | (df['Deposit_z'] > z_thresh)]
    return anomalies.to_dict(orient="records")

