#!/usr/bin/env python3
"""Used Car Sentinel — offline listing decoder and deal screener.

Validates/decodes VINs (ISO 3779 check digit), scores mileage plausibility,
models a fair-price band, and prints inspection/negotiation sheets.
No network, no API keys, stdlib only.

Informational tool — not a substitute for a vehicle-history report or a
professional pre-purchase inspection.
"""
import argparse
import datetime as dt
import sys

# ---------------------------------------------------------------- VIN tables
VIN_LETTER_VALUES = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
    "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
}
VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
YEAR_CODES = {
    "A": 2010, "B": 2011, "C": 2012, "D": 2013, "E": 2014, "F": 2015,
    "G": 2016, "H": 2017, "J": 2018, "K": 2019, "L": 2020, "M": 2021,
    "N": 2022, "P": 2023, "R": 2024, "S": 2025, "T": 2026, "V": 2027,
    "1": 2031, "2": 2032, "3": 2033, "4": 2034, "5": 2035, "6": 2036,
    "7": 2037, "8": 2038, "9": 2039,
}
WMI_DB = {
    # North America
    "1HG": ("Honda", "US"), "1FT": ("Ford", "US"), "1GM": (" GMC", "US"),
    "1C4": ("Jeep", "US"), "1FA": ("Ford", "US"), "1G1": ("Chevrolet", "US"),
    "2T1": ("Toyota", "CA"), "2FA": ("Ford", "CA"), "2HG": ("Honda", "CA"),
    "3FA": ("Ford", "MX"), "3MZ": ("Mazda", "MX"), "3GN": ("Chevrolet", "MX"),
    # Japan
    "JHM": ("Honda", "JP"), "JTD": ("Toyota", "JP"), "JT": ("Toyota", "JP"),
    "JN1": ("Nissan", "JP"), "JN8": ("Nissan", "JP"), "JM1": ("Mazda", "JP"),
    "JM3": ("Mazda", "JP"), "JS3": ("Suzuki", "JP"), "JF1": ("Subaru", "JP"),
    "JA3": ("Mitsubishi", "JP"), "JD1": ("Isuzu", "JP"),
    "5YJ": ("Tesla", "US"), "7SA": ("Tesla", "US"), "7FC": ("Tesla", "US"),
    # Germany
    "WBA": ("BMW", "DE"), "WBS": ("BMW M", "DE"), "WDB": ("Mercedes-Benz", "DE"),
    "WDD": ("Mercedes-Benz", "DE"), "WDC": ("Mercedes-Benz", "DE"),
    "WVW": ("Volkswagen", "DE"), "WV1": ("Volkswagen CV", "DE"),
    "WAU": ("Audi", "DE"), "WAU": ("Audi", "DE"), "WP0": ("Porsche", "DE"),
    "WP1": ("Porsche", "DE"), "W0L": ("Opel", "DE"), "WME": ("Smart", "DE"),
    # Korea
    "KMH": ("Hyundai", "KR"), "KM8": ("Hyundai", "KR"), "KNA": ("Kia", "KR"),
    "KNM": ("Kia", "KR"), "KND": ("Kia", "KR"), "KL4": ("Daewoo/GM Korea", "KR"),
    "KLV": ("GM Korea", "KR"), "KNL": ("Renault Korea", "KR"), "KMH4": ("Hyundai", "KR"),
    # China
    "LSV": ("VW SAIC", "CN"), "LSJ": ("MG", "CN"), "LBV": ("BMW Brilliance", "CN"),
    "LB3": ("Geely", "CN"), "LVS": ("Ford Changan", "CN"), "LVG": ("GAC Toyota", "CN"),
    "LDC": ("Dongfeng Peugeot", "CN"), "LSY": ("Chery", "CN"), "LZW": ("Wuling", "CN"),
    "LBE": ("Beijing Hyundai", "CN"), "LB2": ("Changan", "CN"), "L6T": ("Renault Samsung", "CN"),
    # France / Italy / UK / Spain / CZ / TR
    "VF1": ("Renault", "FR"), "VF3": ("Peugeot", "FR"), "VF7": ("Citroën", "FR"),
    "VR1": ("Renault", "FR"), "VXK": ("Peugeot", "FR"), "ZFA": ("Fiat", "IT"),
    "ZFF": ("Ferrari", "IT"), "ZAR": ("Alfa Romeo", "IT"), "ZAM": ("Maserati", "IT"),
    "SAL": ("Land Rover", "GB"), "SAR": ("Rover", "GB"), "SAJ": ("Jaguar", "GB"),
    "SB1": ("Toyota GB", "GB"), "SCB": ("Bentley", "GB"), "SHS": ("Honda GB", "GB"),
    "VSS": ("Seat", "ES"), "VSX": ("Opel Spain", "ES"), "VWV": ("VW Spain", "ES"),
    "TMB": ("Škoda", "CZ"), "TMA": ("Hyundai CZ", "CZ"), "TMP": ("Škoda", "CZ"),
    "NMT": ("Toyota TR", "TR"), "NLH": ("Hyundai Assan", "TR"), "VNK": ("Toyota TR", "TR"),
    # Others
    "YS3": ("Saab", "SE"), "YV1": ("Volvo", "SE"), "YS2": ("Scania", "SE"),
    "TRU": ("Audi HU", "HU"), "SUA": ("Subaru", "US"), "4S3": ("Subaru", "US"),
    "JTK": ("Toyota", "JP"), "4T1": ("Toyota", "US"), "5TD": ("Toyota", "US"),
    "5NP": ("Hyundai", "US"), "5YM": ("BMW US", "US"), "4US": ("BMW US", "US"),
    "1N4": ("Nissan", "US"), "1VW": ("Volkswagen", "US"), "3VW": ("Volkswagen", "US"),
    "9BW": ("Volkswagen", "BR"), "93H": ("Honda", "BR"), "95V": ("VW", "BR"),
    "MA3": ("Suzuki", "IN"), "MA1": ("Mahindra", "IN"), "MAL": ("Hyundai", "IN"),
    "MB1": ("Ashok Leyland", "IN"), "MC2": ("Honda", "IN"), "MDH": ("Maruti", "IN"),
    "XTA": ("Lada/VAZ", "RU"), "X9F": ("Ford", "TR"), "X4X": ("BMW", "RU"),
    "Z8N": ("Nissan", "RU"), "XW8": ("VW", "RU"), "WE0": ("Ford", "TR"),
}

