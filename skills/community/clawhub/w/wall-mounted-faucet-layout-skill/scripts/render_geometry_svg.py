#!/usr/bin/env python3
import argparse
import math
from html import escape
from pathlib import Path

from faucet_geometry import default_length_precision, fmt, td, validate_inputs


def solve(args):
    if args.solve == "H1":
        return (args.K + args.WS - args.L) / td(args.theta) - args.H2
    if args.solve == "L":
        return args.K + args.WS - (args.H1 + args.H2) * td(args.theta)
    if args.solve == "WS":
        return args.L - args.K + (args.H1 + args.H2) * td(args.theta)
    if args.solve == "theta":
        return math.degrees(math.atan2(args.K + args.WS - args.L, args.H1 + args.H2))
    if args.solve == "K":
        return args.L - args.WS + (args.H1 + args.H2) * td(args.theta)
    return (args.K + args.WS - args.L) / td(args.theta) - args.H1


def add_args(parser):
    parser.add_argument("--solve", required=True, choices=["H1", "L", "WS", "theta", "K", "H2"])
    for name in ["K", "W", "WS", "H1", "H2", "L", "theta"]:
        parser.add_argument(f"--{name}", type=float)
    parser.add_argument("--unit", default="cm")
    parser.add_argument("--precision", type=int, help="Decimal places for length outputs. Defaults to metric-friendly precision based on --unit.")
    parser.add_argument("--angle-precision", type=int, default=1, help="Decimal places for angle outputs. Default: 1.")


def line(label, x1, y1, x2, y2, color, text_x, text_y, value, anchor="start"):
    return f"""
  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="3"
        marker-start="url(#arrow-start-{color[1:]})" marker-end="url(#arrow-end-{color[1:]})"/>
  <text x="{text_x:.1f}" y="{text_y:.1f}" class="label" fill="{color}" text-anchor="{anchor}">{escape(label)} = {escape(value)}</text>"""


def marker_defs():
    markers = []
    for color in ["#1f5fae", "#17863b", "#c62828", "#6a3dbb", "#d97706", "#9a5a00"]:
        cid = color[1:]
        markers.append(f"""
    <marker id="arrow-end-{cid}" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 z" fill="{color}"/>
    </marker>
    <marker id="arrow-start-{cid}" markerWidth="10" markerHeight="10" refX="1" refY="3" orient="auto">
      <path d="M7,0 L7,6 L0,3 z" fill="{color}"/>
    </marker>""")
    return "\n".join(markers)


