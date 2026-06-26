---
name: soaring-weather
description: Segelflug- und Thermikvorhersage mit Thermik-Score (0-10). Nutze diesen Skill wenn der User nach Segelflugwetter, Thermik, Streckenflugbedingungen, Flugwetter fuer Segelflieger oder Gleitschirmflieger fragt - auch indirekt wie "lohnt sich Samstag fliegen?", "wie wird die Thermik?", "Segelflugwetter Wochenende?" oder "kann ich am Sonntag einen Streckenflug machen?" oder "Wettercheck Werdenfels". Der Skill ruft Open-Meteo (ICON-D2) ab und liefert eine Profi-Einschaetzung mit Tagesablauf, Steigwerten, Basishöhe, Alpen-Besonderheiten (Foehn, Hangflug) und Warnungen.
version: 2.0.0
---

# Soaring Weather – Thermikvorhersage für Segelflieger v2.0

Scoring-Engine mit 11 gewichteten Parametern inkl. Windscherung, Höhenfeuchte,
Föhn-Erkennung, Hangflug-Bonus und Gewittersicherheits-Cap.

## Schritt 1: Region erfragen

```bash
python3 {baseDir}/scripts/run_forecast.py --list-regions
```

Stelle dem User die Optionen zur Auswahl:

> Für welche Region möchtest du die Thermikvorhersage?
> 1. 🏔️ Werdenfels / Bayerischer Alpenordrand
> 2. 🏔️ Inntal / Nordtiroler Alpen
> 3. ⛰️ Schwäbische Alb
> 4. 🌲 Schwarzwald
> 5. 🌾 Norddeutsches Flachland
> 6. 📍 Eigene Koordinaten eingeben

Falls der User bereits eine Region nennt, überspringe die Frage.

## Schritt 2: Vorhersage abrufen

```bash
python3 {baseDir}/scripts/run_forecast.py --region <region_id> [--days 3]
```

Oder mit eigenen Koordinaten:

```bash
python3 {baseDir}/scripts/run_forecast.py --lat <lat> --lon <lon> --name "Name"
```

Das Script gibt JSON auf stdout aus, Logs auf stderr.

## Schritt 3: Ergebnis formatieren

### Tagesübersicht (pro Tag)

```
[Emoji] THERMIK-VORHERSAGE – [Standortname]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 [Wochentag], [Datum]
🏆 SCORE: [X]/10 — [Label]

🌡️ Thermik-Kern:
   Steigwerte: ~[X] m/s | Basis: [X]m MSL | BLH: [X]m AGL
   CAPE max: [X] J/kg

💨 Wind: ⌀[X] km/h | Windscherung: [X] km/h (10m→850hPa)
💧 Höhenluft (700hPa): [X]% r.F. → [trocken/normal/feucht]
🌍 Boden: [Feuchte-Bewertung]

[🏔️ Hangflug-Bonus: +X Punkte – Nordwindlage günstig]  ← nur wenn relevant
[⚠️ Warnungen]

📊 Tagesablauf:
   09-12: [◉◉◉◎◎] ~[X]m/s · BLH [X]m
   12-15: [◉◉◉◉◎] ~[X]m/s · BLH [X]m
   15-18: [◉◉◉◉◉] ~[X]m/s · BLH [X]m
   18-20: [◉◉◎◎◎] ~[X]m/s · BLH [X]m
```

### Score-Emoji und Labels
- 0–2:  ❌ Kein Segelflugwetter
- 2–4:  🌥️ Eingeschränkt
- 4–6:  ⛅ Ordentlicher Tag
- 6–8:  ☀️ Guter Tag
- 8–10: 🔥 Hammertag!

### Wichtige Warnungstypen
- 🔴 FÖHN: Score gecappt, Turbulenz am Alpenrand
- 🔴 Gewittergefahr (CAPE >2000 oder LI <-6): Score hard cap bei 4.5
- 🔴 Cb-Gefahr: Feuchte 700hPa >65% + CAPE >800 → Score -2
- ⚠️ Überentwicklung: Früh starten, 14:00 landen
- ⚠️ Windscherung >30 km/h: Thermikschläuche destabilisiert

### Hangflug-Bonus (nur Alpen)
Wird angezeigt wenn Score >0 Bonus. Erkläre kurz die Windrichtung.
Kein Bonus bei Föhn oder Niederschlag.

## Schritt 4: Links anbieten

Am Ende immer:
- DHV Wetter: https://www.dhv.de/wetter/dhv-wetter/
- SkySight: https://skysight.io
- TopMeteo: https://europe.topmeteo.eu/de/
- DWD Segelflug: https://www.dwd.de/DE/fachnutzer/luftfahrt/kg_segel/segel_node.html
- Soaringmeteo (WRF 2km): https://soaringmeteo.org/v2
- aufwin.de: https://aufwin.de

## Parameter-Details

→ Siehe `{baseDir}/references/scoring_params.md` für alle Schwellwerte,
  Gewichte, Formeln und Regionstypen.

## Kurzübersicht Scoring-Parameter

| Parameter              | Gewicht | Besonderheit                          |
|------------------------|---------|---------------------------------------|
| Grenzschichthöhe BLH   | 18%     | Wichtigster Einzelparameter           |
| CAPE                   | 12%     | Hard cap bei >2000 J/kg               |
| Bewölkung low+mid      | 12%     | Cu-Thermik-Bonus bei 15–50%           |
| Direkte Strahlung      | 10%     | Antrieb der Thermik                   |
| Lifted Index           | 8%      | Hard cap bei <-6                      |
| Wind 10m               | 8%      | Zu stark = schlecht                   |
| Bodenfeuchte           | 8%      | Trockener Boden = bessere Thermik     |
| **Windscherung →850hPa** | **7%** | **NEU: zerzaust Thermikschläuche**    |
| **RH 700hPa**          | **7%**  | **NEU: Cb-Früherkennung**             |
| Vortages-Regen         | 5%      | —                                     |
| Spread T-Td            | 5%      | Wolkenbasishöhe                       |