CLASS_NORMS = {  # km/year typical band (lo, hi, label)
    "city":       (7_000, 14_000, "city runabout"),
    "compact":    (10_000, 20_000, "compact/compact-SUV"),
    "family":     (12_000, 22_000, "family sedan/SUV"),
    "highway":    (20_000, 35_000, "highway cruiser"),
    "fleet":      (40_000, 80_000, "taxi/fleet"),
    "sport":      (5_000, 12_000, "sportscar"),
    "offroad":    (10_000, 18_000, "offroad SUV"),
}

# base values (USD-ish, relative scale only) + annual depreciation
CLASS_VALUE = {
    "city": (14_000, 0.115), "compact": (22_000, 0.115), "family": (30_000, 0.12),
    "highway": (34_000, 0.13), "fleet": (26_000, 0.155), "sport": (45_000, 0.13),
    "offroad": (38_000, 0.115),
}


# ---------------------------------------------------------------- VIN logic
def vin_transliterate(ch):
    if ch.isdigit():
        return int(ch)
    return VIN_LETTER_VALUES.get(ch.upper())


def vin_check_digit(vin):
    total = 0
    for i, ch in enumerate(vin[:8] + vin[9:]):  # skip position 9
        pass
    # proper loop over all 17 positions with weight, skipping index 8
    total = 0
    for i in range(17):
        if i == 8:
            continue
        v = vin_transliterate(vin[i])
        if v is None:
            return None
        total += v * VIN_WEIGHTS[i]
    rem = total % 11
    return "X" if rem == 10 else str(rem)


