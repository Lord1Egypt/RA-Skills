#!/usr/bin/env python3
"""Calculate true home affordability."""
import json
import os
import argparse

REALESTATE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/realestate")

def ensure_dir():
    os.makedirs(REALESTATE_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Calculate home affordability')
    parser.add_argument('--income', type=float, required=True, help='Annual gross income')
    parser.add_argument('--debts', type=float, default=0, help='Monthly debt payments')
    parser.add_argument('--downpayment', type=float, required=True, help='Down payment amount')
    
    args = parser.parse_args()
    
    monthly_income = args.income / 12
    
    # Standard 28/36 rule
    max_housing = monthly_income * 0.28
    max_total_debt = monthly_income * 0.36
    max_mortgage = max_total_debt - args.debts
    
    # Use more conservative
    affordable_payment = min(max_housing, max_mortgage)
    
    # Estimate home price (rough: $150/month per $25K at 7%)
    loan_amount = (affordable_payment / 150) * 25000
    home_price = loan_amount + args.downpayment
    
    # Add true cost estimates
    property_tax = home_price * 0.012 / 12  # ~1.2% annually
    insurance = 150  # estimated monthly
    maintenance = home_price * 0.01 / 12  # 1% annually for maintenance
    
    true_monthly = affordable_payment + property_tax + insurance + maintenance
    
    print("\n🏠 TRUE AFFORDABILITY CALCULATION")
    print("=" * 60)
    print(f"Annual Income: ${args.income:,.2f}")
    print(f"Monthly Income: ${monthly_income:,.2f}")
    print(f"Monthly Debts: ${args.debts:,.2f}")
    print(f"Down Payment: ${args.downpayment:,.2f}")
    print()
    print("BASE MORTGAGE:")
    print(f"  Max Monthly Payment: ${affordable_payment:,.2f}")
    print(f"  Estimated Home Price: ${home_price:,.0f}")
    print()
    print("TRUE MONTHLY COSTS:")
    print(f"  Mortgage Payment: ${affordable_payment:,.2f}")
    print(f"  Property Tax: ${property_tax:,.2f}")
    print(f"  Insurance: ${insurance:,.2f}")
    print(f"  Maintenance Reserve: ${maintenance:,.2f}")
    print(f"  TOTAL: ${true_monthly:,.2f}")
    print()
    print(f"This is {true_monthly/monthly_income*100:.1f}% of your monthly income")
    print()
    print("⚠️  This is an estimate. Actual costs depend on:")
    print("   - Interest rates and credit score")
    print("   - Property taxes in your specific area")
    print("   - HOA fees (if applicable)")
    print("   - Utility costs")
    print("   - Your specific financial situation")

if __name__ == '__main__':
    main()
