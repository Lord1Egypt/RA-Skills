# Scoring-Parameter Referenz – Erweitert v2.0

## Gewichtete Parameter (0–10 Gesamtscore)

| # | Parameter | Gewicht | Quelle | Invertiert? | Neu? |
|---|-----------|---------|--------|-------------|------|
| 1 | CAPE (J/kg) | 12% | Open-Meteo | Nein | — |
| 2 | Grenzschichthöhe BLH (m AGL) | 18% | Open-Meteo | Nein | — |
| 3 | Lifted Index | 8% | Open-Meteo | Nein | — |
| 4 | Bewölkung low+mid (%) | 12% | Open-Meteo | Ja | — |
| 5 | Wind 10m (km/h) | 8% | Open-Meteo | Ja | — |
| 6 | Temperatur-Spread T-Td (°C) | 5% | Berechnet | Nein | — |
| 7 | Direkte Strahlung (W/m²) | 10% | Open-Meteo | Nein | — |
| 8 | Bodenfeuchte 0-1cm (m³/m³) | 8% | Open-Meteo | Ja | — |
| 9 | Vortages-Regen (mm) | 5% | Open-Meteo | Ja | — |
| 10 | **Windscherung 10m→850hPa** | **7%** | Open-Meteo | Ja | ✅ |
| 11 | **Relative Feuchte 700hPa (%)** | **5%** | Open-Meteo | Ja | ✅ |
| 12 | **Hangflug-Bonus** | **+0–2** | Berechnet | Nein | ✅ |

Gesamt-Basisgewichte: 100% → Score 0–10
Hangflug-Bonus additiv (kann Score auf max 10 erhöhen).

---

## Neue Parameter – Details

### Windscherung (10m → 850 hPa)
Windscherung = Differenz Windgeschwindigkeit/Richtung zwischen 10m und ~1500m MSL (850hPa).
Starke Scherung destabilisiert Thermikschläuche und erhöht Turbulenzen.

```python
shear_ms = sqrt((u850-u10)**2 + (v850-v10)**2)  # in m/s
shear_kmh = shear_ms * 3.6
```

Bewertung:
- Excellent: 0–8 km/h → ruhige Thermikschläuche
- Good:      8–15 km/h
- OK:        15–22 km/h → etwas zerzaust
- Poor:      22–30 km/h → schwierig
- Very Poor: >30 km/h → unfliegbar für Thermik

### Relative Feuchte 700 hPa (~3000m MSL)
Trockene Luftmassen in mittleren Niveaus fördern tiefe, scharfe Cu-Basis und starke Thermik.
Nasse Luft → Überentwicklungsrisiko, Absoaken, Cb-Gefahr.

Bewertung:
- Excellent: <25% → sehr trockene Luft, perfekte Cu-Thermik
- Good:      25–40%
- OK:        40–55% → normal
- Poor:      55–70% → Überentwicklungsrisiko steigt
- Very Poor: >70% → Cb/Gewitter wahrscheinlich (Warnung!)

**Kombinations-Warnung:** Feuchte 700hPa >65% UND CAPE >800 J/kg → 🔴 GEWITTERGEFAHR

### Hangflug-Bonus (nur Alpenregionen)
Berechnet anhand von Windrichtung und Geländeausrichtung.
Für Werdenfels: Nordalpenkamm verläuft etwa West-Ost.

```
Hangwindrichtungen (Werdenfels):
  Nord (330–030°): Nordhangaufwind am Alpenrand → moderater Bonus
  Süd (150–210°): Föhn-Situation → kein Bonus (Föhn-Check dominant)
  
Hangflug-Score:
  Wind 15–35 km/h AUS optimaler Richtung: +1.5
  Wind 35–50 km/h AUS optimaler Richtung: +1.0 (stärker, aber nutzbar)
  Wind <15 km/h:                          +0   (zu schwach)
  Wind >50 km/h:                          +0   (zu stark, gefährlich)
  Kein Regen, kein Föhn:                  Voraussetzung
```

---

## Bestehende Parameter – Schwellwerte (unverändert)

### CAPE (Convective Available Potential Energy)
- Poor: 0–50 J/kg
- OK: 50–150 J/kg
- Good: 150–400 J/kg
- Very Good: 400–900 J/kg
- Excellent: 900–1500 J/kg
- **Gewitterwarnung:** >2000 J/kg

### Grenzschichthöhe (BLH)
- Poor: 0–500m → kaum Thermik
- OK: 500–1000m → schwache Platzrundthermik
- Good: 1000–1800m → solide Thermik, 30–50km Strecken
- Very Good: 1800–2500m → gute Streckenbedingungen
- Excellent: 2500–4000m → Hammertag, lange Strecken

### Lifted Index
- Poor: >2 → stabile Schichtung
- OK: 0 bis 2 → schwach labil
- Good: -2 bis 0 → gute Labilität
- Very Good: -4 bis -2 → starke Labilität
- Excellent: -8 bis -4 → sehr starke Konvektion
- **Gewitterwarnung:** <-6

---

## Föhn-Erkennung (Alpen)

Föhn macht Segelflug schwierig bis unmöglich – trotz optisch gutem Wetter.

```python
foehn_detected = (
    wind_dir_10m in (150..240)  # Südwind am Boden
    AND wind_speed_10m > 25 km/h
    AND (T_2m - T_dewpoint) > 8°C   # sehr trockene Luft
    AND precip_24h < 0.5mm          # kein Regen (Föhnschlier)
)
```

Bei Föhn:
- Score-Malus: -3 Punkte (Minimum 0)
- Warnung: 🔴 FÖHN – Turbulenz am Alpenrand, Böen möglich
- Hangflug-Bonus wird NICHT angewandt

---

## Überentwicklungs-Warnung (Alpen)

```python
overdev_risk = (
    cape > 600
    AND rh_700 > 55
    AND cloud_cover_mid > 30
    AND blh > 2000
)
```

- Moderat: ⚠️ Überentwicklung möglich – früh starten, 14:00 landen
- Hoch:    🔴 Cb-Gefahr – Gewitterentwicklung wahrscheinlich

---

## Steigwert-Schätzung (erweitert)

```
w ≈ √(2·CAPE) × 0.04 × BLH_factor × CloudCover_factor × Wind_factor × Shear_factor
```

- BLH_factor:   min(BLH/2000, 1.5)
- CC_factor:    max(0.3, 1.0 - CC_low/150)
- Wind_factor:  max(0.3, 1.0 - max(0, Wind-15)/40)
- Shear_factor: max(0.5, 1.0 - shear_kmh/60)  ← NEU
- Ergebnis: 0–5 m/s, typisch 0.8–2.5 m/s

## Wolkenbasis-Schätzung (unverändert)

```
Basis_MSL = Platzhöhe + (T - Td) × 125 m/°C
```

---

## Datenquellen

- **Open-Meteo API**: Kostenlos, ICON-D2 (2km Auflösung), ICON-EU Fallback
  - Neue Felder: `windspeed_850hpa`, `winddirection_850hpa`, `relativehumidity_700hpa`
  - u/v-Komponenten für Scherungsberechnung: `u_component_of_wind_10m`, `u_component_of_wind_850hpa`
- **DHV Wetter**: Meteorologe Volker Schwaniz, 2× täglich
