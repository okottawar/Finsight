import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def create_spending_pie_chart(df):
    """
    Generates a pie chart of spending categories using 'Transacting Remarks' as a substitute for Category.
    It filters rows where 'Withdrawal Amount' is positive.
    """
    # Check required columns
    if "Transacting Remarks" not in df.columns or "Withdrawal Amount" not in df.columns or df.empty:
        return None
    try:
        spending_df = df[df["Withdrawal Amount"] > 0]
        if spending_df.empty:
            return None
        # Group by 'Transacting Remarks' as a proxy for spending category
        category_data = spending_df.groupby("Transacting Remarks")["Withdrawal Amount"].sum()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(category_data, labels=category_data.index, autopct='%1.1f%%', startangle=140)
        ax.set_title("Spending Breakdown by Transaction Remarks")
        plt.tight_layout()
        return fig
    except Exception as e:
        print(f"Error in pie chart: {e}")
        return None

def create_balance_trend(df):
    """
    Line chart showing monthly balance trend over time using 'Transaction Date' and 'Balance'.
    The balance for each month is taken as the last available balance of that month.
    """
    if "Balance" not in df.columns or "Transaction Date" not in df.columns:
        return None
    try:
        df = df.copy()
        # Convert and clean date data
        df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
        df = df.dropna(subset=["Transaction Date", "Balance"])
        df = df.sort_values("Transaction Date")
        
        # Create monthly aggregates
        monthly_df = (
            df.set_index("Transaction Date")
            .resample('M')['Balance']
            .last()  # Take last balance of the month
            .reset_index()
        )
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(monthly_df["Transaction Date"], 
                monthly_df["Balance"], 
                marker='o', 
                linestyle='-', 
                color='blue',
                markersize=8)
        
        # Formatting
        ax.set_title("Monthly Balance Trend", fontsize=14)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Balance", fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Format dates on x-axis
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    except Exception as e:
        print(f"Balance trend error: {e}")
        return None

def create_transaction_volume_chart(df):
    """
    Line chart showing weekly transaction volume using 'Transaction Date'.
    The count for each week is computed by resampling the transactions.
    """
    if "Transaction Date" not in df.columns:
        return None
    try:
        df = df.copy()
        df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], errors="coerce")
        df = df.dropna(subset=["Transaction Date"])
        df = df.sort_values("Transaction Date")
        # Set 'Transaction Date' as index for resampling
        df.set_index("Transaction Date", inplace=True)
        weekly_counts = df.resample('W').size().reset_index(name="Count")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(weekly_counts["Transaction Date"], weekly_counts["Count"], marker='o', linestyle='-')
        ax.set_title("Weekly Transaction Volume")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Transactions")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    except Exception as e:
        print(f"Transaction volume error: {e}")
        return None

def create_transaction_frequency_chart(df):
    """
    Bar chart showing transaction frequency by hour of day using 'Transaction Date'.
    """
    if "Transaction Date" not in df.columns:
        return None
    try:
        df = df.copy()
        df["Hour"] = pd.to_datetime(df["Transaction Date"], errors="coerce").dt.hour
        df = df.dropna(subset=["Hour"])
        hourly_counts = df["Hour"].value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(hourly_counts.index, hourly_counts.values, color='teal')
        ax.set_title("Transaction Frequency by Hour of Day")
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Number of Transactions")
        ax.set_xticks(range(0, 24))
        plt.tight_layout()
        return fig
    except Exception as e:
        print(f"Frequency chart error: {e}")
        return None

def create_remark_frequency_chart(df):
    """
    Bar chart displaying the top 10 transaction remarks using 'Transacting Remarks'.
    """
    if "Transacting Remarks" not in df.columns:
        return None
    try:
        # Clean remarks and filter empty values
        remarks = df["Transacting Remarks"].astype(str).str.strip().replace(["", "nan", "None"], pd.NA)
        top_remarks = remarks.value_counts().head(10)
        
        if top_remarks.empty:
            return None
            
        fig, ax = plt.subplots(figsize=(10, 6))
        top_remarks.plot(kind='barh', ax=ax, color='purple')
        ax.set_title("Top 10 Transaction Remarks")
        ax.set_xlabel("Count")
        ax.set_ylabel("Remarks")
        plt.tight_layout()
        return fig
    except Exception as e:
        print(f"Remark frequency error: {e}")
        return None
