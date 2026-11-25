#!/usr/bin/env python3
"""Windshield frost forecaster: will glass frost tonight?

Physics (references/frost-physics.md):
  Radiative depression  dT = (1 - 0.85*cloud) * 5.5C * 1/(1 + wind/1.5)
  Glass minimum         Tg = Tmin_air - dT
  FROST  iff Tg <= 0 AND Tg <= Tdew (moisture available)
  HARD FROST at Tg <= -4C
  Parked car holds ~+2C warm-mass bonus decaying with tau=40min.

Pure stdlib. RH is converted to dew point (Magnus) when given instead of Tdew.
"""
import argparse
import json
import math

TAU_MIN = 40.0          # warm-mass decay constant, minutes
WARM_BONUS_C = 2.0      # glass runs this much warmer right after parking


def rh_to_tdew(t, rh):
    """Magnus approximation, t in °C."""
    a, b = 17.62, 243.12
    gamma = math.log(max(rh, 1) / 100.0) + (a * t) / (b + t)
    return (b * gamma) / (a - gamma)


def glass_delta(cloud_frac, wind_ms):
    """Radiative depression below air temperature, °C."""
    sky = 1.0 - 0.85 * cloud_frac
    wind_f = 1.0 / (1.0 + wind_ms / 1.5)
    return 5.5 * sky * wind_f


def classify(tg, tdew):
    if tg <= -4 and tg <= tdew + 2:      # thick glaze: deep cold + some moisture
        return "HARD FROST"
    if tg <= 0 and tg <= tdew:
        return "FROST"
    if tg <= tdew:                        # condensation above freezing
        return "DEW (no ice)"
    return "NONE"


def tactics(klass):
    t = {
        "NONE": ["Clean or dew beads only. Wipe/wipers if damp. Nothing to prep."],
        "DEW (no ice)": [
            "Water beads, no ice: wipers or a squeegee pass in the morning.",
            "No cover needed; lifting wipers optional (keeps rubber off cold wet glass).",
        ],
        "FROST": [
            "COVER TONIGHT: frost shield / towel / cardboard over windshield, weighed down. Saves a 5-10 min scrape.",
            "Cover on DRY glass in the evening - covering after dew falls can freeze the cover on.",
            "Lift wiper arms off the glass.",
            "Morning: defrost 5-10 min + scraper. 2:1 water:isopropyl spray melts the film.",
        ],
        "HARD FROST": [
            "COVER TONIGHT, non-negotiable (thick glaze otherwise). Towel/cardboard/frost shield + weights.",
            "Lift wipers; they will freeze into the glaze otherwise and tear when switched on.",
            "Morning: start engine + full defrost 10-15 min BEFORE scraping; budget +15 min.",
            "NEVER pour hot water (thermal shock cracks glass). Lukewarm <=30C or de-icer only.",
            "De-icer: 2:1 water:IPA(>=70%) along the edges first, then center. Salt brine corrods trim - avoid.",
        ],
    }
    return t[klass]


def main():
    ap = argparse.ArgumentParser(description="Will the windshield frost tonight?")
    ap.add_argument("--tmin", type=float, required=True, help="overnight min air temp, °C")
    ap.add_argument("--tdew", type=float, default=None, help="dew point, °C (or use --rh)")
    ap.add_argument("--rh", type=float, default=None, help="overnight RH %% (converted to dew point)")
    ap.add_argument("--wind", type=float, default=2.0, help="mean wind speed, m/s (default 2)")
    ap.add_argument("--cloud", type=float, default=30.0, help="mean cloud cover, %% (default 30)")
    ap.add_argument("--hours", type=int, default=0,
                    help="print parked-car glass curve for N hours")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.tdew is None and a.rh is None:
        ap.error("give --tdew or --rh")
    tdew = a.tdew if a.tdew is not None else rh_to_tdew(a.tmin, a.rh)
    cloud_frac = min(max(a.cloud, 0), 100) / 100.0
    d = glass_delta(cloud_frac, a.wind)
    tg = a.tmin - d
    klass = classify(tg, tdew)

    out = {
        "air_min_c": a.tmin,
        "dew_point_c": round(tdew, 1),
        "radiative_depression_c": round(d, 2),
        "glass_min_c": round(tg, 1),
        "verdict": klass,
        "why": (f"glass min {tg:.1f}°C vs 0°C and dew point {tdew:.1f}°C "
                f"(cloud {a.cloud:.0f}% wind {a.wind:.1f} m/s)"),
        "tactics": tactics(klass),
    }

    if a.hours > 0:
        curve = []
        crossed = None
        for h in range(1, a.hours + 1):
            bonus = WARM_BONUS_C * math.exp(-(h * 60.0) / TAU_MIN)
            # air temp eases toward the overnight min by hour 4
            air = a.tmin + 3.0 * max(0.0, 1 - h / 4.0)          # ~3C above min early
            g = air - d + bonus
            curve.append({"hour": h, "air_c": round(air, 1), "glass_c": round(g, 1),
                          "frost_now": bool(g <= 0 and g <= tdew)})
            if crossed is None and g <= 0 and g <= tdew:
                crossed = h
        out["parked_curve"] = curve
        out["first_frost_hour"] = crossed

    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print(f"Tonight: air min {a.tmin:+.1f}°C, dew point {tdew:+.1f}°C, "
          f"cloud {a.cloud:.0f}%, wind {a.wind:.1f} m/s")
    print(f"Radiative depression: {d:.1f}°C -> glass minimum {tg:+.1f}°C")
    print(f"VERDICT: {klass}")
    print(f"  ({out['why']})")
    if a.hours > 0:
        print(f"\nParked-car glass curve (warm-mass decay included):")
        for row in out["parked_curve"]:
            mark = "  <= FROST" if row["frost_now"] else ""
            print(f"  hour {row['hour']:>2}: air {row['air_c']:+5.1f}  glass {row['glass_c']:+5.1f}{mark}")
        if out["first_frost_hour"]:
            print(f"  First frost-forming hour: {out['first_frost_hour']}")
        else:
            print("  Glass never crosses the frost line during the window.")
    print("\nTactics:")
    for i, t in enumerate(out["tactics"], 1):
        print(f"{i}. {t}")


if __name__ == "__main__":
    main()