def decode_wmi(vin):
    for length in (3, 2):
        wmi = vin[:length]
        if wmi in WMI_DB:
            return WMI_DB[wmi]
    c = vin[0]
    country = (
        "US" if c in "1 4 5".split() or c in "145" else
        "CA" if c == "2" else "MX" if c == "3" else
        "JP" if c == "J" else "KR" if c == "K" else
        "DE" if c == "W" else "FR" if c == "V" else
        "IT" if c == "Z" else "GB" if c == "S" else
        "SE" if c == "Y" else "CN" if c == "L" else
        "IN" if c == "M" else "RU" if c == "X" else
        "BR" if c == "9" else "TR" if c == "N" else "?"
    )
    return (None, country)


def cmd_vin(a):
    vin = (a.vin or "").strip().upper().replace(" ", "")
    if a.action == "validate" or a.action == "decode":
        pass
    print(f"VIN: {vin}")
    if len(vin) != 17:
        print(f"[!] LENGTH: {len(vin)} — VINs are exactly 17 characters (post-1981). REJECT.")
        return 2
    bad = [c for c in vin if c in "IOQ"]
    if bad:
        print(f"[!] FORBIDDEN CHARS: {', '.join(sorted(set(bad)))} — I/O/Q never appear in VINs. REJECT.")
        return 2
    if not all(vin_transliterate(c) is not None for c in vin):
        print("[!] NON-ALPHANUMERIC characters present. REJECT.")
        return 2
    maker, country = decode_wmi(vin)
    year_code = vin[9]
    year = YEAR_CODES.get(year_code)
    year_note = ""
    if year:
        # 30-year cycle: codes repeat; if decoded year > current+1, previous cycle
        if year > dt.date.today().year + 1:
            year -= 30
            year_note = " (cycle-adjusted)"
    plant = vin[10]
    serial = vin[11:]
    print(f"    structure   : 17 chars, no I/O/Q — OK")
    print(f"    WMI {vin[:3]:3}    : {maker or 'unknown maker'} / {country}")
    if year:
        print(f"    year code '{year_code}'    : {year}{year_note}")
    else:
        print(f"    year code '{year_code}'    : not a standard year code")
    print(f"    plant code   : {plant}")
    print(f"    serial       : {serial} ({'low/early — could indicate early production or reorder' if serial.lstrip('0').isdigit() and int(serial.lstrip('0') or 0) < 100 else 'normal range'})")
    cd_expected = vin_check_digit(vin)
    if cd_expected is None:
        print("    check digit  : not computable (unexpected characters)")
        return 1
    if cd_expected == vin[8]:
        print(f"    check digit  : {vin[8]} = computed {cd_expected} — VALID ✓")
        return 0
    print(f"    check digit  : {vin[8]} ≠ computed {cd_expected} — MISMATCH!")
    print("[!] The VIN fails its ISO 3779 check digit. Either the listing has a typo")
    print("    (ask the seller to re-send, photo of the plate) or the plate is")
    print("    counterfeit/cloned. Do not travel, do not pay a deposit.")
    return 2


# ---------------------------------------------------------------- mileage
def mileage_verdict(age_years, km, klass):
    lo, hi, label = CLASS_NORMS[klass]
    per_year = km / age_years if age_years > 0 else km
    if per_year < lo * 0.45:
        v = "SUSPICIOUSLY-LOW"
    elif per_year < lo:
        v = "PLAUSIBLE-LOW"
    elif per_year <= hi:
        v = "PLAUSIBLE"
    elif per_year <= hi * 1.5:
        v = "PLAUSIBLE-HIGH"
    else:
        v = "SUSPICIOUSLY-HIGH"
    return v, per_year, (lo, hi, label)


