#!/usr/bin/env python3
"""TV size / viewing distance planner.

Exact 16:9 angular geometry (SMPTE 30-deg reference, THX 40-deg cinematic),
resolution-acuity distances (1 arc-minute/pixel: 1080p at 1.56x diag, 4K at
0.78x), size-band recommendations by content mix, price-per-square-inch
comparisons, and projector lumens/throw math. Stdlib only.
"""
import argparse
import math
import sys

W_FACTOR = 0.8716  # 16:9 width / diagonal
H_FACTOR = 0.4903  # 16:9 height / diagonal
ARCMIN = math.radians(1.0) / 60.0  # 20/20 acuity: 1 arcmin per resolvable line pair element


def width_ft(diag):  # diag in inches -> width in feet
    return diag * W_FACTOR / 12.0


def angle_deg(diag, dist_ft):
    w = width_ft(diag)
    return 2 * math.degrees(math.atan((w / 2) / dist_ft))


def diag_for_angle(angle_deg, dist_ft):
    w = 2 * dist_ft * math.tan(math.radians(angle_deg) / 2)
    return w * 12.0 / W_FACTOR


def acuity_distance(diag, horiz_pixels):
    """Distance (ft) at which one pixel subtends 1 arc-minute."""
    px_width_in = diag * W_FACTOR / horiz_pixels
    return (px_width_in / 12.0) / (2 * math.tan(ARCMIN / 2))


def area_sqin(diag):
    return diag * W_FACTOR * diag * H_FACTOR


def cmd_recommend(a):
    d = a.distance
    use = a.use
    lo_angle = {"movies": 34, "mixed": 30, "sports": 28, "monitor": 45}[use]
    hi_angle = {"movies": 45, "mixed": 40, "sports": 36, "monitor": 55}[use]
    lo = diag_for_angle(lo_angle, d)
    hi = diag_for_angle(hi_angle, d)
    print(f"seat distance {d} ft, primary use: {use}")
    print(f"SMPTE 30° reference → {diag_for_angle(30, d):.0f}\" | THX 40° cinematic → "
          f"{diag_for_angle(40, d):.0f}\"")
    print(f"recommended band for {use}: {lo:.0f}\"–{hi:.0f}\" "
          f"(round to the nearest shelf size)")
    shelf = [43, 50, 55, 58, 65, 70, 75, 77, 83, 85, 90, 98]
    in_band = [s for s in shelf if lo - 4 <= s <= hi + 4]
    if in_band:
        print("shelf sizes in/near band:", ", ".join(f'{s}"' for s in in_band))
        for s in in_band:
            ang = angle_deg(s, d)
            d4k = acuity_distance(s, 3840)
            d1080 = acuity_distance(s, 1920)
            res = "4K VISIBLE" if d <= d1080 else "4K WASTED at this distance"
            print(f'  {s}" → {ang:.1f}° | 4K beats 1080p inside {d1080:.1f} ft → {res}; '
                  f'8K needs < {d4k:.1f} ft (not a couch)')
    if a.current:
        ang = angle_deg(a.current, d)
        if ang < lo_angle - 4:
            v = f"UNDERSIZED for {use}"
        elif ang < lo_angle:
            v = f"SMALL SIDE of the {use} band"
        elif ang <= hi_angle:
            v = "IN BAND"
        else:
            v = "IMMERSIVE (fine for movies; check mount/tilt)"
        print(f'\ncurrent TV {a.current}" → {ang:.1f}° → {v}')
        if ang < lo_angle:
            print(f'  free upgrade: couch at {(a.current / 12.0) * 1.62:.1f} ft gives SMPTE 30° '
                  f'(currently {d} ft)')
    print("\nreminders: measure eye-to-PANEL (mount setback ~1 ft); center at seated "
          "eye height ~40\"; showroom walls sit you at 0.8x diagonal - re-anchor.")


def cmd_resolution(a):
    d = a.distance
    a1080 = acuity_distance(a.diagonal, 1920)
    a4k = acuity_distance(a.diagonal, 3840)
    print(f'{a.diagonal}" at {d} ft (20/20 vision, 1 arc-min/pixel):')
    print(f"  1080p pixels visible inside {a1080:.1f} ft; 4K pixels inside {a4k:.1f} ft")
    if d < a4k:
        v = "even 4K shows pixels this close — 8K ACTUALLY VISIBLE (rare)"
    elif d < a1080:
        v = f"4K VISIBLE over 1080p (1080p pixels start to show inside {a1080:.1f} ft)"
    else:
        v = f"4K WASTED: beyond {a1080:.1f} ft even 1080p pixels are invisible — resolution premium is $0"
    print(f"  verdict: {v}")


