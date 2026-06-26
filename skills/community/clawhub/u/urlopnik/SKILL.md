# Urlopnik — Inteligentny asystent urlopowy

## Description
Inteligentny asystent do zarządzania urlopami w Polsce. Automatycznie oblicza dni urlopowe, generuje wnioski urlopowe w formacie PDF i wysyła do przełożonego.

## Features
- **Obliczanie urlopu** — ile dni urlopu przysługuje pracownikowi
- **Generator wniosków** — tworzy profesjonalny wniosek URLOP w formacie PDF
- **Kalendarz urlopów** — podgląd dni wolnych w miesiącu
- **Planowanie urlopu** — sugestie najlepszych terminów

## Wymagania
- Python 3.8+ (do lokalnego uruchomienia)
- OpenClaw z zainstalowanym skillem
- Dane pracownika: imię, nazwisko, stanowisko, dział

## Usage
Użytkownik podaje:
1. Datę początkową i końcową urlopu
2. Rodzaj urlopu (wypoczynkowy, na żądanie, macierzyński, itp.)
3. Dane pracownika (jednorazowo, potem zapamiętuje)

Skill automatycznie:
- Sprawdza czy pracownik ma wystarczającą liczbę dni
- Oblicza ile dni urlopu zostanie po urlopie
- Generuje wniosek URLOP w formacie PDF
- Podpowiada czy wybrać dzień wolny / długi weekend

## Przykłady użycia
```
"Chcę wziąć urlop od 15 do 19 lipca"
"Oblicz ile dni urlopu mi zostało"
"Wyślij wniosek urlopowy do mojego szefa"
"Jaki jest mój limit dni urlopu?"
```

## Autor
**Twórca:** Tomasz Pędzierski
**Wersja:** 2.0.0
**Data:** 2026-05-03

---

## 💰 Wersja PRO

**Chcesz więcej?** Wersja PRO zawiera:
- Generator PDF wniosków urlopowych (gotowy do wydruku)
- Wysyłanie wniosków mailem do przełożonego
- Statystyki wykorzystania urlopu (ile dni, kiedy, ile zostało)
- Podpowiedzi optymalnych dat (przedłużone weekendy)
- Automatyczne przypomnienia o niewykorzystanym urlopie

**Cena:** 9.99 zł netto (12.29 zł brutto z VAT 23%)

**Jak wykupić?** Wyślij maila na tomaszpedzierski.infinity@wp.pl — odpowiem z linkiem do płatności.

---

## Licencja
MIT License

## Status
✅ Gotowy do użycia — wersja darmowa

---

*Skill stworzony z ❤️ dla pracowników w Polsce*
*Twórca: Tomasz Pędzierski*