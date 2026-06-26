#!/usr/bin/env python3
"""
UmowaGenerator — Generator Umów Prawnych
Wersja: 1.0.0
Autor: Tomasz Pędzierski / Infinity Tech

Użycie:
    python3 umowa_generator.py --type=zlecenie
    python3 umowa_generator.py --type=dzielo
    python3 umowa_generator.py --type=najmu
    python3 umowa_generator.py --demo
"""

import sys
from datetime import datetime, timedelta

def generate_contract(
    contract_type,
    employer_name, employer_address, employer_nip=None, employer_pesel=None,
    employee_name=None, employee_address=None, employee_nip=None, employee_pesel=None,
    subject=None, remuneration=None, currency='PLN', start_date=None, end_date=None,
    lieu_of_work=False, notice_period=None, deposit=None, property_address=None,
    tenant_name=None, tenant_address=None, tenant_pesel=None,
    landlord_name=None, landlord_address=None,
    car_brand=None, car_model=None, car_year=None, car_vin=None, car_price=None,
    apartment_address=None, apartment_rooms=None, apartment_area=None,
    apartment_floor=None, apartment_rent=None, advance_date=None,
    buyer_name=None, buyer_address=None, buyer_nip=None,
    seller_name=None, seller_address=None, seller_nip=None,
    property_description=None, deposit_amount=None, handover_date=None,
    additional_terms=None, notes=None
):
    """Generuje umowę wybranego typu."""
    
    contract_type = contract_type.lower().replace('-', '').replace(' ', '')
    
    if contract_type in ['zlecenie', 'zlecen']:
        return generate_contract_zlecenie(
            employer_name, employer_address, employer_nip, employer_pesel,
            employee_name, employee_address, employee_nip, employee_pesel,
            subject, remuneration, currency, start_date, end_date, notice_period, additional_terms
        )
    elif contract_type in ['dzielo', 'odzielo', 'dzieło']:
        return generate_contract_dzielo(
            employer_name, employer_address, employer_nip,
            employee_name, employee_address, employee_nip, employee_pesel,
            subject, remuneration, currency, start_date, end_date, additional_terms
        )
    elif contract_type in ['najmu', 'wynajmu', 'najemmieszkania']:
        return generate_contract_najmu(
            landlord_name, landlord_address, tenant_name, tenant_address, tenant_pesel,
            property_address, apartment_rooms, apartment_area, apartment_floor,
            apartment_rent, currency, start_date, deposit_amount, notes
        )
    elif contract_type in ['sprzedazy', 'sprzedaz', 'samochodu', 'auta']:
        return generate_contract_sprzedazy(
            seller_name, seller_address, seller_nip, buyer_name, buyer_address, buyer_nip,
            car_brand, car_model, car_year, car_vin, car_price, currency,
            handover_date, advance_date, additional_terms
        )
    elif contract_type in ['przedwstepna', 'przedwstępna', 'przedwstepna_zak']:
        return generate_contract_przedwstepna(
            seller_name, seller_address, seller_nip, buyer_name, buyer_address, buyer_nip,
            property_description, property_address, car_price, currency,
            advance_date, handover_date, additional_terms
        )
    else:
        return {'error': f'Nieznany typ umowy: {contract_type}. Dostępne: zlecenie, dzielo, najmu, sprzedazy, przedwstepna'}

def generate_header(title, date, place="Zamość"):
    """Generuje nagłówek umowy."""
    return f"""
{'='*70}
{'='*70}
                                UMOWA {title}
         zawarta w {place} w dniu {date}
{'='*70}
{'='*70}
"""

