#!/usr/bin/env python3
"""
Urlopnik — Inteligentny asystent urlopowy
Wersja: 1.0.0
Autor: Tomasz Pędzierski / ClawLabs

Użycie:
    python3 urlopnik.py "15 lipca 2025" "19 lipca 2025" "wypoczynkowy"
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Polski kalendarz świąt (2025-2026)
HOLIDAYS = [
    # 2025
    "2025-01-01", "2025-01-06", "2025-04-20", "2025-04-21", "2025-05-01",
    "2025-05-03", "2025-05-30", "2025-06-19", "2025-08-15", "2025-11-01",
    "2025-11-11", "2025-12-25", "2025-12-26",
    # 2026
    "2026-01-01", "2026-01-06", "2026-04-05", "2026-04-06", "2026-05-01",
    "2026-05-03", "2026-05-21", "2026-06-04", "2026-08-15", "2026-11-01",
    "2026-11-11", "2026-12-25", "2026-12-26",
]

HOLIDAYS = [datetime.strptime(d, "%Y-%m-%d").date() for d in HOLIDAYS]

# Polskie nazwy miesięcy
MONTHS_PL = {
    'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4,
    'maja': 5, 'czerwca': 6, 'lipca': 7, 'sierpnia': 8,
    'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12
}

# Rodzaje urlopów
LEAVE_TYPES = {
    'wypoczynkowy': {'name': 'urlop wypoczynkowy', 'days': 20, 'color': '🟢'},
    'na żądanie': {'name': 'urlop na żądanie', 'days': 4, 'color': '🟡'},
    'macierzyński': {'name': 'urlop macierzyński', 'days': 0, 'color': '🩷'},
    'ojcowski': {'name': 'urlop ojcowski', 'days': 2, 'color': '🔵'},
    'taternicki': {'name': 'urlop wypoczynkowy', 'days': 20, 'color': '🟢'},
}

def parse_date(date_str):
    """Parsuje polską datę tekstową."""
    date_str = date_str.lower().strip()
    
    # Spróbuj bezpośredniego formatu
    for fmt in ["%d %m %Y", "%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y"]:
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            pass
    
    # Parsuj "15 lipca 2025" lub "15 lipca"
    parts = date_str.split()
    if len(parts) >= 2:
        day = int(parts[0])
        month_name = parts[1].rstrip('.,')
        year = int(parts[2]) if len(parts) > 2 else datetime.now().year
        
        if month_name in MONTHS_PL:
            month = MONTHS_PL[month_name]
            try:
                return datetime(year, month, day).date()
            except:
                return None
    
    return None

def count_business_days(start_date, end_date):
    """Liczy dni robocze między datami (bez weekendów i świąt)."""
    days = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5 and current not in HOLIDAYS:
            days += 1
        current += timedelta(days=1)
    return days

def calculate_remaining_leave(used_days, total_days=26):
    """Oblicza pozostały urlop."""
    remaining = total_days - used_days
    return max(0, remaining)

def format_date_pl(date):
    """Formatuje datę po polsku: 15 lipca 2025."""
    months = {
        1: 'stycznia', 2: 'lutego', 3: 'marca', 4: 'kwietnia',
        5: 'maja', 6: 'czerwca', 7: 'lipca', 8: 'sierpnia',
        9: 'września', 10: 'października', 11: 'listopada', 12: 'grudnia'
    }
    return f"{date.day} {months[date.month]} {date.year}"

def generate_leave_request(employee_data, start_date, end_date, leave_type):
    """Generuje wniosek urlopowy."""
    
    business_days = count_business_days(start_date, end_date)
    
    # Format dat
    start_str = format_date_pl(start_date)
    end_str = format_date_pl(end_date)
    today = format_date_pl(datetime.now().date())
    
    # Wygeneruj wniosek w formacie Markdown
    request = f"""
╔══════════════════════════════════════════════════════════════════════╗
║                      WNIOSEK O URLOP WYPOCZYNKOWY                    ║
╚══════════════════════════════════════════════════════════════════════╝

Data sporządzenia: {today}
Numer wniosku: WR/{datetime.now().strftime('%Y%m%d')}/{employee_data.get('initials', 'XX')}

═══════════════════════════════════════════════════════════════════════
                              DANE PRACOWNIKA
═══════════════════════════════════════════════════════════════════════

Imię i nazwisko:    {employee_data.get('name', 'Jan Kowalski')}
Stanowisko:         {employee_data.get('position', 'Specjalista')}
Dział:              {employee_data.get('department', 'Sprzedaż')}
Lokalizacja:        {employee_data.get('location', 'Zamość')}
Tel. kontaktowy:     {employee_data.get('phone', '500 123 456')}
E-mail:             {employee_data.get('email', 'jan.kowalski@firma.pl')}

═══════════════════════════════════════════════════════════════════════
                            INFORMACJE O URLOPIE
═══════════════════════════════════════════════════════════════════════

Rodzaj urlopu:         {leave_type.get('name', 'urlop wypoczynkowy')}
Okres urlopu:          od {start_str}
                       do {end_str}
Liczba dni kalendarzowych: {(end_date - start_date).days + 1}
Liczba dni roboczych:  {business_days}

═══════════════════════════════════════════════════════════════════════
                            DO WYPEŁNIENIA
