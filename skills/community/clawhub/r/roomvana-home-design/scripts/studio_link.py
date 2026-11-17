#!/usr/bin/env python3
"""Roomvana studio link builder — standard library only, no API key.

    python3 studio_link.py list
    python3 studio_link.py link --room bedroom --style japandi
    python3 studio_link.py link --room living-room --mode stage --style scandinavian
    python3 studio_link.py link --room kitchen --mode surface --surface cabinets --finish sage-green
    python3 studio_link.py link --room exterior --mode surface --surface siding --finish navy-blue
    python3 studio_link.py catalog-md      # regenerates references/catalog.md

Every id is checked against Roomvana's live catalog (GET
https://api.roomvana.co/options, public, no auth), so a link never names a room,
style or finish the studio can't render. The combination rules mirror what the
studio itself accepts from a URL (roomvana.ai/design reads ?room= &mode=
&surface= &style= once on load).
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://api.roomvana.co/options"
STUDIO = "https://roomvana.ai/design"
# Lets Roomvana see that a visit came from this skill. Not personal data.
REF = "agent-skill"

# Human-readable labels. /options returns ids only; an id missing here still
# works, it just gets a title-cased label.
STYLE_LABELS = {
    "modern": "clean lines, uncluttered surfaces, neutral palette with bold accents",
    "minimalist": "essential furniture only, calm neutral tones, hidden storage",
    "scandinavian": "light woods, white walls, cozy textiles, functional simplicity",
    "japandi": "Japanese-Scandinavian fusion, warm woods, low-profile furniture, serene neutrals",
    "mid-century-modern": "walnut and teak furniture, organic curves, retro accents",
    "industrial": "exposed brick and metal, dark tones, raw finishes",
    "bohemian": "layered patterns and textures, plants, warm eclectic decor",
    "modern-farmhouse": "shiplap accents, warm woods, black fixtures, rustic-meets-clean",
    "coastal": "airy whites and blues, natural fibers, beach-house freshness",
    "traditional": "classic furniture silhouettes, rich woods, elegant symmetry",
    "contemporary": "current-day polish, mixed materials, comfortable sophistication",
    "rustic": "reclaimed wood, stone textures, warm cabin comfort",
    "french-country": "soft pastels, carved wood, linen fabrics, Provencal charm",
    "mediterranean": "terracotta, wrought iron, warm plaster walls, arched details",
    "art-deco": "geometric patterns, brass and velvet, glamorous jewel tones",
    "modern-luxury": "marble, brass details, statement lighting, hotel-suite polish",
    "vintage": "curated second-hand furniture, nostalgic colors, timeless character",
    "dark-academia": "moody deep tones, wood paneling, library-inspired warmth",
    "tropical": "lush green plants, rattan and bamboo, resort-like brightness",
    "cottagecore": "floral patterns, soft vintage furniture, whimsical countryside coziness",
    "transitional": "traditional silhouettes with contemporary lines, soft neutral palette",
    "spanish-colonial-revival": "white stucco, dark carved wood beams, terracotta tile, arched openings",
    "2026-trends": "organic curved furniture, earthy color-drenched walls, sculptural lighting",
}
ROOM_LABELS = {
    "living-room": "living room", "dining-room": "dining room", "home-office": "home office",
    "kids-room": "kids' room", "attic": "attic bedroom", "laundry-room": "laundry room",
    "closet": "walk-in closet", "home-theater": "home theater", "home-gym": "home gym",
    "wine-cellar": "wine cellar", "basement-bar": "basement bar",
    "staircase": "staircase and stairwell", "exterior": "house exterior (facade)",
    "landscape": "yard and surrounding landscape", "patio": "patio and outdoor seating area",
}

MODES = ("redesign", "stage", "declutter", "surface")


def label(id_, table=None):
    if table and id_ in table:
        return table[id_]
    return id_.replace("-", " ")


def fetch_catalog():
    req = urllib.request.Request(API, headers={"User-Agent": "roomvana-agent-skill"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)
    except Exception as e:  # network-less sandbox, outage, …
        sys.exit(
            f"Could not reach {API} ({e}).\n"
            "Use the bundled snapshot in references/catalog.md instead and build the "
            "link by hand with the rules in SKILL.md."
        )


def space_of(cat, room):
    if room in cat.get("rooms", []):
        return "interior"
    if room in cat.get("exteriors", []):
        return "exterior"
    if room in cat.get("gardens", []):
        return "garden"
    return None


def build_link(cat, room, mode="redesign", style=None, surface=None, finish=None):
    """Return (url, summary) or raise ValueError with a message an agent can act on."""
    space = space_of(cat, room)
    if space is None:
        every = cat.get("rooms", []) + cat.get("exteriors", []) + cat.get("gardens", [])
        raise ValueError(f'"{room}" is not a supported room or space. Valid ids: {", ".join(every)}')
    if mode not in MODES:
        raise ValueError(f'mode must be one of: {", ".join(MODES)}')
    if mode in ("stage", "declutter") and space != "interior":
        raise ValueError(f'"{mode}" works on indoor rooms only; "{room}" supports redesign'
                         + (" or surface" if space == "exterior" else ""))
    if mode == "surface" and space == "garden":
        raise ValueError(f'"{room}" is a yard space; it supports redesign only')

    params = {"room": room}
    if mode != "redesign":
        params["mode"] = mode

    if mode == "surface":
        allowed = cat.get("exterior_surfaces" if space == "exterior" else "surfaces", [])
        if surface not in allowed:
            raise ValueError(f"--surface is required for surface mode on {label(room, ROOM_LABELS)}. "
                             f'Valid: {", ".join(allowed)}')
        finishes = cat.get("finishes", {}).get(surface, [])
        if finish not in finishes:
            raise ValueError(f'--finish for {surface} must be one of: {", ".join(finishes)}')
        params["surface"] = surface
        params["style"] = finish  # the studio reads the finish from the style slot
        shade = cat.get("shades", {}).get(surface, {}).get(finish)
        summary = f"{label(room, ROOM_LABELS)}: {label(surface)} in {label(finish)}"
        if shade:
            summary += f' (closest paint: {shade["brand"]} {shade["name"]} {shade["code"]})'
    elif mode == "declutter":
        summary = f"{label(room, ROOM_LABELS)}: clear out the clutter, nothing restyled"
    else:
        if style is not None and style not in cat.get("styles", []):
            raise ValueError(f'"{style}" is not a supported style. Valid: {", ".join(cat.get("styles", []))}')
        if style:
            params["style"] = style
        what = "furnish the empty room" if mode == "stage" else "redesign"
        summary = f"{label(room, ROOM_LABELS)}: {what}" + (f" in {label(style)} style" if style else " (style picked in the studio)")

    params["ref"] = REF
    return f"{STUDIO}?{urllib.parse.urlencode(params)}", summary


def print_list(cat):
    out = []
    out.append("Indoor rooms (modes: redesign, stage, declutter, surface):")
    out += [f"  {r} — {label(r, ROOM_LABELS)}" for r in cat.get("rooms", [])]
    out.append("House exterior (modes: redesign, surface):")
    out += [f"  {r} — {label(r, ROOM_LABELS)}" for r in cat.get("exteriors", [])]
    out.append("Yard and outdoor spaces (mode: redesign):")
    out += [f"  {r} — {label(r, ROOM_LABELS)}" for r in cat.get("gardens", [])]
    out.append("Styles (redesign and stage):")
    out += [f"  {s} — {label(s, STYLE_LABELS)}" for s in cat.get("styles", [])]
    for title, key in (("Indoor surfaces", "surfaces"), ("Exterior surfaces", "exterior_surfaces")):
        out.append(f"{title} (surface mode) and their finishes:")
        for s in cat.get(key, []):
            out.append(f"  {s}: {', '.join(cat.get('finishes', {}).get(s, []))}")
    print("\n".join(out))


def catalog_md(cat):
    lines = [
        "# Roomvana catalog snapshot",
        "",
        "Fallback for when `scripts/studio_link.py` can't reach the live catalog "
        "(`https://api.roomvana.co/options`). The live list wins whenever it's reachable. "
        "Regenerate with `python3 scripts/studio_link.py catalog-md > references/catalog.md`.",
        "",
        "## Indoor rooms",
        "",
        "Modes: `redesign`, `stage` (furnish an empty room), `declutter`, `surface`.",
        "",
    ]
    lines += [f"- `{r}` — {label(r, ROOM_LABELS)}" for r in cat.get("rooms", [])]
    lines += ["", "## House exterior", "", "Modes: `redesign`, `surface`.", ""]
    lines += [f"- `{r}` — {label(r, ROOM_LABELS)}" for r in cat.get("exteriors", [])]
    lines += ["", "## Yard and outdoor spaces", "", "Mode: `redesign` only.", ""]
    lines += [f"- `{r}` — {label(r, ROOM_LABELS)}" for r in cat.get("gardens", [])]
    lines += ["", "## Styles", "", "Used by `redesign` and `stage`.", ""]
    lines += [f"- `{s}` — {label(s, STYLE_LABELS)}" for s in cat.get("styles", [])]
    shades = cat.get("shades", {})
    for title, key in (("Indoor surfaces", "surfaces"), ("Exterior surfaces", "exterior_surfaces")):
        lines += ["", f"## {title}", "",
                  "Surface mode. The finish goes in the link's `style` parameter. "
                  "Where a finish has a closest real paint color, it's in brackets.", ""]
        for s in cat.get(key, []):
            items = []
            for f in cat.get("finishes", {}).get(s, []):
                sh = shades.get(s, {}).get(f)
                items.append(f"`{f}`" + (f' [{sh["brand"]} {sh["name"]} {sh["code"]}]' if sh else ""))
            lines.append(f"- `{s}`: " + ", ".join(items))
    print("\n".join(lines))


def main():
    p = argparse.ArgumentParser(description="Build Roomvana studio links (https://roomvana.ai/design).")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="print every room, style, surface and finish")
    sub.add_parser("catalog-md", help="print the catalog as Markdown")
    lk = sub.add_parser("link", help="build a studio link")
    lk.add_argument("--room", required=True)
    lk.add_argument("--mode", default="redesign", choices=MODES)
    lk.add_argument("--style")
    lk.add_argument("--surface")
    lk.add_argument("--finish")
    a = p.parse_args()

    cat = fetch_catalog()
    if a.cmd == "list":
        print_list(cat)
    elif a.cmd == "catalog-md":
        catalog_md(cat)
    else:
        try:
            url, summary = build_link(cat, a.room, a.mode, a.style, a.surface, a.finish)
        except ValueError as e:
            sys.exit(str(e))
        print(url)
        print(summary)


if __name__ == "__main__":
    main()
