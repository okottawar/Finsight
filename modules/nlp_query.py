def handle_query(query, df):
    """Processes user queries and returns relevant insights."""
    query = query.lower()

    if "total withdrawn" in query or "total spent" in query:
        total_withdrawn = df["Withdrawal"].sum()
        return f"Total money withdrawn: {total_withdrawn}"
    
    if "total deposited" in query or "total received" in query:
        total_deposited = df["Deposit"].sum()
        return f"Total money deposited: {total_deposited}"

    if "largest withdrawal" in query:
        largest = df.nlargest(1, "Withdrawal")
        return f"Largest withdrawal transaction: {largest.to_dict(orient='records')}"
    
    if "largest deposit" in query:
        largest = df.nlargest(1, "Deposit")
        return f"Largest deposit transaction: {largest.to_dict(orient='records')}"
        
    if "balance" in query:
        current_balance = df["Balance"].iloc[-1] if not df.empty else "No balance information available"
        return f"Current balance: {current_balance}"
    
    if "category" in query and "spent" in query:
        # Extract the category from the query
        categories = df["Category"].unique()
        category = None
        for cat in categories:
            if cat.lower() in query:
                category = cat
                break
        
        if category:
            category_spent = df[df["Category"] == category]["Withdrawal"].sum()
            return f"Total spent on {category}: {category_spent}"
        else:
            return "Please specify a valid category."

    return "I couldn't understand the query. Try rephrasing or ask about total spent, total deposited, largest transactions, or balance."