═══════════════════════════════════════════════════════════════════════

Data od delegacji / spotkania: ................................
Środek transportu:           ☐ samochód  ☐ pociąg  ☐ autobus
Adres w czasie urlopu:       .........................................
                                   (kod)     miasto
Tel. w czasie urlopu:        ...............................

Uzasadnienie (opcjonalnie):
..................................................................


╔══════════════════════════════════════════════════════════════════════╗
║                         PODPISY I AKCEPTACJA                          ║
╚══════════════════════════════════════════════════════════════════════╝

Pracownik: ................   Data: .................

Bezpośredni przełożony: ...............   Data: ................

Dział HR / Kasa: ................   Data: ................

═══════════════════════════════════════════════════════════════════════
        ✅ Wypełnij powyższy wniosek i wyślij do przełożonego
        📧 Możesz też wysłać mailem jako załącznik PDF
═══════════════════════════════════════════════════════════════════════

Wygenerowano przez Urlopnik v1.0 | ClawLabs / Infinity Tech
"""
    return request

def suggest_optimal_dates(year=datetime.now().year):
    """Sugeruje optymalne daty urlopowe (przedłużone weekendy)."""
    suggestions = []
    
    # Sprawdź długie weekendy
    special_dates = [
        (1, 6, "Nowy Rok"),
        (1, 7, "Święto Constitution"),
        (5, 1, "Święto Pracy"),
        (5, 3, "Święto Konstytucji 3 Maja"),
        (8, 15, "Wniebowzięcie NMP"),
        (11, 1, "Wszystkich Świętych"),
        (11, 11, "Narodowe Święto Niepodległości"),
        (12, 25, "Boże Narodzenie"),
        (12, 26, "Drugi dzień Bożego Narodzenia"),
    ]
    
    for month, day, name in special_dates:
        try:
            date = datetime(year, month, day).date()
            if date.weekday() == 0:  # Poniedziałek
                suggestions.append(f"🎉 {name} - weź 2 dni urlopu (pt+pon) = 4 dni wolnego!")
            elif date.weekday() == 4:  # Piątek
                suggestions.append(f"🎉 {name} - weź poniedziałek = 4 dni wolnego!")
        except:
            pass
    
    return suggestions

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    🏖️  URLOPNIK v1.0  🏖️                            ║
║         Inteligentny asystent urlopowy dla pracowników             ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # Dane pracownika (demo)
    employee = {
        'name': 'Jan Kowalski',
        'position': 'Specjalista ds. Sprzedaży',
        'department': 'Dział Handlowy',
        'location': 'Zamość',
        'phone': '500 123 456',
        'email': 'jan.kowalski@firm.pl',
        'initials': 'JK',
        'total_leave': 26,
        'used_leave': 10,
    }
    
    remaining = calculate_remaining_leave(employee['used_leave'], employee['total_leave'])
    
    print(f"📋 Dane pracownika: {employee['name']}")
    print(f"   Stanowisko: {employee['position']}")
    print(f"   Limit urlopu: {employee['total_leave']} dni")
    print(f"   Wykorzystano: {employee['used_leave']} dni")
    print(f"   Pozostało: {remaining} dni")
    print()
    
    if len(sys.argv) >= 3:
        # Parse dates from command line
        start = parse_date(sys.argv[1])
        end = parse_date(sys.argv[2])
        
        if not start or not end:
            print("❌ Nieprawidłowy format daty. Użyj: python3 urlopnik.py '15 lipca 2025' '19 lipca 2025'")
            sys.exit(1)
        
        leave_type_key = sys.argv[3] if len(sys.argv) > 3 else 'wypoczynkowy'
        leave_type = LEAVE_TYPES.get(leave_type_key, LEAVE_TYPES['wypoczynkowy'])
        
        # Oblicz dni robocze
        business_days = count_business_days(start, end)
        
        print(f"✅ Urlop od {format_date_pl(start)} do {format_date_pl(end)}")
        print(f"   Dni robocze: {business_days}")
        print(f"   Pozostało po urlopie: {remaining - business_days} dni")
        print()
        
        # Generuj wniosek
        request = generate_leave_request(employee, start, end, leave_type)
        print(request)
        
        # Sugestie
        print("\n💡 SUGESTIE OPTYMALNYCH DAT:")
        for s in suggest_optimal_dates():
            print(f"   {s}")
        
    else:
        print("📅 Przykładowe wywołanie:")
        print("   python3 urlopnik.py '15 lipca 2025' '19 lipca 2025'")
        print()
        
        print("💡 SUGESTIE NA NAJBLIŻSZE DNI WOLNE:")
        for s in suggest_optimal_dates():
            print(f"   {s}")
        
        print("\n" + "="*60)
        print("🎄 BOŻE NARODZENIE 2026:")
        print("   Weź od poniedziałku 22.12 do środy 24.12 = 6 dni wolnego!")
        print()
        
        # Przykładowy wniosek
        example_start = datetime(2026, 7, 15).date()
        example_end = datetime(2026, 7, 19).date()
        request = generate_leave_request(employee, example_start, example_end, LEAVE_TYPES['wypoczynkowy'])
        print("📝 PRZYKŁADOWY WNIOSEK URLOPOWY:")
        print(request)

if __name__ == "__main__":
    main()