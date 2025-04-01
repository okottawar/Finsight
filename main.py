import streamlit as st
import pandas as pd
from modules.data_processing import upload_statement, parse_csv_to_df
from modules import insights, visualization, nlp_query
import sys
import os

# Add the parent directory to sys.path to correctly import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    st.title("📊 Finsight - Bank Statement Analyzer")
    st.write("Finsight is a powerful AI/ML tool that helps users analyze their bank statements to gain valuable financial insights by providing intuitive visualizations, transaction categorizations, and intelligent financial insights.")

    # Upload and Process Data Using the Data Processing Module
    uploaded_file = upload_statement()
    if not uploaded_file:
        st.warning("Please upload a bank statement CSV file.")
        return

    st.success("File uploaded successfully!")
    
    # Since this module is designed for CSV files, we assume the file type is CSV.
    df = parse_csv_to_df(uploaded_file)
    raw_text = "CSV data loaded."
    
    st.write("Extracted Data Preview:")
    st.text(raw_text)
    st.write("📝 Processed Transactions:", df.head())

    # Sidebar Menu for Insights
    st.sidebar.title("Select Insight")
    menu = st.sidebar.selectbox("Choose an option", [
        "Overall Spending vs. Income Analysis",
        "Category-wise Breakdown",
        "Recurring Transactions",
        "Top Transactions",
        "Anomaly Detection",
        "Natural Language Query",
        "Visualizations"
    ])

    if menu == "Overall Spending vs. Income Analysis":
        overall = insights.overall_spending_vs_income(df)
        st.subheader("Overall Spending vs. Income Analysis")
        st.write(overall)

    elif menu == "Category-wise Breakdown":
        cat_breakdown = insights.category_breakdown(df)
        st.subheader("Category-wise Breakdown")
        st.write("Spending by Category:", cat_breakdown["Spending"])
        st.write("Income by Category:", cat_breakdown["Income"])

    elif menu == "Recurring Transactions":
        recurring = insights.recurring_transactions(df)
        st.subheader("Recurring Transactions")
        st.write(recurring)

    elif menu == "Top Transactions":
        top_tx = insights.top_transactions(df)
        st.subheader("Top Transactions")
        st.write("Top Withdrawal:", top_tx["Top Withdrawal"])
        st.write("Top Deposit:", top_tx["Top Deposit"])

    elif menu == "Anomaly Detection":
        anomalies = insights.anomaly_detection(df)
        st.subheader("Anomalous Transactions")
        st.write(anomalies)

    elif menu == "Natural Language Query":
        st.subheader("Ask a Question")
        query = st.text_input("Enter your query about the statement:")
        if query:
            answer = nlp_query.handle_query(query, df)
            st.write("🔍 Answer:", answer)
            
    elif menu == "Visualizations":
        st.subheader("Spending Breakdown by Category")
        fig = visualization.create_spending_pie_chart(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Could not generate chart.")

        st.subheader("Balance Trend")
        fig = visualization.create_balance_trend(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Could not generate chart.")

        st.subheader("Transaction Volume")
        fig = visualization.create_transaction_volume_chart(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Could not generate chart.")

        st.subheader("Transaction Frequency")
        fig = visualization.create_transaction_frequency_chart(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Could not generate chart.")
        
        st.subheader("Transaction Remark Frequency")
        fig = visualization.create_remark_frequency_chart(df)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("Could not generate chart.")

if __name__ == "__main__":
    main()