# ---------------------------------------------------------------- price model
def market_band(year, km, klass):
    age = max(0.0, dt.date.today().year - year + (0.5 if dt.date.today().month > 6 else 0.0))
    base, dep = CLASS_VALUE[klass]
    value = base * ((1 - dep) ** age)
    norm_lo, norm_hi, _ = CLASS_NORMS[klass]
    mid = (norm_lo + norm_hi) / 2
    if km > 0 and age > 0:
        actual = km / age
        if actual > mid:
            # penalty: 6% per 10k km above norm-mid, capped
            value *= max(0.55, 1 - 0.06 * (actual - mid) / 10_000)
        elif actual < mid:
            value *= min(1.12, 1 + 0.04 * (mid - actual) / 10_000)
    lo, hi = value * 0.85, value * 1.15
    return age, lo, value, hi


# ---------------------------------------------------------------- screen
def screen_core(year, km, price, klass, currency="$"):
    today = dt.date.today()
    age_years = max(0.25, today.year - year)
    risks, notes = [], []
    verdict_code = 0

    mv, per_year, (lo, hi, label) = mileage_verdict(age_years, km, klass)
    _, band_lo, band_mid, band_hi = market_band(year, km, klass)

    print(f"LISTING SCREEN — {year} {label}, {km:,} km, asking {currency}{price:,}\n")

    # mileage section
    print(f"[mileage] {per_year:,.0f} km/yr vs class norm {lo:,}–{hi:,}")
    if mv == "SUSPICIOUSLY-LOW":
        print(f"          → {mv}: rollback or 'garage queen' (rot risk: seals, brakes, fluids by time not km)")
        risks.append(("odometer-rollback-suspect", 3))
        notes.append("demand service book with dated stamps; compare pedal/wear to mileage")
    elif mv == "PLAUSIBLE-LOW":
        print(f"          → {mv}: fine if documented; verify service-by-time")
        notes.append("low-mileage claims need documentation — time-based service matters")
    elif mv == "PLAUSIBLE-HIGH":
        print(f"          → {mv}: ask what it did (highway ok, city delivery bad)")
        risks.append(("high-usage", 1))
    elif mv == "SUSPICIOUSLY-HIGH":
        print(f"          → {mv}: fleet/taxi pattern — engine/drivetrain near end-of-service-life budget")
        risks.append(("fleet-expattern", 2))
        notes.append("budget for imminent major maintenance")
    else:
        print(f"          → {mv} ✓")

    # price section
    ratio = price / band_mid if band_mid else 0
    print(f"\n[price] modeled market: {currency}{band_lo:,.0f} – {currency}{band_hi:,.0f} (mid {currency}{band_mid:,.0f})")
    if ratio > 1.30:
        print(f"        asking {ratio:.0%} of modeled mid — way over. Either the seller knows something (rare trim, history) or is fishing.")
        risks.append(("price-far-over-market", 2))
    elif ratio > 1.12:
        print(f"        asking {ratio:.0%} of mid — typical private-listing optimism; negotiate down.")
        risks.append(("price-over-market", 1))
    elif ratio < 0.70:
        print(f"        asking only {ratio:.0%} of modeled mid — TOO GOOD. Suspect scam, salvage/rebuilt title, or hidden major fault.")
        risks.append(("too-cheap-scam-risk", 3))
        notes.append("if it's real, there's a reason; demand title + history before travel")
    elif ratio < 0.88:
        print(f"        asking {ratio:.0%} of mid — below market: motivated seller or known defect. Find out which.")
        risks.append(("under-market-explain-first", 1))
    else:
        print(f"        asking {ratio:.0%} of mid — within normal band.")
    offer_open = int(band_mid * (0.82 if ratio > 1 else 0.92))
    offer_walk = int(band_hi * 0.97)
    print(f"\n[offer]  opening: {currency}{offer_open:,} | walk-away (max): {currency}{offer_walk:,}")

    # age-specific warnings
    if age_years >= 10:
        risks.append(("age-10+", 1)); notes.append("10+ years: budget for rubber/plastic age failures (hoses, bushings, tanks)")
    if age_years >= 15:
        risks.append(("age-15+", 2)); notes.append("15+ years: inspect sills/floor for structural rust — often terminal")
    if 0 < km < 30_000 and age_years >= 6:
        risks.append(("low-km-old-car", 2)); notes.append("old + ultra-low km = time-based decay; verify the mileage story hard")
    if km >= 250_000:
        risks.append(("absolute-km-250k+", 2)); notes.append("250,000+ km: engine/transmission major-service horizon; turbo/injector budget")
    elif km >= 160_000:
        risks.append(("absolute-km-160k+", 1)); notes.append("160,000+ km: suspension, timing, and clutch/DPF items are due-now, not later")

    # verdict
    score = sum(w for _, w in risks)
    if score >= 4 or any(w == 3 for _, w in risks):
        v = "RED"
    elif score >= 2:
        v = "YELLOW"
    else:
        v = "GREEN"
    print(f"\n[risks]  {', '.join(f'{r}({w})' for r, w in risks) or 'none'}")
    print(f"\nVERDICT: {v}")
    if v == "RED":
        print("  Screen-out unless the seller resolves the red flags in writing first.")
    elif v == "YELLOW":
        print("  Worth the trip IF: service book present, VIN photo matches listing, no title brands.")
    else:
        print("  Clean screen. Proceed to viewing with the inspection sheet.")
    if notes:
        print("\n[notes]")
        for n in notes:
            print(f"  - {n}")
    print("\nNext: sentinel.py inspect   |   History report before deposit. Always.")
    return 0 if v != "RED" else 2


