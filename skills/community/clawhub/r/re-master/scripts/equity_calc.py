import sys
import json

def calculate_equity(participants, months_elapsed=0):
    """
    Calculate proportional ownership based on total contributed equity.
    
    participants = {
        'inv1': {'dp': 132149, 'monthly': 17000},
        'inv2': {'dp': 240000, 'monthly': 12000},
        ...
    }
    """
    totals = {}
    grand_total = 0
    
    for name, data in participants.items():
        contrib = data.get('dp', 0) + (data.get('monthly', 0) * months_elapsed)
        totals[name] = contrib
        grand_total += contrib
        
    if grand_total == 0:
        return {name: 0 for name in participants}
        
    return {name: (val / grand_total) * 100 for name, val in totals.items()}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = json.loads(sys.argv[1])
        months = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        print(json.dumps(calculate_equity(data, months), indent=2))
    else:
        print("Usage: python3 equity_calc.py <json_participants> [months_elapsed]")