def cmd_compare(a):
    d = a.distance
    print(f'price-per-square-inch of image (distance {d} ft):')
    rows = []
    for spec in a.sizes:
        diag_s, price_s = spec.split(":")
        diag, price = float(diag_s), float(price_s)
        ang = angle_deg(diag, d)
        ar = area_sqin(diag)
        rows.append((diag, price, ang, ar, price / ar))
    for diag, price, ang, ar, ppi in rows:
        print(f'  {diag:.0f}"  ${price:,.0f}  {ar:,.0f} sq in  {ang:.1f}°  '
              f'${ppi:.2f}/sq in')
    if len(rows) >= 2:
        (d1, p1, _, a1, _), (d2, p2, _, a2, _) = rows[0], rows[-1]
        gained = a2 - a1
        dp = p2 - p1
        print(f'\nupgrade {d1:.0f}"→{d2:.0f}": +{gained:,.0f} sq in '
              f'({gained / a1:+.0%} image), +${dp:,.0f} → ${dp / gained:.2f} per ADDED sq in')
        print("note: area grows with the square of diagonal - 65→77 is +40% image, not +18%")


def cmd_projector(a):
    diag = a.screen
    w_in = diag * W_FACTOR
    h_in = diag * H_FACTOR
    area_sqft = (w_in * h_in) / 144.0
    target_fl = {"sdr": 16, "hdr": 40, "sports": 60}[a.mode]
    lumen_need = target_fl * area_sqft / a.gain
    throw = a.throw_ratio * w_in / 12.0
    print(f'{diag}" 16:9 screen: {w_in:.0f} × {h_in:.0f} in = {area_sqft:.1f} sq ft, gain {a.gain}')
    print(f'target brightness {target_fl} fL ({a.mode}) → projector needs ≈ '
          f'{lumen_need:,.0f} lumens (after-lens honest spec; "marketing lumens" run hot)')
    print(f'throw ratio {a.throw_ratio} → mount at ≈ {throw:.1f} ft from screen')
    if a.ambient:
        print(f'ambient light {a.ambient} fL of wash: image contrast drops to roughly '
              f'{target_fl / (target_fl + a.ambient):.0%} of dark-room contrast — '
              f'curtains/alighting beat more lumens')
        if a.ambient > 5:
            print("VERDICT: no consumer projector survives direct sun (~50+ fL wash). "
                  "Control the light first, buy lumens second.")
    print(f'4K acuity: sit inside {acuity_distance(diag, 3840):.1f} ft for full 4K benefit')


def cmd_demo(_):
    print("=== couch 8.5 ft, movies ===\n")
    cmd_recommend(argparse.Namespace(distance=8.5, use="movies", current=None))
    print("\n=== current 55\" check at same distance ===\n")
    cmd_recommend(argparse.Namespace(distance=8.5, use="movies", current=55))
    print("\n=== 65\" at 9 ft: is 4K worth it? ===\n")
    cmd_resolution(argparse.Namespace(diagonal=65, distance=9))
    print("\n=== 65:1099 vs 77:2199 at 10 ft ===\n")
    cmd_compare(argparse.Namespace(sizes=["65:1099", "77:2199"], distance=10))
    print("\n=== 120\" projector, gain 1.0, HDR, some ambient 3 fL ===\n")
    cmd_projector(argparse.Namespace(screen=120, gain=1.0, mode="hdr",
                                     throw_ratio=1.2, ambient=3.0))


def main():
    argv = sys.argv[1:]
    if argv and argv[0] == "--demo":
        cmd_demo(None)
        return 0
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("recommend", help="size band for a distance + use")
    r.add_argument("--distance", type=float, required=True, help="eye-to-screen ft")
    r.add_argument("--use", choices=["movies", "mixed", "sports", "monitor"], default="mixed")
    r.add_argument("--current", type=float, help="current TV diagonal for a verdict")
    r.set_defaults(func=cmd_recommend)

    v = sub.add_parser("resolution", help="acuity check")
    v.add_argument("--diagonal", type=float, required=True)
    v.add_argument("--distance", type=float, required=True)
    v.set_defaults(func=cmd_resolution)

    c = sub.add_parser("compare", help="price per square inch")
    c.add_argument("--sizes", nargs="+", required=True, help='DIAG:PRICE e.g. 65:1099 77:2199')
    c.add_argument("--distance", type=float, default=9.0)
    c.set_defaults(func=cmd_compare)

    pj = sub.add_parser("projector", help="lumens, gain, throw")
    pj.add_argument("--screen", type=float, required=True, help="diagonal in")
    pj.add_argument("--gain", type=float, default=1.0)
    pj.add_argument("--mode", choices=["sdr", "hdr", "sports"], default="sdr")
    pj.add_argument("--throw-ratio", type=float, default=1.2)
    pj.add_argument("--ambient", type=float, default=0, help="ambient wash fL")
    pj.set_defaults(func=cmd_projector)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
