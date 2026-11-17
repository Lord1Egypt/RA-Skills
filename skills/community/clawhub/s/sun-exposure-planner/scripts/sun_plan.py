#!/usr/bin/env python3
"""sun_plan.py — sun exposure planner: time-to-burn by skin type, vitamin D
windows, realistic sunscreen math, hour-by-hour day plans from solar geometry.
Stdlib only.

Examples:
  python3 sun_plan.py --uv 8 --skin 2
  python3 sun_plan.py --lat 37.97 --date 08-05 --skin 2 --spf 30 --plan
  python3 sun_plan.py --lat 59.33 --date 03-15 --skin 3   # Stockholm in March
"""
import argparse
import math
from datetime import date

# Fitzpatrick: name, MED J/m^2, description
SKINS = {
    1: (200, "always burns, never tans (pale, freckles)"),
    2: (250, "burns easily, tans poorly"),
    3: (300, "sometimes burns, gradually tans"),
    4: (400, "rarely burns, tans well"),
    5: (500, "very rarely burns"),
    6: (800, "almost never burns"),
}


def solar_declination(d: date) -> float:
    day = d.timetuple().tm_yday
    return math.radians(23.44) * math.sin(math.radians(360 / 365 * (day - 81)))


def solar_elevation(lat_deg, hour_local_solar, d: date):
    lat = math.radians(lat_deg)
    decl = solar_declination(d)
    H = math.radians(15 * (hour_local_solar - 12))
    sin_elev = math.sin(lat) * math.sin(decl) + math.cos(lat) * math.cos(decl) * math.cos(H)
    return math.degrees(math.asin(max(-1, min(1, sin_elev))))


def clearsky_uvi(elev_deg, altitude_m=0):
    """Published approximation: clear-sky UVI ~ 12.5 * cos(SZA)^2.42 at sea level,
    typical ozone (~300 DU). Valid within ~±0.5 UVI for elevations > ~20°."""
    if elev_deg <= 0:
        return 0.0
    mu = math.sin(math.radians(elev_deg))  # cos(zenith) = sin(elevation)
    uvi = 12.5 * (mu ** 2.42)
    return uvi * (1 + 0.10 * altitude_m / 1000)


def burn_minutes(uvi, skin_type):
    if uvi <= 0:
        return None
    med = SKINS[skin_type][0]
    return med / (0.025 * uvi) / 60.0


def fmt_min(m):
    if m is None:
        return "—"
    if m >= 90:
        return f"{m / 60:.1f} h"
    return f"{m:.0f} min"


def main():
    p = argparse.ArgumentParser(description="Sun exposure planner.")
    p.add_argument("--uv", type=float, help="forecast UV index (overrides model)")
    p.add_argument("--lat", type=float, help="latitude for model UV")
    p.add_argument("--date", type=str, help="MM-DD (default today)")
    p.add_argument("--skin", type=int, required=True, choices=range(1, 7))
    p.add_argument("--spf", type=int, default=None)
    p.add_argument("--altitude", type=int, default=0)
    p.add_argument("--cloud", choices=["clear", "thin", "broken", "overcast", "heavy"],
                   default="clear")
    p.add_argument("--reflect", choices=["grass", "sand", "water", "snow"], default="grass")
    p.add_argument("--plan", action="store_true", help="hour-by-hour table 8-18h")
    p.add_argument("--tz-offset", type=float, default=0.0,
                   help="hours east of solar meridian (clock - solar); DST=+1")
    a = p.parse_args()

    cloud_f = {"clear": 1.0, "thin": 0.7, "broken": 0.5, "overcast": 0.3, "heavy": 0.15}[a.cloud]
    reflect_f = {"grass": 1.0, "sand": 1.15, "water": 1.2, "snow": 1.8}[a.reflect]
    med = SKINS[a.skin][0]

    def env_uvi(uvi):
        return uvi * cloud_f * reflect_f

    if a.uv is not None:
        uv = env_uvi(a.uv)
        print(f"UVI {a.uv} (forecast) × cloud {cloud_f} × reflect {reflect_f} = {uv:.1f} effective")
        bm = burn_minutes(uv, a.skin)
        print(f"Skin type {a.skin} ({SKINS[a.skin][1]}), MED {med} J/m²")
        print(f"Time to burn, unprotected: {fmt_min(bm)}")
        if a.spf:
            real = max(1.0, a.spf * 0.4)
            print(f"SPF {a.spf} realistic (~40% of label = {real:.0f}×): "
                  f"{fmt_min(bm * real if bm else None)}  — reapply cap 2 h")
        if uv >= 3:
            quarter = (burn_minutes(uv, a.skin) or 0) / 4
            print(f"Vitamin D: UV ≥ 3 ✓ — ~{fmt_min(quarter)} to ¼ MED (hands/face/arms), "
                  f"saturation ~20-30 min")
        else:
            print("Vitamin D: UV < 3 — no meaningful cutaneous synthesis today")
        return

    if a.lat is None:
        p.error("need --uv or --lat")
    d = date.today()
    if a.date:
        mm, dd = a.date.split("-")
        d = date(d.year, int(mm), int(dd))

    print(f"{'h':>4} {'elev':>6} {'UVI':>6} {'burn':>9} {'vitD ¼MED':>9}")
    for h in range(8, 19):
        hsolar = h - a.tz_offset
        e = solar_elevation(a.lat, hsolar, d)
        u = clearsky_uvi(e, a.altitude)
        ue = env_uvi(u)
        bm = burn_minutes(ue, a.skin)
        vd = fmt_min(bm / 4) if (bm and ue >= 3) else "—"
        print(f"{h:>4} {e:>5.0f}° {ue:>6.1f} {fmt_min(bm):>9} {vd:>9}")
    print(f"\n(skin {a.skin}: {SKINS[a.skin][1]}; altitude {a.altitude} m; "
          f"cloud {a.cloud}; surface {a.reflect})")
    noon_e = solar_elevation(a.lat, 12, d)
    print(f"Solar noon elevation {noon_e:.0f}° — {'HIGH BURN WINDOW' if noon_e > 45 else 'moderate'}"
          f" — shadow rule: {'shadow < you ⇒ seek shade 11-15' if noon_e > 45 else 'long shadows, low UVB'}")


if __name__ == "__main__":
    main()