def generate_zlecenie_content(
    employer_name, employer_address, employer_nip, employer_pesel,
    employee_name, employee_address, employee_nip, employee_pesel,
    subject, remuneration, currency, start_date, end_date, notice_period, additional_terms
):
    """Generuje treść umowy zlecenia."""
    
    lines = []
    lines.append(f"""
STRONY UMOWY

1. Zleceniodawca:
   {employer_name}
   Adres: {employer_address}
   {"NIP: " + employer_nip if employer_nip else "PESEL: " + employer_pesel if employer_pesel else ""}

   dalej zwany(-a) „Zleceniodawcą"


2. Zleceniobiorca:
   {employee_name}
   Adres: {employee_address}
   {"NIP: " + employee_nip if employee_nip else "PESEL: " + employee_pesel if employee_pesel else ""}

   dalej zwany(-a) „Zleceniobiorcą"


PRZEDMIOT UMOWY

§ 1

Przedmiotem niniejszej umowy jest wykonanie przez Zleceniobiorcę
następującej pracy:

{subject if subject else '[PRZEDMIOT UMOWY - DO UZUPEŁNIENIA]'}

Miejsce wykonywania pracy: {" место wykonywania pracy zostanie podane przez Zleceniodawcę" if not lieu_of_work else "ustalone w § 3"}


WYNAGRODZENIE

§ 2

Za wykonanie przedmiotu umowy Zleceniodawca zapłaci Zleceniobiorcy
wynagrodzenie w wysokości: {remuneration if remuneration else '[KWOTA]'} {currency}

{"Wynagrodzenie płatne po wykonaniu przedmiotu umowy." if not end_date else f"Wynagrodzenie płatne: [DO UZUPEŁNIENIA - np. po wykonaniu / ratalnie / z góry]"}
{"(kwota uwzględnia składki ZUS i podatek)" if employer_nip else "(wynagrodzenie netto, Zleceniodawca potrąca podatek)"}


CZAS TRWANIA

§ 3

Umowa zostaje zawarta na czas:
{"od dnia " + start_date if start_date else "od dnia [DATA ROZPOCZĘCIA]"}
{"do dnia " + end_date if end_date else "do dnia [DATA ZAKOŃCZENIA]"}

{"Strony ustalają możliwość rozwiązania umowy za wypowiedzeniem z zachowaniem " + str(notice_period if notice_period else 3) + "-dniowego okresu wypowiedzenia." if notice_period else ""}


OBOWIĄZKI STRON

§ 4

1. Zleceniodawca zobowiązuje się do:
   - przekazania Zleceniobiorcy niezbędnych informacji i materiałów,
   - terminowej zapłaty wynagrodzenia,
   - zapewnienia właściwych warunków do wykonania pracy.

2. Zleceniobiorca zobowiązuje się do:
   - wykonania pracy zgodnie z ustaleniami stron,
   - stosowania się do wskazówek Zleceniodawcy,
   - zachowania poufności w zakresie informacji uzyskanych przy realizacji umowy,
   - niewykonywania pracy na rzecz innych podmiotów w tym samym czasie bez zgody Zleceniodawcy {"(zakaz konkurencji)" if lieu_of_work else ""}.
""")

    if additional_terms:
        lines.append(f"""
POSTANOWIENIA DODATKOWE

§ 5

{additional_terms}
""")

    lines.append(f"""
ODPOWIEDZIALNOŚĆ

§ 6

1. Zleceniobiorca ponosi odpowiedzialność za szkodę wyrządzoną
   Zleceniodawcy z winy umyślnej lub rażącego niedbalstwa.

2. W przypadku niewykonania lub nienależytego wykonania umowy,
   Zleceniobiorca odpowiada za poniesione straty.


POSTANOWIENIA KOŃCOWE

§ 7

1. W sprawach nieuregulowanych niniejszą umową mają zastosowanie
   przepisy Kodeksu Cywilnego.

2. Wszelkie zmiany umowy wymagają formy pisemnej pod rygorem nieważności.

3. Umowa została sporządzona w dwóch jednobrzmiących egzemplarzach,
   po jednym dla każdej ze stron.

{"Data i podpisy:": "^70}

Zleceniodawca:                      Zleceniobiorca:

...............                      ...............

{employee_name}                     {employer_name}
""")

    return ''.join(lines)

def generate_contract_zlecenie(*args, **kwargs):
    """Generuje umowę zlecenia."""
    content = generate_zlecenie_content(*args, **kwargs)
    header = generate_header("ZLECENIA", datetime.now().strftime('%d.%m.%Y'))
    return {
        'type': 'umowa zlecenia',
        'header': header.strip(),
        'content': content,
        'generated': datetime.now().isoformat()
    }

