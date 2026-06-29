#!/usr/bin/env python3
import argparse
import math

REQUIRED_INPUTS = {
    "H1": ("K", "WS", "L", "theta", "H2"),
    "L": ("K", "WS", "H1", "H2", "theta"),
    "WS": ("K", "L", "H1", "H2", "theta"),
    "theta": ("K", "WS", "L", "H1", "H2"),
    "K": ("L", "WS", "H1", "H2", "theta"),
    "H2": ("K", "WS", "L", "theta", "H1"),
}

def td(x):
    return math.tan(math.radians(x))

def default_length_precision(unit):
    normalized = unit.strip().lower()
    if normalized in ("mm", "millimeter", "millimeters"):
        return 0
    if normalized in ("cm", "centimeter", "centimeters"):
        return 1
    if normalized in ("m", "meter", "meters"):
        return 3
    return 2

def fmt(value, precision):
    return f"{value:.{precision}f}"

def validate_inputs(parser, a):
    if a.W is not None and a.W <= 0:
        parser.error("--W must be greater than 0")

    if a.precision is not None and a.precision < 0:
        parser.error("--precision must be 0 or greater")

    if a.angle_precision < 0:
        parser.error("--angle-precision must be 0 or greater")

    if a.WS is None and a.W is not None and a.solve != "WS":
        a.WS = a.W / 2

    for name in REQUIRED_INPUTS[a.solve]:
        if getattr(a, name) is None:
            if name == "WS":
                parser.error(f"--WS is required when --solve {a.solve}, or provide --W to assume a centered drain")
            parser.error(f"--{name} is required when --solve {a.solve}")

    if a.solve != "theta" and not (0 < a.theta < 90):
        parser.error("--theta must be greater than 0 and less than 90 degrees for forward flow")

    if a.W is not None and a.WS is not None and a.solve != "WS" and not (0 < a.WS < a.W):
        parser.error("--WS must be greater than 0 and less than --W")

    if a.solve == "theta" and a.H1 + a.H2 <= 0:
        parser.error("H1 + H2 must be greater than 0 when solving theta")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--solve", required=True, choices=["H1","L","WS","theta","K","H2"])
    for name in ["K","W","WS","H1","H2","L","theta"]:
        p.add_argument(f"--{name}", type=float)
    p.add_argument("--unit", default="cm")
    p.add_argument("--precision", type=int, help="Decimal places for length outputs. Defaults to metric-friendly precision based on --unit.")
    p.add_argument("--angle-precision", type=int, default=1, help="Decimal places for angle outputs. Default: 1.")
    a = p.parse_args()

    validate_inputs(p, a)
    length_precision = a.precision if a.precision is not None else default_length_precision(a.unit)

    target = a.solve
    if target == "H1":
        result = (a.K + a.WS - a.L) / td(a.theta) - a.H2
    elif target == "L":
        result = a.K + a.WS - (a.H1 + a.H2) * td(a.theta)
    elif target == "WS":
        result = a.L - a.K + (a.H1 + a.H2) * td(a.theta)
    elif target == "theta":
        result = math.degrees(math.atan2(a.K + a.WS - a.L, a.H1 + a.H2))
    elif target == "K":
        result = a.L - a.WS + (a.H1 + a.H2) * td(a.theta)
    else:
        result = (a.K + a.WS - a.L) / td(a.theta) - a.H1

    setattr(a, target, result)
    suffix = "degrees" if target == "theta" else a.unit
    result_precision = a.angle_precision if target == "theta" else length_precision
    print(f"{target} = {fmt(result, result_precision)} {suffix}")

    horizontal_offset = None
    vertical_drop = None
    if a.K is not None and a.WS is not None and a.L is not None:
        horizontal_offset = a.K + a.WS - a.L
        print(f"horizontal_offset = {fmt(horizontal_offset, length_precision)} {a.unit}")
    if a.H1 is not None and a.H2 is not None:
        vertical_drop = a.H1 + a.H2
        print(f"vertical_drop = {fmt(vertical_drop, length_precision)} {a.unit}")
    if horizontal_offset is not None and vertical_drop is not None and vertical_drop != 0:
        reverse_theta = math.degrees(math.atan2(horizontal_offset, vertical_drop))
        print(f"reverse_theta = {fmt(reverse_theta, a.angle_precision)} degrees")
    if a.W is not None and a.WS is not None:
        print(f"drain_center_offset = {fmt(a.WS - a.W/2, length_precision)} {a.unit}")

    warnings = []
    if a.H1 is not None and a.H1 < 0:
        warnings.append("H1 is negative; check reference levels or geometry")
    if horizontal_offset is not None and horizontal_offset < 0:
        warnings.append("horizontal offset is negative; the target lies behind the outlet")
    if vertical_drop is not None and vertical_drop <= 0:
        warnings.append("vertical drop is not positive; check H1 and H2")
    if a.W is not None and a.WS is not None and not (0 < a.WS < a.W):
        warnings.append("WS is outside the basin width W")
    for warning in warnings:
        print(f"warning: {warning}")

if __name__ == "__main__":
    main()
