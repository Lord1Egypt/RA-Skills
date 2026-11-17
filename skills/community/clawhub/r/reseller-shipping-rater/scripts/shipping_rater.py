#!/usr/bin/env python3
"""reseller-shipping-rater — dimensional weight, flat-rate fit, cubic eligibility,
and listing-profit math for online sellers. Stdlib only.

Retail-rate bands are 2025-26-era ESTIMATES for decision support; always confirm
the winning service's live price in the platform label flow before purchase.

Subcommands: rate, flatrate, profit, --demo
"""
import argparse

UPS_DIV = 139
USPS_DIV = 166

# Approx retail Ground/Advantage-ish price bands $/lb by zone (ESTIMATES)
USPS_GA = {1: 0.95, 2: 1.05, 3: 1.15, 4: 1.28, 5: 1.42, 6: 1.55, 7: 1.68, 8: 1.82}
UPS_GND = {1: 1.15, 2: 1.28, 3: 1.42, 4: 1.58, 5: 1.75, 6: 1.92, 7: 2.10, 8: 2.30}

FLAT_RATE = {  # sku: (price, interior L,W,H in)
    "FR Envelope": (7.9, 12.5, 9.5, 0.5),
    "Small FR Box": (10.4, 10.0, 7.0, 4.75),
    "Medium FR Box 1 (top)": (17.6, 11.0, 8.5, 5.5),
    "Medium FR Box 2 (side)": (17.6, 14.0, 12.0, 3.5),
    "Large FR Box": (23.9, 12.25, 12.25, 6.0),
}
# cubic Ground Advantage tiers: volume cu-ft -> base price by zone (T1-T5 band avg)
CUBIC_TIERS = [(0.10, 5.1, 8.6), (0.20, 5.6, 9.5), (0.30, 6.1, 10.3),
               (0.40, 6.7, 11.4), (0.50, 7.4, 12.6)]  # (max cuft, z1, z8 price)


def dim_weight(dims, divisor):
    l, w, h = dims
    return (l * w * h) / divisor


def cubic_price(cu_ft, zone):
    for i, (cap, z1, z8) in enumerate(CUBIC_TIERS, 1):
        if cu_ft <= cap:
            t = (zone - 1) / 7
            return i, z1 + (z8 - z1) * t
    return None, None


def price_est(service, billable_lb, zone):
    if service == "USPS Ground Adv":
        return 6.40 + USPS_GA[zone] * max(1, billable_lb - 1)
    if service == "UPS Ground":
        return 9.20 + UPS_GND[zone] * max(1, billable_lb - 1)
    return None


def parse_dims(s):
    l, w, h = (float(x) for x in s.split(","))
    return l, w, h


def cmd_rate(a) -> None:
    dims = parse_dims(a.dims)
    vol_cf = (dims[0] * dims[1] * dims[2]) / 1728
    du = dim_weight(dims, UPS_DIV)
    dz = dim_weight(dims, USPS_DIV) if vol_cf > 1.0 else 0
    print("=== DIMENSIONAL WEIGHT ANALYSIS (ESTIMATE model)\n")
    print(f"Box: {dims[0]:.0f}x{dims[1]:.0f}x{dims[2]:.0f} in  "
          f"({vol_cf:.2f} cu ft), actual {a.weight:.1f} lb, zone {a.zone}")
    print(f"UPS/FedEx dim weight (139): {du:.1f} lb -> billable {max(du, a.weight):.1f}")
    if vol_cf > 1.0:
        print(f"USPS dim weight (166, >1 cuft applies): {dz:.1f} lb -> billable {max(dz, a.weight):.1f}")
    else:
        print("USPS: under 1 cu ft -> dim pricing not applied, billable = actual")
    cub, cp = cubic_price(vol_cf, a.zone) if vol_cf <= 0.5 else (None, None)
    print("\n--- Service estimates (retail-band ESTIMATES, verify live) ---")
    rows = []
    rows.append(("USPS Ground Adv", max(dz if vol_cf > 1 else 0, a.weight)))
    rows.append(("UPS Ground", max(du, a.weight)))
    for svc, lb in sorted(rows, key=lambda r: price_est(r[0], r[1], a.zone) or 1e9):
        p = price_est(svc, lb, a.zone)
        print(f"  {svc:<20} billable {lb:>5.1f} lb   ~${p:6.2f}")
    if cp is not None:
        print(f"  USPS GA CUBIC T{cub:<12} <0.5 cuft        ~${cp:6.2f}  <-- often the winner")
        print(f"  (Cubic eligible: {vol_cf:.2f} cuft <= 0.5, weight <= 20 lb: "
              f"{'YES' if a.weight <= 20 else 'NO (over 20 lb)'})")
    else:
        print(f"  (Cubic NOT eligible: {vol_cf:.2f} cuft > 0.5 — box DOWN 1-2 inches if close)")
    print("\nRule: light-but-large (dim >> actual) -> smallest box or poly bag;")
    print("      dense -> flat-rate candidates; small -> cubic tier.")