def generate_contract_dzielo(
    employer_name, employer_address, employer_nip,
    employee_name, employee_address, employee_nip, employee_pesel,
    subject, remuneration, currency, start_date, end_date, additional_terms
):
    """Generuje umowę o dzieło."""
    
    content = f"""
STRONY UMOWY

1. Zamawiający:
   {employer_name}
   Adres: {employer_address}
   {"NIP: " + employer_nip if employer_nip else ""}

2. Wykonawca:
   {employee_name}
   Adres: {employee_address}
   {"NIP: " + employee_nip if employee_nip else "PESEL: " + employee_pesel if employee_pesel else ""}


PRZEDMIOT UMOWY

§ 1

Przedmiotem niniejszej umowy jest stworzenie przez Wykonawcę
następującego dzieła:

{subject if subject else '[DOKŁADNY OPIS DZIEŁA]'}

Dzieło zostanie wykonane w sposób staranny i zgodny z ustaleniami stron.


WYNAGRODZENIE

§ 2

Za wykonanie dzieła Zamawiający zapłaci Wykonawcy wynagrodzenie
w wysokości: {remuneration if remuneration else '[KWOTA]'} {currency}


ODBIÓR DZIEŁA

§ 3

1. Wykonawca zobowiązuje się wykonać i oddać dzieło w terminie:
   {"od " + start_date if start_date else "od [DATA ROZPOCZĘCIA]"}
   {"do " + end_date if end_date else "do [DATA ZAKOŃCZENIA]"}

2. Zamawiający dokona odbioru dzieła w ciągu 7 dni od jego przedstawienia.

3. W przypadku stwierdzenia wad, Zamawiający określi termin ich usunięcia.


POSTANOWIENIA KOŃCOWE

§ 4

1. Z chwilą odbioru dzieła, prawo autorskie przechodzi na Zamawiającego
   (chyba że strony ustalą inaczej).

2. W sprawach nieuregulowanych stosuje się przepisy Kodeksu Cywilnego.

3. Umowa została sporządzona w dwóch egzemplarzach.

Zamawiający:                      Wykonawca:

...............                    ...............

{employer_name}                   {employee_name}
"""
    
    return {
        'type': 'umowa o dzieło',
        'header': generate_header("O DZIEŁO", datetime.now().strftime('%d.%m.%Y')).strip(),
        'content': content,
        'generated': datetime.now().isoformat()
    }