def cmd_screen(a):
    if a.klass not in CLASS_NORMS:
        print(f"[!] --class must be one of: {', '.join(CLASS_NORMS)}")
        return 1
    return screen_core(a.year, a.km, a.price, a.klass, a.currency)


def cmd_negotiate(a):
    rc = screen_core(a.year, a.km, a.price, a.klass, a.currency)
    print("\n" + "=" * 60)
    print("NEGOTIATION SHEET")
    print("=" * 60)
    age_years = max(0.25, dt.date.today().year - a.year)
    mv, per_year, (lo, hi, label) = mileage_verdict(age_years, a.km, a.klass)
    _, band_lo, band_mid, band_hi = market_band(a.year, a.km, a.klass)
    print("Objective talking points (calm, factual, printable):")
    pts = []
    if per_year > hi:
        pts.append(f"Usage is {per_year:,.0f} km/yr vs the {lo:,}–{hi:,} class norm — above-average wear on drivetrain and interior.")
    if per_year < lo:
        pts.append(f"Mileage is documented below class norm — service-by-time (fluids, tires, battery age) is due regardless of km.")
    if a.price > band_hi:
        pts.append(f"Asking is above the modeled market band ({a.currency}{band_lo:,.0f}–{a.currency}{band_hi:,.0f}) for year/km/class.")
    if age_years >= 10:
        pts.append(f"{age_years:.0f} years old: rubber components (bushings, hoses, seals) age out by time — inspection findings here are negotiating items, not 'bad luck'.")
    if not pts:
        pts.append("Car screens clean; your leverage is market band + any inspection findings.")
    for i, p in enumerate(pts, 1):
        print(f"  {i}. {p}")
    print("\nRules of engagement:")
    print("  - Never negotiate before inspecting; findings are currency.")
    print(f"  - Open at the modeled opening offer; concede in shrinking steps (400/200/100).")
    print("  - Walk-away is a real number: write it down before you go, don't move it.")
    print("  - A seller who won't put 'no accidents, clean title' in writing is telling you something.")
    return rc