def render_svg(args):
    result = solve(args)
    setattr(args, args.solve, result)

    if args.H1 + args.H2 <= 0:
        raise ValueError("H1 + H2 must be greater than 0 to render the diagram")

    length_precision = args.precision if args.precision is not None else default_length_precision(args.unit)
    angle_precision = args.angle_precision
    unit = args.unit
    target_precision = angle_precision if args.solve == "theta" else length_precision
    target_unit = "degrees" if args.solve == "theta" else unit

    drain_x_model = args.K + args.WS
    front_width = args.W if args.W is not None else max(args.WS * 1.8, args.WS + abs(drain_x_model - args.L), args.WS + 10)
    front_x_model = args.K + front_width
    max_x_model = max(front_x_model, args.L, drain_x_model, args.K, 1)

    left = 110
    right = 1010
    scale_x = (right - left) / max_x_model

    def sx(value):
        return left + value * scale_x

    wall_x = sx(0)
    rear_x = sx(args.K)
    outlet_x = sx(args.L)
    drain_x = sx(drain_x_model)
    front_x = sx(front_x_model)

    outlet_y = 230
    drain_y = 760
    scale_y = (drain_y - outlet_y) / (args.H1 + args.H2)
    rim_y = outlet_y + args.H1 * scale_y

    h_offset = drain_x_model - args.L
    v_drop = args.H1 + args.H2
    reverse_theta = math.degrees(math.atan2(h_offset, v_drop))
    center_offset = None if args.W is None else args.WS - args.W / 2

    length = lambda value: f"{fmt(value, length_precision)} {unit}"
    angle = lambda value: f"{fmt(value, angle_precision)} degrees"

    w_dimension = ""
    if args.W is not None:
        w_dimension = line("W", rear_x, 840, front_x, 840, "#6a3dbb", (rear_x + front_x) / 2 - 18, 825, length(args.W))

    center_offset_row = ""
    if center_offset is not None:
        center_offset_row = f"<text x=\"1190\" y=\"682\" class=\"small\">drain center offset = {escape(length(center_offset))}</text>"

    target_value = f"{args.solve} = {fmt(result, target_precision)} {target_unit}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1700" height="980" viewBox="0 0 1700 980">
  <defs>
    <style>
      .title {{ font: 700 32px Arial, sans-serif; fill:#111; }}
      .subtitle {{ font: 700 22px Arial, sans-serif; fill:#111; }}
      .body {{ font: 18px Arial, sans-serif; fill:#222; }}
      .small {{ font: 16px Arial, sans-serif; fill:#333; }}
      .label {{ font: 700 20px Arial, sans-serif; }}
      .formula {{ font: 700 25px "Times New Roman", serif; fill:#111; }}
      .guide {{ stroke:#777; stroke-width:1.5; stroke-dasharray:7 6; }}
      .wall {{ fill:#777; }}
      .counter {{ fill:#b9b9b9; }}
      .basin {{ fill:#fafafa; stroke:#222; stroke-width:4; }}
      .spout {{ fill:none; stroke:#444; stroke-width:24; stroke-linecap:round; stroke-linejoin:round; }}
      .water {{ fill:none; stroke:#2d86e8; stroke-width:12; stroke-linecap:round; }}
      .drain {{ fill:#222; stroke:#111; stroke-width:2; }}
      .panel {{ fill:#fff; stroke:#aaa; stroke-width:2; rx:18; }}
      .highlight {{ fill:#f7fbff; stroke:#6ea8fe; stroke-width:2; rx:16; }}
    </style>
{marker_defs()}
  </defs>

  <rect width="1700" height="980" fill="white"/>
  <text x="50" y="48" class="title">Wall-mounted faucet layout result</text>
  <text x="50" y="82" class="small">Custom geometry diagram generated from the supplied dimensions.</text>

  <text x="50" y="125" class="subtitle">SIDE VIEW</text>
  <rect x="{wall_x - 16:.1f}" y="150" width="32" height="650" class="wall"/>
  <rect x="{wall_x:.1f}" y="{drain_y:.1f}" width="{front_x - wall_x + 60:.1f}" height="34" class="counter"/>

  <path d="M{wall_x + 17:.1f} {outlet_y - 65:.1f} L{max(outlet_x - 130, wall_x + 70):.1f} {outlet_y - 65:.1f} Q{outlet_x - 45:.1f} {outlet_y - 65:.1f} {outlet_x:.1f} {outlet_y:.1f}" class="spout"/>
  <circle cx="{outlet_x:.1f}" cy="{outlet_y:.1f}" r="8" fill="#333"/>

  <path d="M{rear_x:.1f} {rim_y:.1f} L{front_x:.1f} {rim_y:.1f}
           C{front_x - 10:.1f} {rim_y + 110:.1f} {front_x - 55:.1f} {drain_y - 40:.1f} {drain_x + 120:.1f} {drain_y:.1f}
           L{drain_x - 170:.1f} {drain_y:.1f}
           C{rear_x + 80:.1f} {drain_y - 45:.1f} {rear_x + 15:.1f} {rim_y + 115:.1f} {rear_x:.1f} {rim_y:.1f} Z" class="basin"/>
  <ellipse cx="{drain_x:.1f}" cy="{drain_y:.1f}" rx="32" ry="13" class="drain"/>
  <path d="M{outlet_x:.1f} {outlet_y:.1f} L{drain_x:.1f} {drain_y:.1f}" class="water"/>

  <line x1="{wall_x:.1f}" y1="145" x2="{wall_x:.1f}" y2="820" class="guide"/>
  <line x1="{rear_x:.1f}" y1="145" x2="{rear_x:.1f}" y2="820" class="guide"/>
  <line x1="{outlet_x:.1f}" y1="145" x2="{outlet_x:.1f}" y2="820" class="guide"/>
  <line x1="{drain_x:.1f}" y1="145" x2="{drain_x:.1f}" y2="820" class="guide"/>
  <line x1="{front_x:.1f}" y1="145" x2="{front_x:.1f}" y2="820" class="guide"/>
  <line x1="{max(rear_x - 30, 60):.1f}" y1="{rim_y:.1f}" x2="1100" y2="{rim_y:.1f}" class="guide"/>
  <line x1="{drain_x - 35:.1f}" y1="{drain_y:.1f}" x2="1100" y2="{drain_y:.1f}" class="guide"/>
  <line x1="{outlet_x:.1f}" y1="{outlet_y:.1f}" x2="1100" y2="{outlet_y:.1f}" class="guide"/>

{line("L", wall_x, 170, outlet_x, 170, "#c62828", (wall_x + outlet_x) / 2 - 35, 158, length(args.L))}
{line("K", wall_x, 235, rear_x, 235, "#1f5fae", (wall_x + rear_x) / 2 - 35, 223, length(args.K))}
{line("WS", rear_x, 300, drain_x, 300, "#17863b", (rear_x + drain_x) / 2 - 42, 288, length(args.WS))}
{line("dx", outlet_x, rim_y - 42, drain_x, rim_y - 42, "#1f5fae", (outlet_x + drain_x) / 2 - 70, rim_y - 52, length(h_offset))}
{w_dimension}
{line("H1", 1065, outlet_y, 1065, rim_y, "#d97706", 1045, (outlet_y + rim_y) / 2, length(args.H1), "end")}
{line("H2", 1065, rim_y, 1065, drain_y, "#9a5a00", 1045, (rim_y + drain_y) / 2, length(args.H2), "end")}

  <text x="{outlet_x + 24:.1f}" y="{outlet_y + 65:.1f}" class="label" fill="#1f5fae">theta = {escape(angle(args.theta))}</text>
  <text x="920" y="{outlet_y - 10:.1f}" class="small">outlet level</text>
  <text x="920" y="{rim_y - 10:.1f}" class="small">basin rim level</text>
  <text x="920" y="{drain_y - 10:.1f}" class="small">drain target level</text>

  <rect x="1150" y="95" width="500" height="180" class="highlight"/>
  <text x="1180" y="135" class="subtitle">Solved result</text>
  <text x="1180" y="182" class="formula">{escape(target_value)}</text>
  <text x="1180" y="225" class="small">Use this value for faucet selection or install checks.</text>

  <rect x="1150" y="305" width="500" height="180" class="panel"/>
  <text x="1180" y="345" class="subtitle">Core relationship</text>
  <text x="1195" y="400" class="formula">tan theta = (K + WS - L) / (H1 + H2)</text>
  <text x="1180" y="438" class="small">dx = {escape(length(h_offset))}; vertical drop = {escape(length(v_drop))}</text>

  <rect x="1150" y="515" width="500" height="210" class="panel"/>
  <text x="1180" y="555" class="subtitle">Validation values</text>
  <text x="1190" y="602" class="small">reverse theta = {escape(angle(reverse_theta))}</text>
  <text x="1190" y="642" class="small">target point x = K + WS = {escape(length(drain_x_model))}</text>
  {center_offset_row}

  <rect x="50" y="895" width="1040" height="58" class="highlight"/>
  <text x="75" y="930" class="body">This is a straight-line geometric estimate. Confirm final placement with an on-site water-flow test.</text>
</svg>
"""
    return svg


def main():
    parser = argparse.ArgumentParser(description="Render a custom annotated SVG for wall-mounted faucet geometry.")
    add_args(parser)
    parser.add_argument("--output", required=True, help="Output SVG path")
    args = parser.parse_args()
    validate_inputs(parser, args)

    svg = render_svg(args)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