def generate_contract_najmu(
    landlord_name, landlord_address, tenant_name, tenant_address, tenant_pesel,
    property_address, apartment_rooms, apartment_area, apartment_floor,
    apartment_rent, currency, start_date, deposit_amount, notes
):
    """Generuje umowę najmu mieszkania."""
    
    deposit = deposit_amount if deposit_amount else (float(apartment_rent.replace(' ','').replace('zł','').replace(',','.')) if apartment_rent else 0) * 2
    
    content = f"""
STRONY UMOWY

1. Wynajmujący:
   {landlord_name}
   Adres: {landlord_address}

2. Najemca:
   {tenant_name}
   Adres zamieszkania: {tenant_address}
   PESEL: {tenant_pesel if tenant_pesel else '[PESEL]'}


PRZEDMIOT UMOWY

§ 1

Przedmiotem najmu jest lokal mieszkalny położony w:
{property_address if property_address else '[ADRES LOKALU]'}

Na lokal składają się:
- {"pokoi: " + str(apartment_rooms) if apartment_rooms else "liczba pokoi: [DO UZUPEŁNIENIA]"}
- {"powierzchnia: " + str(apartment_area) + " m²" if apartment_area else "powierzchnia: [DO UZUPEŁNIENIA] m²"}
- {"piętro: " + str(apartment_floor) if apartment_floor else "piętro: parter / [NUMER PIĘTRA]"}

Lokal wyposażony jest w standardzie:
- Kuchnia / aneks kuchenny: wyposażony / do wyposażenia przez najemcę
- Łazienka: wanna/prysznic, umywalka, WC
- Ogrzewanie: centralne / gazowe / elektryczne
- Okna: PCV / drewniane


CZAS TRWANIA I CZYNSZ

§ 2

1. Umowa zostaje zawarta na czas:
   {"od " + start_date if start_date else "od [DATA ROZPOCZĘCIA NAJMU]"}

2. Miesięczny czynsz najmu wynosi:
   {apartment_rent if apartment_rent else '[KWOTA]'} {currency}

3. Czynsz płatny z dołu do 10. dnia każdego miesiąca na konto Wynajmującego.

4. Najemca zobowiązany jest do wpłacenia kaucji w wysokości:
   {deposit} {currency} (dwukrotność miesięcznego czynszu)
   Kaucja zostanie zwrócona w ciągu 30 dni od opuszczenia lokalu.


OBOWIĄZKI STRON

§ 3

1. Wynajmujący zobowiązuje się do:
   - wydania lokalu w stanie przydatnym do umówionego użytku
   - zapewnienia ciągłego korzystania z lokalu
   - dokonywania napraw i konserwacji budynku

2. Najemca zobowiązuje się do:
   - używania lokalu zgodnie z jego przeznaczeniem
   - utrzymywania lokalu w należytym stanie
   - terminowego płacenia czynszu i opłat eksploatacyjnych
   - nieoddawania lokalu w podnajem bez zgody Wynajmującego
   - przestrzegania Regulaminu budynku


PROTOKÓŁ ZDAWCZO-ODBIORCZY

§ 4

1. Stan lokalu zostanie spisany w protokole zdawczo-odbiorczym,
   stanowiącym załącznik nr 1 do niniejszej umowy.

2. Przy opuszczeniu lokalu, najemca zobowiązany jest do:
   - usunięcia wszelkich własnych rzeczy
   - przeprowadzenia drobnych napraw (malowanie, dziury po obrazach)
   - przekazania kluczy Wynajmującemu

3. Wszelkie szkody powstałe z winy najemcy zostaną potrącone z kaucji.


ROZWIĄZANIE UMOWY

§ 5

1. Każda ze stron może wypowiedzieć umowę z zachowaniem
   {"1-miesięcznego" if False else "3-miesięcznego"} okresu wypowiedzenia.

2. Wynajmujący może wypowiedzieć umowę bez zachowania terminu wypowiedzenia
   w przypadku:
   - zwłoki z zapłatą czynszu powyżej 3 miesięcy
   - używania lokalu w sposób sprzeczny z umową
   - podnajmu bez zgody Wynajmującego
   - dewastacji lokalu


POSTANOWIENIA KOŃCOWE

§ 6

1. W sprawach nieuregulowanych stosuje się Kodeks Cywilny.

2. Wszelkie zmiany wymagają formy pisemnej.

3. Umowa została zawarta w dwóch egzemplarzach.

{"Załącznik 1: Protokół zdawczo-odbiorczy lokalu": "^70}

Data i podpisy:

Wynajmujący:                        Najemca:

...............                      ...............

{landlord_name}                     {tenant_name}
"""
    
    return {
        'type': 'umowa najmu',
        'header': generate_header("NAJMU LOKALU MIESZKALNEGO", datetime.now().strftime('%d.%m.%Y')).strip(),
        'content': content,
        'generated': datetime.now().isoformat()
    }

