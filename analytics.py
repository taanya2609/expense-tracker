import pandas as pd
from datetime import datetime
from io import StringIO

def calculate_health(total, budget):
    try:
        if not budget or budget <= 0: return 0
        score = max(0, 100 - (float(total) / float(budget) * 100))
        return int(score)
    except:
        return 0

def get_ai_insights(expenses, budget):
    if not expenses: return "Welcome! Add your first expense to start AI tracking.", 0
    df = pd.DataFrame([{'amt': e.amount, 'date': e.date} for e in expenses])
    total = df['amt'].sum()
    days = (datetime.now() - df['date'].min()).days + 1
    daily_avg = total / days
    projected = daily_avg * 30
    
    if total > budget:
        return f"🚨 Critical: Budget exceeded by ₹{round(total-budget, 2)}!", projected
    if projected > budget:
        return f"⚠️ Warning: High spending. Projected ₹{round(projected, 2)}", projected
    return f"✅ Healthy: You are on track to save ₹{round(budget-projected, 2)}", projected

def generate_csv(expenses):
    output = StringIO()
    df = pd.DataFrame([{'Date': e.date, 'Title': e.title, 'Category': e.category, 'Amount': e.amount} for e in expenses])
    df.to_csv(output, index=False)
    return output.getvalue()