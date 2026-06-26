#!/usr/bin/env bash
# shadow/scripts/script.sh — CSS Shadow Effect Generator
# Version: 1.0.0
# Data: ~/.shadow/data.jsonl
set -euo pipefail

VERSION="1.0.0"
DATA_DIR="$HOME/.shadow"
DATA_FILE="$DATA_DIR/data.jsonl"

mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

# ─── usage ───────────────────────────────────────────────────────────────────
usage() {
  cat <<'EOF'
shadow — CSS Shadow Effect Generator v1.0.0

Usage:
  script.sh <command> [options]

Commands:
  box       Generate a CSS box-shadow value
  text      Generate a CSS text-shadow value
  drop      Generate a CSS drop-shadow filter value
  inset     Generate an inset box-shadow value
  layer     Combine multiple shadows into a layered effect
  preset    List or apply built-in shadow presets
  random    Generate a random shadow effect
  animate   Generate CSS animation keyframes for shadow transitions
  export    Export saved shadows to CSS, JSON, or SCSS
  preview   Preview a shadow as ASCII art or HTML
  help      Show this help message
  version   Show version

Run 'script.sh <command> --help' for details on each command.
EOF
}

# ─── main dispatch ───────────────────────────────────────────────────────────
CMD="${1:-help}"
shift || true

case "$CMD" in
  box|text|drop|inset|layer|preset|random|animate|export|preview)
    python3 - "$CMD" "$@" << 'PYEOF'
#!/usr/bin/env python3
"""shadow — CSS Shadow Effect Generator (Python core)"""

import sys
import os
import json
import random
import datetime
import argparse
import colorsys
import re

VERSION = "1.0.0"
DATA_DIR = os.path.expanduser("~/.shadow")
DATA_FILE = os.path.join(DATA_DIR, "data.jsonl")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    open(DATA_FILE, "a").close()

# ── helpers ──────────────────────────────────────────────────────────────────

def load_all():
    """Load all shadow records from data.jsonl."""
    records = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return records