def generate_contract_sprzedazy(
    seller_name, seller_address, seller_nip, buyer_name, buyer_address, buyer_nip,
    car_brand, car_model, car_year, car_vin, car_price, currency,
    handover_date, advance_date, additional_terms
):
    """Generuje umowę sprzedaży samochodu."""
    
    content = f"""
STRONY UMOWY

Sprzedający:
{buyer_name if seller_name is None else seller_name}
Adres: {seller_address if seller_address else '[ADRES SPRZEDAJĄCEGO]'}
NIP: {seller_nip if seller_nip else '[NIP]'}

Kupujący:
{buyer_name if buyer_name else '[IMIĘ I NAZWISKO]'}
Adres: {buyer_address if buyer_address else '[ADRES KUPUJĄCEGO]'}
NIP: {buyer_nip if buyer_nip else '[NIP]'}


PRZEDMIOT SPRZEDAŻY

§ 1

Przedmiotem niniejszej umowy jest pojazd:
- Marka: {car_brand if car_brand else '[MARKA]'}
- Model: {car_model if car_model else '[MODEL]'}
- Rok produkcji: {car_year if car_year else '[ROK]'}
- Numer VIN: {car_vin if car_vin else '[VIN]'}
- Stan techniczny: zgodny z ogłoszeniem / sprawdzony / do naprawy

Sprzedający oświadcza, że:
- jest właścicielem pojazdu i przysługuje mu prawo do jego sprzedaży
- pojazd nie jest obciążony hipoteką ani innymi roszczeniami osób trzecich
- dane techniczne są zgodne ze stanem faktycznym


CENA I WARUNKI PŁATNOŚCI

§ 2

Cena sprzedaży wynosi: {car_price if car_price else '[KWOTA]'} {currency}

{"Zadatko w wysokości 10% ceny zostało wpłacone w dniu podpisania umowy." if advance_date else ""}

Pozostała kwota zostanie uregulowana:
{"w dniu przekazania pojazdu" if handover_date else "w dniu [DATA PŁATNOŚCI]"}


PRZEKAZANIE POJAZDU

§ 3

Przekazanie pojazdu nastąpi w dniu: {handover_date if handover_date else '[DATA PRZEKAZANIA]'}
w miejscu: {seller_address if seller_address else '[MIEJSCE PRZEKAZANIA]'}

Wraz z pojazdem Sprzedający przekaże:
- dowód rejestracyjny
- kartę pojazdu (jeśli była wydana)
- aktualne ubezpieczenie OC
- tablice rejestracyjne
- kluczyki (2 szt.)
- instrukcję obsługi

{"Protokół zdawczo-odbiorczy stanowi załącznik do umowy." if True else ""}


OŚWIADCZENIA STRON

§ 4

1. Sprzedający oświadcza, że nie są mu znane wady prawne ani fizyczne pojazdu,
   z wyjątkiem ujawnionych w ogłoszeniu / usterek wymienionych poniżej.

2. Kupujący oświadcza, że zapoznał się ze stanem technicznym pojazdu
   i akceptuje go w obecnym stanie.

3. Strony wzajemnie oświadczają, że są pelnoletnie i posiadają pełną zdolność
   do czynności prawnych.


POSTANOWIENIA KOŃCOWE

§ 5

1. W sprawach nieuregulowanych stosuje się Kodeks Cywilny.

2. Koszty związane z przerejestrowaniem pojazdu ponosi Kupujący.

3. Umowa została sporządzona w dwóch jednobrzmiących egzemplarzach.

{"Data i podpisy:": "^70}

Sprzedający:                        Kupujący:

...............                      ...............

{seller_name if seller_name else '[IMIĘ NAZWISKO]'}      [IMIĘ NAZWISKO]
"""
    
    return {
        'type': 'umowa sprzedaży samochodu',
        'header': generate_header("SPRZEDAŻY POJAZDU", datetime.now().strftime('%d.%m.%Y')).strip(),
        'content': content,
        'generated': datetime.now().isoformat()
    }