def cmd_flatrate(a) -> None:
    dims = parse_dims(a.dims)
    print("=== FLAT-RATE FIT TEST (USPS)\n")
    print(f"Item/box: {dims[0]:.0f}x{dims[1]:.0f}x{dims[2]:.0f} in, {a.weight:.1f} lb, zone {a.zone}\n")
    any_fit = False
    for sku, (price, L, W, H) in FLAT_RATE.items():
        s = sorted(dims, reverse=True)
        b = sorted((L, W, H), reverse=True)
        fits = s[0] <= b[0] and s[1] <= b[1] and s[2] <= b[2] and a.weight <= 70
        mark = "FITS " if fits else "no   "
        if fits:
            any_fit = True
        print(f"  [{mark}] {sku:<24} ${price:>5.2f} any zone")
    gnd = price_est("USPS Ground Adv", a.weight, a.zone)
    if any_fit:
        cheapest_fr = min(p for sku, (p, L, W, H) in FLAT_RATE.items()
                          if sorted(dims, reverse=True)[0] <= sorted((L, W, H), reverse=True)[0]
                          and sorted(dims, reverse=True)[1] <= sorted((L, W, H), reverse=True)[1]
                          and sorted(dims, reverse=True)[2] <= sorted((L, W, H), reverse=True)[2])
        verdict = ("FLAT-RATE WINS" if cheapest_fr <= gnd and a.zone >= 5
                   else "COMPARE: flat-rate vs ~${:.2f} weight-based; flat-rate "
                        "shines zone 5+ or 10+ lb".format(gnd))
        print(f"\nWeight-based Ground Adv est: ~${gnd:.2f}")
        print(f"Cheapest fitting flat rate:   ${cheapest_fr:.2f}")
        print(f"VERDICT: {verdict}")
    else:
        print(f"\nNo flat-rate box fits (or over 70 lb). Weight-based est ~${gnd:.2f}.")
    print("\nGotchas: padded FR is its own SKU; 'Flat Rate' branding = that tier only;")
    print("media rate (books/media ONLY) undercuts everything for eligible content.")


def cmd_profit(a) -> None:
    dims = parse_dims(a.dims)
    vol_cf = (dims[0] * dims[1] * dims[2]) / 1728
    du = dim_weight(dims, UPS_DIV)
    dz = dim_weight(dims, USPS_DIV) if vol_cf > 1.0 else 0
    billable = max(min(du if vol_cf > 1 else a.weight, 1e9), a.weight)
    # choose best estimate among GA weight, UPS dim, cubic
    cands = [price_est("USPS Ground Adv", max(dz, a.weight) if vol_cf > 1 else a.weight, a.zone),
             price_est("UPS Ground", max(du, a.weight), a.zone)]
    cub, cp = cubic_price(vol_cf, a.zone) if vol_cf <= 0.5 else (None, None)
    if cp:
        cands.append(cp)
    label = min(cands)
    gross = a.sold + a.ship_charged
    fee = gross * a.fee_pct
    net = gross - fee - label - a.packaging - a.cost_goods
    print("=== LISTING PROFIT AUTOPSY\n")
    print(f"Sold price:            ${a.sold:>8.2f}")
    print(f"Shipping charged:      ${a.ship_charged:>8.2f}")
    print(f"Gross (fee base!):     ${gross:>8.2f}")
    print(f"Platform fee ({a.fee_pct*100:.2f}%):     -${fee:>7.2f}")
    print(f"Label (best est):      -${label:>7.2f}   (billable {billable:.1f} lb)")
    print(f"Packaging:             -${a.packaging:>7.2f}")
    print(f"Cost of goods:         -${a.cost_goods:>7.2f}")
    print(f"{'-'*34}")
    print(f"NET PROFIT:            ${net:>8.2f}  ({net/gross*100 if gross else 0:.1f}% of gross)")
    if net < 0:
        print("\nVERDICT: LOSS — raise price, cut box size (cubic tier), or pickup-only.")
    elif net / gross < 0.15:
        print("\nVERDICT: THIN — under 15% margin; the next fee hike eats you.")
    else:
        print("\nVERDICT: HEALTHY margin. Ship it.")
    print("\nReminder: fees apply to SHIPPING money too — 'free shipping' is not free.")


def run_demo() -> None:
    import types
    print("######## DEMO 1: the light-big trap (plush in a big box) ########\n")
    cmd_rate(types.SimpleNamespace(dims="18,14,12", weight=2.5, zone=4, value=30))
    print("\n######## DEMO 2: dense books cross-country ########\n")
    cmd_flatrate(types.SimpleNamespace(dims="12,9,4", weight=9, zone=8))
    print("\n######## DEMO 3: margin autopsy on a $60 sale ########\n")
    cmd_profit(types.SimpleNamespace(sold=60, ship_charged=9, dims="14,10,6",
                                     weight=3, zone=4, cost_goods=18,
                                     packaging=1.2, fee_pct=0.1325))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd")
    r = sub.add_parser("rate")
    r.add_argument("--dims", required=True, help="L,W,H inches of the PACKED box")
    r.add_argument("--weight", type=float, required=True)
    r.add_argument("--zone", type=int, default=4, choices=range(1, 9))
    r.add_argument("--value", type=float, default=0)
    f = sub.add_parser("flatrate")
    f.add_argument("--dims", required=True)
    f.add_argument("--weight", type=float, required=True)
    f.add_argument("--zone", type=int, default=5, choices=range(1, 9))
    pr = sub.add_parser("profit")
    pr.add_argument("--sold", type=float, required=True)
    pr.add_argument("--ship-charged", type=float, default=0)
    pr.add_argument("--dims", required=True)
    pr.add_argument("--weight", type=float, required=True)
    pr.add_argument("--zone", type=int, default=4, choices=range(1, 9))
    pr.add_argument("--cost-goods", type=float, default=0)
    pr.add_argument("--packaging", type=float, default=0.8)
    pr.add_argument("--fee-pct", type=float, default=0.1325)
    p.add_argument("--demo", action="store_true")
    a = p.parse_args()
    if a.demo:
        run_demo()
    elif a.cmd == "rate":
        cmd_rate(a)
    elif a.cmd == "flatrate":
        cmd_flatrate(a)
    elif a.cmd == "profit":
        cmd_profit(a)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