INSPECT_SHEET = """\
30-MINUTE INSPECTION SHEET (print this; check in order)
=========================================================

BEFORE STARTING THE ENGINE (10 min)
[ ] Cold engine — insist it has NOT been warmed up before you arrive
[ ] Oil on dipstick: amber/brown OK; black gritty = skipped changes; milky = head gasket
[ ] Coolant reservoir: green/orange/pink OK; rusty or oily film = trouble
[ ] Under-car: fresh oil/coolant drops, welded crash repairs, rust on sills
[ ] Panel gaps even; paint texture matches panel-to-panel (repaint = repair?)
[ ] Windshield: stars/cracks; all lights intact, no moisture inside
[ ] Tires: brand/date codes (DOT xxxx/YY — older than 6 years = replacement cost)
[ ] Interior wear vs claimed mileage: pedal rubber, steering wheel, seat bolsters
[ ] Under-seat / spare-wheel well: silt line or corrosion = flood car
[ ] Harness connectors under dash: green crust = water history

COLD START (5 min) — the most diagnostic 5 minutes of the visit
[ ] Starts within 2s without smoke burst
[ ] Blue smoke (oil) / persistent white (coolant) / black (fuel) — each is a walk-flag
[ ] First 20s: ticking that fades = normal; knocking = walk away
[ ] Idle smooth after 30s; no Check Engine (ask for OBD-II scan if light on)

TEST DRIVE (15 min) — route must include: rough road, 80+ km/h stretch, full-lock turns
[ ] Acceleration 0–80: no hesitation, no transmission flare or harsh shifts
[ ] Braking from 60: straight, no pulsation (warped rotors), no grinding
[ ] Steering full-lock both directions at low speed: no clunks (CV joints)
[ ] Rough road: no rattles from suspension; car doesn't continue bouncing (dampers)
[ ] 80+ km/h: no vibration (alignment/bearings), tracks straight with light grip
[ ] Upshift and downshift each gear manually if automatic: smooth, instant
[ ] Hill: no overheating trend on temp gauge
[ ] Quiet cabin at 80 — wind noise = panel alignment history

AFTER DRIVE (5 min)
[ ] Let it idle: no smoke, temp stable, no warning lights
[ ] Check under car again: new drops after the drive
[ ] A/C cold; heat hot; all windows, locks, wipers, signals
[ ] OBD-II scan if you brought a $20 reader — pending codes tell stories

PAPERWORK (non-negotiable)
[ ] Title in seller's name (no 'I'm selling for a friend')
[ ] No lien; title brand field blank (salvage/rebuilt/flood = walk or huge discount)
[ ] VIN on dash/door stamp/title matches EXACTLY (validate: sentinel.py vin decode)
[ ] Service book with dated stamps consistent with mileage
[ ] Two keys; original toolkit; manual

ECONOMICS
- Independent pre-purchase inspection ($100–200): mandatory for YELLOW/RED cars
- History report (Carfax/Autocode/local): mandatory before ANY deposit
- Deposit only after inspection, in writing, refundability stated
"""


def cmd_inspect(a):
    print(INSPECT_SHEET)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("vin", help="validate/decode a VIN")
    p.add_argument("action", choices=["decode", "validate"])
    p.add_argument("vin")
    p.set_defaults(fn=cmd_vin)

    p = sub.add_parser("screen", help="full listing screen: mileage, price band, verdict")
    p.add_argument("--year", type=int, required=True)
    p.add_argument("--km", type=int, required=True)
    p.add_argument("--price", type=int, required=True)
    p.add_argument("--class", dest="klass", default="compact", choices=list(CLASS_NORMS))
    p.add_argument("--currency", default="$")
    p.set_defaults(fn=cmd_screen)

    p = sub.add_parser("negotiate", help="screen + negotiation talking points")
    p.add_argument("--year", type=int, required=True)
    p.add_argument("--km", type=int, required=True)
    p.add_argument("--price", type=int, required=True)
    p.add_argument("--class", dest="klass", default="compact", choices=list(CLASS_NORMS))
    p.add_argument("--currency", default="$")
    p.set_defaults(fn=cmd_negotiate)

    p = sub.add_parser("inspect", help="print the 30-minute inspection sheet")
    p.set_defaults(fn=cmd_inspect)

    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
