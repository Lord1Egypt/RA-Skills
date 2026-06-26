#!/usr/bin/env python3
"""
Urlopnik — Main entry point
Użycie: python3 main.py "15 lipca 2026" "19 lipca 2026"
"""

from urlopnik import (
    parse_date, count_business_days, calculate_remaining_leave,
    format_date_pl, generate_leave_request, suggest_optimal_dates, LEAVE_TYPES
)
from datetime import datetime, timedelta
import sys

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    🏖️  URLOPNIK v1.0  🏖️                            ║
║         Inteligentny asystent urlopowy dla pracowników             ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Dane pracownika (domyślne - użytkownik je zmieni)
    employee = {
        'name': 'IMIĘ NAZWISKO',
        'position': 'STANOWISKO',
        'department': 'DZIAŁ',
        'location': 'MIASTO',
        'phone': 'TELEFON',
        'email': 'EMAIL@FIRMA.PL',
        'initials': 'XX',
        'total_leave': 26,
        'used_leave': 0,
    }
    
    if len(sys.argv) >= 3:
        start = parse_date(sys.argv[1])
        end = parse_date(sys.argv[2])
        leave_type_key = sys.argv[3] if len(sys.argv) > 3 else 'wypoczynkowy'
    else:
        print("📅 Wpisz daty urlopu:")
        start_str = input("   Od (np. 15 lipca 2026): ")
        end_str = input("   Do (np. 19 lipca 2026): ")
        start = parse_date(start_str)
        end = parse_date(end_str)
        leave_type_key = 'wypoczynkowy'
    
    if not start or not end:
        print("❌ Nieprawidłowy format daty!")
        print("   Użyj: python3 main.py '15 lipca 2026' '19 lipca 2026'")
        sys.exit(1)
    
    leave_type = LEAVE_TYPES.get(leave_type_key, LEAVE_TYPES['wypoczynkowy'])
    business_days = count_business_days(start, end)
    
    print(f"""
✅ URLOPIK - OBLICZENIA:

📅 Okres urlopu: {format_date_pl(start)} - {format_date_pl(end)}
📊 Dni robocze: {business_days}
🏷️  Rodzaj: {leave_type['name']}

""")
    
    # Generuj wniosek
    request = generate_leave_request(employee, start, end, leave_type)
    print(request)
    
    print("\n💡 NAJBLIŻSZE OPTYMALNE DATY:")
    for s in suggest_optimal_dates():
        print(f"   {s}")

if __name__ == "__main__":
    main()