def generate_contract_przedwstepna(
    seller_name, seller_address, seller_nip, buyer_name, buyer_address, buyer_nip,
    property_description, property_address, car_price, currency,
    advance_date, handover_date, additional_terms
):
    """Generuje umowę przedwstępną."""
    
    content = f"""
STRONY UMOWY

1. Strona sprzedająca (Zbywający):
{buyer_name if seller_name is None else seller_name}
Adres: {seller_address if seller_address else '[ADRES]'}
NIP: {seller_nip if seller_nip else '[NIP]'}

2. Strona kupująca (Nabywca):
{buyer_name if buyer_name else '[IMIĘ I NAZWISKO]'}
Adres: {buyer_address if buyer_address else '[ADRES]'}
NIP: {buyer_nip if buyer_nip else '[NIP]'}


PRZEDMIOT UMOWY

§ 1

Niniejsza umowa dotyczy:
{property_description if property_description else '[DOKŁADNY OPIS PRZEDMIOTU np. mieszkania, działki]'}

Położonego w: {property_address if property_address else '[ADRES NIERUCHOMOŚCI]'}

Strony zobowiązują się do zawarcia w terminie określonym w § 3
umowy przyrzeczonej (umowy sprzedaży / zamiany / darowizny) na powyższy przedmiot.


CENA I ZADATEK

§ 2

Strony ustalają, że cena przedmiotu umowy wynosi: {car_price if car_price else '[KWOTA]'} {currency}

{"W dniu podpisania niniejszej umowy Kupujący wpłaca Zadatko w wysokości 10% ceny," if advance_date else "Strony ustalają wpłatę zadatku w wysokości 10% ceny:"}
tj. kwotę: {float(car_price.replace(' ', '').replace('zł', '').replace(',', '.')) * 0.1 if car_price else '[10% CENY]'} {currency}


TERMIN ZAWARCIA UMOWY PRZYRZECZONEJ

§ 3

Umowa przyrzeczona (przyrzeczona sprzedaż) zostanie zawarta
w terminie do: {advance_date if advance_date else '[TERMIN Zawarcia umowy przyrzeczonej]'}
w kancelarii notarialnej wskazanej przez Strony.

{"Przeniesienie własności nastąpi po zapłacie pełnej ceny." if True else ""}


ZASADY ROZWIĄZANIA

§ 4

1. Jeżeli Kupujący uchyla się od zawarcia umowy przyrzeczonej,
   traci wpłacony Zadatek na rzecz Sprzedającego.

2. Jeżeli Sprzedający uchyla się od zawarcia umowy przyrzeczonej,
   zobowiązany jest zwrócić Kupującemu Zadatek w podwójnej wysokości.

3. Strony mogą rozwiązać umowę za porozumieniem stron w formie pisemnej.


OŚWIADCZENIA STRON

§ 5

1. Sprzedający oświadcza, że przysługuje mu prawo własności przedmiotu
   i nie jest on obciążony prawami osób trzecich.

2. Kupujący oświadcza, że zapoznał się ze stanem prawnym i fizycznym
   przedmiotu umowy i nie zgłasza zastrzeżeń.

3. Strony zobowiązują się do współdziałania w celu zawarcia umowy przyrzeczonej.


POSTANOWIENIA KOŃCOWE

§ 6

1. W sprawach nieuregulowanych stosuje się Kodeks Cywilny.

2. Wszelkie zmiany wymagają formy pisemnej.

3. Umowa została sporządzona w dwóch egzemplarzach.

{"Data i podpisy:": "^70}

Sprzedający:                        Kupujący:

...............                      ...............

{seller_name if seller_name else '[IMIĘ NAZWISKO]'}      [IMIĘ NAZWISKO]
"""
    
    return {
        'type': 'umowa przedwstępna',
        'header': generate_header("PRZEDWSTĘPNA", datetime.now().strftime('%d.%m.%Y')).strip(),
        'content': content,
        'generated': datetime.now().isoformat()
    }