def save_record(record):
    """Append a shadow record to data.jsonl, replacing if same name exists."""
    records = load_all()
    records = [r for r in records if r.get("name") != record.get("name")]
    records.append(record)
    with open(DATA_FILE, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def find_record(name):
    """Find a record by name."""
    for r in load_all():
        if r.get("name") == name:
            return r
    return None


def timestamp():
    return datetime.datetime.utcnow().isoformat() + "Z"


def parse_color(c):
    """Return a valid CSS color string."""
    if c is None:
        return "rgba(0,0,0,0.2)"
    return c


# ── shadow value builders ────────────────────────────────────────────────────

def build_box_shadow(x=0, y=4, blur=8, spread=0, color="rgba(0,0,0,0.2)", inset=False):
    parts = []
    if inset:
        parts.append("inset")
    parts.extend([f"{x}px", f"{y}px", f"{blur}px", f"{spread}px", color])
    return " ".join(parts)


def build_text_shadow(x=1, y=1, blur=2, color="#333"):
    return f"{x}px {y}px {blur}px {color}"


def build_drop_shadow(x=0, y=4, blur=8, color="rgba(0,0,0,0.3)"):
    return f"drop-shadow({x}px {y}px {blur}px {color})"


# ── presets ──────────────────────────────────────────────────────────────────

PRESETS = {
    "material-1": {
        "type": "box",
        "css": "0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)",
        "description": "Material Design elevation 1",
    },
    "material-2": {
        "type": "box",
        "css": "0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)",
        "description": "Material Design elevation 2",
    },
    "material-3": {
        "type": "box",
        "css": "0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)",
        "description": "Material Design elevation 3",
    },
    "material-4": {
        "type": "box",
        "css": "0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)",
        "description": "Material Design elevation 4",
    },
    "material-5": {
        "type": "box",
        "css": "0 19px 38px rgba(0,0,0,0.30), 0 15px 12px rgba(0,0,0,0.22)",
        "description": "Material Design elevation 5",
    },
    "neumorphism": {
        "type": "box",
        "css": "8px 8px 16px rgba(0,0,0,0.1), -8px -8px 16px rgba(255,255,255,0.7)",
        "description": "Soft UI neumorphic effect",
    },
    "flat": {
        "type": "box",
        "css": "0 1px 2px rgba(0,0,0,0.1)",
        "description": "Minimal flat shadow",
    },
    "elevated": {
        "type": "box",
        "css": "0 20px 60px rgba(0,0,0,0.3), 0 8px 20px rgba(0,0,0,0.15)",
        "description": "Strong elevation effect",
    },
    "glow": {
        "type": "box",
        "css": "0 0 20px rgba(98,0,238,0.4), 0 0 60px rgba(98,0,238,0.2)",
        "description": "Colored glow effect",
    },
}


# ── command handlers ─────────────────────────────────────────────────────────

def cmd_box(args):
    parser = argparse.ArgumentParser(prog="shadow box", description="Generate CSS box-shadow")
    parser.add_argument("--x", type=int, default=0, help="Horizontal offset (px)")
    parser.add_argument("--y", type=int, default=4, help="Vertical offset (px)")
    parser.add_argument("--blur", type=int, default=8, help="Blur radius (px)")
    parser.add_argument("--spread", type=int, default=0, help="Spread radius (px)")
    parser.add_argument("--color", type=str, default="rgba(0,0,0,0.2)", help="Shadow color")
    parser.add_argument("--name", type=str, default=None, help="Name for this shadow")
    parser.add_argument("--save", action="store_true", help="Save to data file")
    opts = parser.parse_args(args)

    css_value = build_box_shadow(opts.x, opts.y, opts.blur, opts.spread, opts.color)
    name = opts.name or f"box-{opts.x}-{opts.y}-{opts.blur}"

    record = {
        "name": name,
        "type": "box",
        "params": {"x": opts.x, "y": opts.y, "blur": opts.blur, "spread": opts.spread, "color": opts.color},
        "css_property": "box-shadow",
        "css_value": css_value,
        "created_at": timestamp(),
    }

    print(f"box-shadow: {css_value};")
    print(f"Name: {name}")

    if opts.save:
        save_record(record)
        print(f"✅ Saved to {DATA_FILE}")


def cmd_text(args):
    parser = argparse.ArgumentParser(prog="shadow text", description="Generate CSS text-shadow")
    parser.add_argument("--x", type=int, default=1, help="Horizontal offset (px)")
    parser.add_argument("--y", type=int, default=1, help="Vertical offset (px)")
    parser.add_argument("--blur", type=int, default=2, help="Blur radius (px)")
    parser.add_argument("--color", type=str, default="#333", help="Shadow color")
    parser.add_argument("--name", type=str, default=None, help="Name for this shadow")
    parser.add_argument("--save", action="store_true", help="Save to data file")
    opts = parser.parse_args(args)

    css_value = build_text_shadow(opts.x, opts.y, opts.blur, opts.color)
    name = opts.name or f"text-{opts.x}-{opts.y}-{opts.blur}"

    record = {
        "name": name,
        "type": "text",
        "params": {"x": opts.x, "y": opts.y, "blur": opts.blur, "color": opts.color},
        "css_property": "text-shadow",
        "css_value": css_value,
        "created_at": timestamp(),
    }

    print(f"text-shadow: {css_value};")
    print(f"Name: {name}")

    if opts.save:
        save_record(record)
        print(f"✅ Saved to {DATA_FILE}")


def cmd_drop(args):
    parser = argparse.ArgumentParser(prog="shadow drop", description="Generate CSS drop-shadow filter")
    parser.add_argument("--x", type=int, default=0, help="Horizontal offset (px)")
    parser.add_argument("--y", type=int, default=4, help="Vertical offset (px)")
    parser.add_argument("--blur", type=int, default=8, help="Blur radius (px)")
    parser.add_argument("--color", type=str, default="rgba(0,0,0,0.3)", help="Shadow color")
    parser.add_argument("--name", type=str, default=None, help="Name for this shadow")
    parser.add_argument("--save", action="store_true", help="Save to data file")
    opts = parser.parse_args(args)

    css_value = build_drop_shadow(opts.x, opts.y, opts.blur, opts.color)
    name = opts.name or f"drop-{opts.x}-{opts.y}-{opts.blur}"

    record = {
        "name": name,
        "type": "drop",
        "params": {"x": opts.x, "y": opts.y, "blur": opts.blur, "color": opts.color},
        "css_property": "filter",
        "css_value": css_value,
        "created_at": timestamp(),
    }

    print(f"filter: {css_value};")
    print(f"Name: {name}")

    if opts.save:
        save_record(record)
        print(f"✅ Saved to {DATA_FILE}")


def cmd_inset(args):
    parser = argparse.ArgumentParser(prog="shadow inset", description="Generate inset box-shadow")
    parser.add_argument("--x", type=int, default=0, help="Horizontal offset (px)")
    parser.add_argument("--y", type=int, default=2, help="Vertical offset (px)")
    parser.add_argument("--blur", type=int, default=4, help="Blur radius (px)")
    parser.add_argument("--spread", type=int, default=0, help="Spread radius (px)")
    parser.add_argument("--color", type=str, default="rgba(0,0,0,0.1)", help="Shadow color")
    parser.add_argument("--name", type=str, default=None, help="Name for this shadow")
    parser.add_argument("--save", action="store_true", help="Save to data file")
    opts = parser.parse_args(args)

    css_value = build_box_shadow(opts.x, opts.y, opts.blur, opts.spread, opts.color, inset=True)
    name = opts.name or f"inset-{opts.x}-{opts.y}-{opts.blur}"

    record = {
        "name": name,
        "type": "inset",
        "params": {"x": opts.x, "y": opts.y, "blur": opts.blur, "spread": opts.spread, "color": opts.color},
        "css_property": "box-shadow",
        "css_value": css_value,
        "created_at": timestamp(),
    }

    print(f"box-shadow: {css_value};")
    print(f"Name: {name}")

    if opts.save:
        save_record(record)
        print(f"✅ Saved to {DATA_FILE}")


def cmd_layer(args):
    parser = argparse.ArgumentParser(prog="shadow layer", description="Combine multiple shadows")
    parser.add_argument("shadows", nargs="+", help="Names of shadows to combine")
    parser.add_argument("--name", type=str, default=None, help="Name for the layered shadow")
    parser.add_argument("--save", action="store_true", help="Save to data file")
    opts = parser.parse_args(args)

    shadow_names = opts.shadows
    found = []
    for sn in shadow_names:
        rec = find_record(sn)
        if rec is None:
            print(f"❌ Shadow '{sn}' not found. Save it first.")
            sys.exit(1)
        found.append(rec)

    # only box-shadow and inset types can be layered directly
    css_parts = []
    for rec in found:
        css_parts.append(rec["css_value"])

    combined = ", ".join(css_parts)
    name = opts.name or "layered-" + "-".join(shadow_names)

    record = {
        "name": name,
        "type": "layer",
        "layers": shadow_names,
        "css_property": "box-shadow",
        "css_value": combined,
        "created_at": timestamp(),
    }

    print(f"box-shadow: {combined};")
    print(f"Name: {name}")
    print(f"Layers: {', '.join(shadow_names)}")

    if opts.save:
        save_record(record)
        print(f"✅ Saved to {DATA_FILE}")


def cmd_preset(args):
    parser = argparse.ArgumentParser(prog="shadow preset", description="List or apply presets")
    parser.add_argument("action", nargs="?", default="list", choices=["list", "apply"])
    parser.add_argument("--name", type=str, default=None, help="Preset name")
    parser.add_argument("--save", action="store_true", help="Save applied preset")
    opts = parser.parse_args(args)

    if opts.action == "list":
        print("Available presets:")
        print(f"{'Name':<20} {'Description'}")
        print("-" * 60)
        for pname, pdata in PRESETS.items():
            print(f"{pname:<20} {pdata['description']}")
        return

    # apply
    if not opts.name:
        print("❌ --name is required for apply")
        sys.exit(1)

    if opts.name not in PRESETS:
        print(f"❌ Unknown preset: {opts.name}")
        print(f"Available: {', '.join(PRESETS.keys())}")
        sys.exit(1)

    preset = PRESETS[opts.name]
    print(f"box-shadow: {preset['css']};")
    print(f"/* {preset['description']} */")

    if opts.save:
        record = {
            "name": opts.name,
            "type": preset["type"],
            "params": {"preset": opts.name},
            "css_property": "box-shadow",
            "css_value": preset["css"],
            "created_at": timestamp(),
        }
        save_record(record)
        print(f"✅ Saved preset '{opts.name}' to {DATA_FILE}")


def cmd_random(args):
    parser = argparse.ArgumentParser(prog="shadow random", description="Generate random shadow")
    parser.add_argument("--type", dest="shadow_type", choices=["box", "text", "drop"], default="box")
    parser.add_argument("--layers", type=str, default="1", help="Number of layers, e.g. '1-3'")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--name", type=str, default=None)
    opts = parser.parse_args(args)

    # parse layers range
    if "-" in opts.layers:
        lo, hi = opts.layers.split("-")
        num_layers = random.randint(int(lo), int(hi))
    else:
        num_layers = int(opts.layers)

    def rand_color():
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        a = round(random.uniform(0.1, 0.5), 2)
        return f"rgba({r},{g},{b},{a})"

    parts = []
    for _ in range(max(1, num_layers)):
        x = random.randint(-20, 20)
        y = random.randint(-20, 20)
        blur = random.randint(0, 40)
        spread = random.randint(-5, 15)
        color = rand_color()

        if opts.shadow_type == "box":
            parts.append(build_box_shadow(x, y, blur, spread, color))
        elif opts.shadow_type == "text":
            parts.append(build_text_shadow(x, y, blur, color))
        elif opts.shadow_type == "drop":
            parts.append(build_drop_shadow(x, y, blur, color))

    css_value = ", ".join(parts)
    name = opts.name or f"random-{opts.shadow_type}-{random.randint(1000,9999)}"

    prop_map = {"box": "box-shadow", "text": "text-shadow", "drop": "filter"}
    css_property = prop_map.get(opts.shadow_type, "box-shadow")

    record = {
        "name": name,
        "type": opts.shadow_type,
        "params": {"random": True, "layers": num_layers},
        "css_property": css_property,
        "css_value": css_value,
        "created_at": timestamp(),
    }

    print(f"{css_property}: {css_value};")
    print(f"Name: {name}")
    print(f"Layers: {num_layers}")

    if opts.save:
        save_record(record)
        print(f"✅ Saved to {DATA_FILE}")


def cmd_animate(args):
    parser = argparse.ArgumentParser(prog="shadow animate", description="Generate CSS animation keyframes")
    parser.add_argument("shadow_from", help="Starting shadow name")
    parser.add_argument("shadow_to", help="Ending shadow name")
    parser.add_argument("--duration", type=str, default="0.3s", help="Animation duration")
    parser.add_argument("--name", type=str, default=None, help="Animation name")
    opts = parser.parse_args(args)

    rec_from = find_record(opts.shadow_from)
    rec_to = find_record(opts.shadow_to)

    if not rec_from:
        print(f"❌ Shadow '{opts.shadow_from}' not found.")
        sys.exit(1)
    if not rec_to:
        print(f"❌ Shadow '{opts.shadow_to}' not found.")
        sys.exit(1)

    anim_name = opts.name or f"shadow-{opts.shadow_from}-to-{opts.shadow_to}"
    prop = rec_from.get("css_property", "box-shadow")

    css = f"""@keyframes {anim_name} {{
  0% {{
    {prop}: {rec_from['css_value']};
  }}
  100% {{
    {prop}: {rec_to['css_value']};
  }}
}}

.{anim_name} {{
  animation: {anim_name} {opts.duration} ease-in-out;
}}

/* Hover usage example */
.shadow-hover {{
  {prop}: {rec_from['css_value']};
  transition: {prop} {opts.duration} ease-in-out;
}}
.shadow-hover:hover {{
  {prop}: {rec_to['css_value']};
}}"""

    print(css)
    print(f"\n/* Animation: {anim_name} | Duration: {opts.duration} */")


def cmd_export(args):
    parser = argparse.ArgumentParser(prog="shadow export", description="Export shadows")
    parser.add_argument("--format", choices=["css", "json", "scss"], default="css")
    parser.add_argument("--name", type=str, default=None, help="Export specific shadow")
    parser.add_argument("--all", action="store_true", help="Export all shadows")
    opts = parser.parse_args(args)

    records = load_all()
    if opts.name:
        records = [r for r in records if r.get("name") == opts.name]
    if not records:
        print("❌ No shadows found to export.")
        sys.exit(1)

    if opts.format == "css":
        print(":root {")
        for r in records:
            safe = r["name"].replace(" ", "-")
            print(f"  --shadow-{safe}: {r['css_value']};")
        print("}")
        print()
        for r in records:
            safe = r["name"].replace(" ", "-")
            prop = r.get("css_property", "box-shadow")
            print(f".shadow-{safe} {{")
            print(f"  {prop}: {r['css_value']};")
            print("}")
    elif opts.format == "scss":
        for r in records:
            safe = r["name"].replace(" ", "-")
            print(f"$shadow-{safe}: {r['css_value']};")
        print()
        for r in records:
            safe = r["name"].replace(" ", "-")
            prop = r.get("css_property", "box-shadow")
            print(f".shadow-{safe} {{")
            print(f"  {prop}: $shadow-{safe};")
            print("}")
    elif opts.format == "json":
        output = []
        for r in records:
            output.append({
                "name": r["name"],
                "type": r.get("type", "box"),
                "css_property": r.get("css_property", "box-shadow"),
                "css_value": r["css_value"],
            })
        print(json.dumps(output, indent=2))


def cmd_preview(args):
    parser = argparse.ArgumentParser(prog="shadow preview", description="Preview a shadow")
    parser.add_argument("shadow_name", help="Name of shadow to preview")
    parser.add_argument("--html", action="store_true", help="Generate HTML preview")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    opts = parser.parse_args(args)

    rec = find_record(opts.shadow_name)
    if not rec:
        print(f"❌ Shadow '{opts.shadow_name}' not found.")
        sys.exit(1)

    prop = rec.get("css_property", "box-shadow")
    val = rec["css_value"]

    if opts.html:
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shadow Preview: {rec['name']}</title>
  <style>
    body {{
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: #f0f0f0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      margin: 0;
      flex-direction: column;
      gap: 24px;
    }}
    .preview-card {{
      width: 280px;
      height: 180px;
      background: #ffffff;
      border-radius: 12px;
      {prop}: {val};
      display: flex;
      align-items: center;
      justify-content: center;
      color: #666;
      font-size: 14px;
    }}
    .css-code {{
      background: #1e1e1e;
      color: #d4d4d4;
      padding: 16px 24px;
      border-radius: 8px;
      font-family: 'Courier New', monospace;
      font-size: 13px;
      white-space: pre;
    }}
    h2 {{ color: #333; margin: 0; }}
  </style>
</head>
<body>
  <h2>{rec['name']}</h2>
  <div class="preview-card">Shadow Preview</div>
  <div class="css-code">{prop}: {val};</div>
</body>
</html>"""

        if opts.output:
            with open(opts.output, "w") as f:
                f.write(html_content)
            print(f"✅ HTML preview written to {opts.output}")
        else:
            print(html_content)
    else:
        # ASCII art preview
        print(f"┌─────────────────────────────┐")
        print(f"│                             │")
        print(f"│     Shadow: {rec['name']:<15}│")
        print(f"│     Type:   {rec.get('type','?'):<15}│")
        print(f"│                             │")
        print(f"└─────────────────────────────┘")
        print(f"  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
        print(f"   ░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
        print()
        print(f"{prop}: {val};")


# ── dispatch ─────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Missing command.")
        sys.exit(1)

    cmd = sys.argv[1]
    rest = sys.argv[2:]

    dispatch = {
        "box": cmd_box,
        "text": cmd_text,
        "drop": cmd_drop,
        "inset": cmd_inset,
        "layer": cmd_layer,
        "preset": cmd_preset,
        "random": cmd_random,
        "animate": cmd_animate,
        "export": cmd_export,
        "preview": cmd_preview,
    }

    handler = dispatch.get(cmd)
    if handler:
        handler(rest)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
PYEOF
    ;;

  help)
    usage
    ;;

  version)
    echo "shadow v${VERSION}"
    ;;

  *)
    echo "❌ Unknown command: $CMD"
    echo "Run 'script.sh help' for usage."
    exit 1
    ;;
esac