def format_contract(contract):
    """Formatuje umowę do wyświetlenia."""
    if 'error' in contract:
        return f"❌ Błąd: {contract['error']}"
    
    return f"""
{contract.get('header', '')}
{contract.get('content', '')}
---
Wygenerowano: {contract.get('generated', '')[:10]}
"""

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                📄 UmowaGenerator v1.0 📄                                    ║
║              Generator Umów Prawnych dla Polaków                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    if '--demo' in sys.argv or '--help' in sys.argv or len(sys.argv) < 2:
        print("""
📖 DOSTĘPNE POLECENIA:

   python3 umowa_generator.py --type=zlecenie       — Umowa zlecenia
   python3 umowa_generator.py --type=dzielo         — Umowa o dzieło
   python3 umowa_generator.py --type=najmu          — Umowa najmu
   python3 umowa_generator.py --type=sprzedazy      — Sprzedaż samochodu
   python3 umowa_generator.py --type=przedwstepna   — Umowa przedwstępna
   python3 umowa_generator.py --demo                — Demo wszystkich typów

💡 PRZYKŁAD:
   python3 umowa_generator.py --type=zlecenie --demo
        """)
        
        print("\n" + "="*70)
        print("🚀 DEMO: Umowa zlecenia")
        print("="*70 + "\n")
        
        contract = generate_contract_zlecenie(
            employer_name="Firma IT sp. z o.o.",
            employer_address="ul. Główna 1, 20-001 Lublin",
            employer_nip="1234567890",
            employee_name="Jan Kowalski",
            employee_address="ul. Kwiatowa 5, 22-400 Zamość",
            employee_pesel="90010100000",
            subject="Wsparcie techniczne systemu informatycznego",
            remuneration="5 000,00",
            currency="PLN",
            start_date="01.06.2026",
            end_date="30.06.2026",
            notice_period=3
        )
        print(format_contract(contract))
    
    elif '--type=' in sys.argv[1]:
        contract_type = sys.argv[1].split('=')[1]
        
        if contract_type == 'zlecenie':
            contract = generate_contract_zlecenie(
                employer_name="[NAZWA FIRM / IMIĘ NAZWISKO]",
                employer_address="[ADRES]",
                employer_nip="[NIP lub PESEL]",
                employee_name="[IMIĘ NAZWISKO]",
                employee_address="[ADRES]",
                employee_pesel="[PESEL]",
                subject="[PRZEDMIOT UMOWY]",
                remuneration="[WYNAGRODZENIE]",
                currency="PLN"
            )
        elif contract_type == 'dzielo':
            contract = generate_contract_dzielo(
                employer_name="[NAZWA FIRM / IMIĘ NAZWISKO]",
                employer_address="[ADRES]",
                employer_nip="[NIP]",
                employee_name="[IMIĘ NAZWISKO]",
                employee_address="[ADRES]",
                employee_nip="[NIP lub PESEL]",
                subject="[DOKŁADNY OPIS DZIEŁA]",
                remuneration="[WYNAGRODZENIE]"
            )
        elif contract_type == 'najmu':
            contract = generate_contract_najmu(
                landlord_name="[IMIĘ NAZWISKO WLASCICIELA]",
                landlord_address="[ADRES WLASCICIELA]",
                tenant_name="[IMIĘ NAZWISKO NAJEMCY]",
                tenant_address="[ADRES ZAMIESZKANIA]",
                tenant_pesel="[PESEL]",
                property_address="[ADRES MIESZKANIA]",
                apartment_rent="[CZYNSZ MIESIĘCZNY]"
            )
        elif contract_type == 'sprzedazy':
            contract = generate_contract_sprzedazy(
                seller_name="[IMIĘ NAZWISKO SPRZEDAJĄCEGO]",
                seller_address="[ADRES]",
                seller_nip="[NIP]",
                buyer_name="[IMIĘ NAZWISKO KUPUJĄCEGO]",
                buyer_address="[ADRES]",
                car_brand="[MARKA]",
                car_model="[MODEL]",
                car_year="[ROK]",
                car_vin="[VIN]",
                car_price="[CENA]"
            )
        elif contract_type == 'przedwstepna':
            contract = generate_contract_przedwstepna(
                seller_name="[IMIĘ NAZWISKO]",
                seller_address="[ADRES]",
                seller_nip="[NIP]",
                buyer_name="[IMIĘ NAZWISKO]",
                buyer_address="[ADRES]",
                property_description="[OPIS NIERUCHOMOŚCI]",
                property_address="[ADRES NIERUCHOMOŚCI]",
                car_price="[CENA]"
            )
        else:
            contract = {'error': f'Nieznany typ: {contract_type}'}
        
        print(format_contract(contract))

if __name__ == "__main__":
    main()