#!/usr/bin/env python3
"""
token_engine.py — one palette, every surface.

Grounds (stocks) × inks (accent pairs) → derive() → tokens → emitters.

    python3 token_engine.py --list
    python3 token_engine.py --report
    python3 token_engine.py --theme warm-cobalt --emit css     --out build/
    python3 token_engine.py --theme night-hivis  --emit vscode  --out build/
    python3 token_engine.py --theme warm-cobalt  --emit latex   --out build/
    python3 token_engine.py --theme warm-cobalt  --emit json    --out build/
    python3 token_engine.py --theme warm-cobalt  --emit skin    --out build/
    python3 token_engine.py --assign sakib                     # unique per user

Surfaces: css (web/UI), vscode (editor + terminal ANSI), latex (xcolor package),
json (design tokens for documents/PDF/pipelines), skin (Hermes/app theme YAML).

Edit the two libraries, never an emitter. Everything else is derived.
"""

import argparse
import hashlib
import json
import os
import sys

# ── library 1 · grounds ─────────────────────────────────────────────────────
# slug, name, stock, press-black, dark?, note
GROUNDS = [
    ("warm", "Warm Paper", "#FDF3E3", "#12100E", False, "cream, forgiving, archive"),
    ("news", "Newsprint", "#F2EEE2", "#171717", False, "cheap and proud"),
    ("bone", "Bone", "#F4EFE4", "#1A1917", False, "neutral gallery stock"),
    ("cool", "Cool Stock", "#EDF1F1", "#14181A", False, "blue-cast, technical"),
    ("kraft", "Kraft", "#E4D7C2", "#1C150E", False, "unbleached board"),
    ("blush", "Blush Stock", "#F8EFE6", "#1B1214", False, "pink-cast, cultural"),
    ("sage", "Sage Stock", "#E9EDE2", "#171A14", False, "green-cast, botanical"),
    ("graphite", "Graphite", "#DCDCD8", "#131313", False, "grey board"),
    ("board", "Blackboard", "#141414", "#0A0A0A", True, "hi-vis reads here"),
    ("midnight", "Midnight Board", "#0E1420", "#070A10", True, "neon reads coldest"),
]

# ── library 2 · inks ────────────────────────────────────────────────────────
# slug, name, accent, secondary, short, family, screen angle
INKS = [
    ("cobalt", "Cobalt & Rose", "#0F4BD8", "#E8175D", "Cobalt", "riso", 27),
    ("vermilion", "Vermilion & Slate", "#C1440E", "#2C4A52", "Vermilion", "riso", 15),
    ("moss", "Moss & Ochre", "#246B4A", "#A96712", "Moss", "riso", 38),
    ("plum", "Plum & Amber", "#6B2D5B", "#A85A10", "Plum", "riso", 62),
    ("teal", "Teal & Coral", "#0F6E6E", "#D2523C", "Teal", "riso", 15),
    ("indigo", "Indigo & Marigold", "#2B2F7A", "#C98A00", "Indigo", "riso", 45),
    ("olive", "Olive & Clay", "#4F5A1E", "#A4552F", "Olive", "riso", 38),
    ("navy", "Navy & Fuchsia", "#1F3A5F", "#B0306B", "Navy", "riso", 62),
    ("vivid", "Vivid Magenta & Cyan", "#E6007E", "#00A3E0", "Vivid", "vivid", 15),
    ("electric", "Electric Blue & Gold", "#0066FF", "#FFC400", "Electric", "vivid", 27),
    ("ultra", "Ultraviolet & Lemon", "#7A00FF", "#FFE600", "Ultraviolet", "vivid", 45),
    ("hivis", "Hi-Vis Yellow & Safety Orange", "#D6FF00", "#FF5F00", "Hi-Vis", "hivis", 15),
    ("neon", "Fluorescent Pink & Aqua", "#FF2D95", "#00E0C6", "Fluorescent", "hivis", 38),
    ("laser", "Laser Green & Signal Red", "#39FF14", "#FF2B2B", "Laser", "hivis", 62),
    ("signal", "Signal Orange & Ink", "#FF5F00", "#0B3D91", "Signal", "accent", 27),
]

CURATED = ["warm-cobalt", "cool-teal", "news-vermilion", "kraft-moss", "blush-plum",
           "bone-indigo", "sage-olive", "graphite-electric", "board-hivis",
           "midnight-neon", "warm-signal"]


# ── colour maths ────────────────────────────────────────────────────────────
def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexof(c):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v))) for v in c)


def _lin(v):
    v = v / 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def luminance(h):
    r, g, b = rgb(h)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def mix(a, b, t):
    return hexof(tuple(x + (y - x) * t for x, y in zip(rgb(a), rgb(b))))


def walk(fg, bg, target, towards="#000000"):
    """Push fg toward black (or white) until it clears `target` against bg."""
    for step in range(0, 21):
        ink = mix(fg, towards, step / 20)
        if contrast(ink, bg) >= target:
            return ink
    return mix(fg, towards, 1.0)


def on(surface):
    """Cream or ink, whichever the surface can carry."""
    return "#0B0B0B" if luminance(surface) > 0.5 else "#F6F1E7"


# ── derive ──────────────────────────────────────────────────────────────────
def derive(g, i, plate="day"):
    gs, gname, stock, press, dark, gnote = g
    islug, iname, accent, secondary, short, family, angle = i
    dark_ground = dark

    if dark_ground:
        surface = stock if plate == "day" else mix(stock, "#000000", 0.45)
        typ = mix(stock, "#FFFFFF", 0.90)
        towards = "#FFFFFF"
        panel = mix(surface, typ, 0.06)
        panel_deep = mix(surface, typ, 0.11)
        muted = mix(typ, surface, 0.42)
        rule = mix(surface, typ, 0.22)
        rule_soft = mix(surface, typ, 0.13)
        sel_t = 0.32
    else:
        surface = stock if plate == "day" else press
        typ = press if plate == "day" else mix(stock, "#FFFFFF", 0.10)
        towards = "#000000" if plate == "day" else "#FFFFFF"
        panel = mix(surface, typ, 0.035 if plate == "day" else 0.06)
        panel_deep = mix(surface, typ, 0.075 if plate == "day" else 0.10)
        muted = walk(mix(typ, surface, 0.62), panel, 4.5, towards=towards)
        rule = mix(typ, surface, 0.22 if plate == "night" else 0.78)
        rule_soft = mix(typ, surface, 0.13 if plate == "night" else 0.88)
        sel_t = 0.22 if plate == "day" else 0.32

    fill_floor = 3.0 if (dark_ground or plate == "night") else 1.0
    t = {
        "surface": surface, "ink": typ, "ink2": mix(typ, surface, 0.12),
        "panel": panel, "panelDeep": panel_deep, "muted": muted,
        "rule": rule, "ruleSoft": rule_soft,
        "accent": walk(accent, surface, fill_floor, towards=towards),
        "accentInk": walk(accent, surface, 4.5, towards=towards),
        "secondary": walk(secondary, surface, fill_floor, towards=towards),
        "secondaryInk": walk(secondary, surface, 4.5, towards=towards),
        "ok": walk("#1F8A55", panel, 4.5, towards=towards),
        "warn": walk("#B06A00" if towards == "#000000" else "#C98A12", panel, 4.5, towards=towards),
        "error": walk("#C4182A" if towards == "#000000" else "#E8503F", panel, 4.5, towards=towards),
        "selection": mix(surface, secondary, sel_t),
        "onSurface": on(surface), "onAccent": on(walk(accent, surface, fill_floor, towards=towards)),
    }
    return t


PAIRS = [("ink", "surface", "body"), ("ink2", "surface", "copy"),
         ("muted", "surface", "caption"), ("muted", "panel", "caption on panel"),
         ("accent", "surface", "accent fill"), ("accentInk", "surface", "accent type"),
         ("secondary", "surface", "register fill"),
         ("secondaryInk", "surface", "register type"),
         ("onAccent", "accent", "label on accent")]


def theme(code):
    gs, islug = code.split("-")
    g = next(x for x in GROUNDS if x[0] == gs)
    i = next(x for x in INKS if x[0] == islug)
    plates = {"day": derive(g, i, "day"), "night": derive(g, i, "night")}
    ratios = {k: {f"{a}/{b}": contrast(p[a], p[b]) for a, b, _ in PAIRS} for k, p in plates.items()}
    return {"code": code, "name": f"{gs}-{islug}", "label": f"{g[1]} · {i[1]}",
            "ground": {"slug": g[0], "name": g[1], "note": g[5]},
            "ink": {"slug": i[0], "name": i[1], "short": i[4], "family": i[5], "angle": i[6]},
            "plates": plates, "contrast": ratios}


def all_codes():
    return [f"{g[0]}-{i[0]}" for g in GROUNDS for i in INKS]


# ── emitters ────────────────────────────────────────────────────────────────
def emit_css(t):
    out = [f"/* {t['label']} — generated by token_engine.py. Do not hand-edit. */"]
    for plate in ("day", "night"):
        sel = ":root, [data-theme=\"%s\"][data-plate=\"day\"]" % t["name"] if plate == "day" \
            else '[data-theme="%s"][data-plate="night"]' % t["name"]
        out.append(f"{sel} {{")
        out += [f"  --{k}: {v};" for k, v in t["plates"][plate].items()]
        out.append("}")
    return "\n".join(out) + "\n"


def emit_json(t):
    return json.dumps(t, indent=2)


def ansi_map(t):
    p = t["plates"]["day"]
    return {
        "black": p["surface"], "red": p["error"], "green": p["ok"],
        "yellow": p["warn"], "blue": p["accent"], "magenta": p["secondary"],
        "cyan": mix(p["accent"], p["secondary"], 0.5), "white": p["ink"],
        "brightBlack": p["muted"], "brightRed": mix(p["error"], "#FFFFFF", 0.25),
        "brightGreen": mix(p["ok"], "#FFFFFF", 0.25),
        "brightYellow": mix(p["warn"], "#FFFFFF", 0.25),
        "brightBlue": mix(p["accent"], "#FFFFFF", 0.25),
        "brightMagenta": mix(p["secondary"], "#FFFFFF", 0.25),
        "brightCyan": mix(mix(p["accent"], p["secondary"], 0.5), "#FFFFFF", 0.25),
        "brightWhite": p["ink"],
    }


def emit_vscode(t):
    p = t["plates"]["day"]
    dark = luminance(p["surface"]) < 0.4
    a = ansi_map(t)
    colors = {
        "editor.background": p["surface"], "editor.foreground": p["ink"],
        "editorLineNumber.foreground": p["muted"],
        "editorLineNumber.activeForeground": p["ink"],
        "editorCursor.foreground": p["accent"],
        "editor.selectionBackground": p["selection"],
        "editor.inactiveSelectionBackground": p["panelDeep"],
        "editor.lineHighlightBackground": p["panel"],
        "editorIndentGuide.background1": p["ruleSoft"],
        "editorWhitespace.foreground": p["rule"],
        "editorGutter.background": p["surface"],
        "editorError.foreground": p["error"], "editorWarning.foreground": p["warn"],
        "editorInfo.foreground": p["accentInk"],
        "editorBracketMatch.background": p["panel"],
        "editorBracketMatch.border": p["accent"],
        "focusBorder": p["accent"],
        "foreground": p["ink2"], "descriptionForeground": p["muted"],
        "activityBar.background": p["panel"], "activityBar.foreground": p["ink"],
        "activityBar.border": p["rule"], "activityBar.inactiveForeground": p["muted"],
        "activityBarBadge.background": p["accent"],
        "activityBarBadge.foreground": p["onAccent"],
        "sideBar.background": p["panel"], "sideBar.foreground": p["ink2"],
        "sideBar.border": p["rule"],
        "sideBarSectionHeader.background": p["panelDeep"],
        "sideBarSectionHeader.foreground": p["ink"],
        "list.activeSelectionBackground": p["selection"],
        "list.activeSelectionForeground": p["ink"],
        "list.hoverBackground": p["panelDeep"],
        "list.inactiveSelectionBackground": p["panel"],
        "statusBar.background": p["accent"], "statusBar.foreground": p["onAccent"],
        "statusBar.border": p["accent"],
        "statusBar.noFolderBackground": p["panel"],
        "statusBarItem.remoteBackground": p["secondary"],
        "statusBarItem.remoteForeground": p["onSurface"],
        "titleBar.activeBackground": p["panel"], "titleBar.activeForeground": p["ink"],
        "titleBar.inactiveBackground": p["panelDeep"],
        "titleBar.border": p["rule"],
        "tabs.background": p["panel"],
        "tab.activeBackground": p["surface"], "tab.activeForeground": p["ink"],
        "tab.inactiveBackground": p["panel"], "tab.inactiveForeground": p["muted"],
        "tab.border": p["rule"], "tab.activeBorderTop": p["accent"],
        "panel.background": p["panel"], "panel.border": p["rule"],
        "panelTitle.activeForeground": p["ink"],
        "panelTitle.activeBorder": p["accent"],
        "terminal.background": p["surface"], "terminal.foreground": p["ink"],
        **{f"terminal.ansi{k[0].upper() + k[1:]}": v for k, v in a.items()},
        "button.background": p["accent"], "button.foreground": p["onAccent"],
        "input.background": p["panel"], "input.foreground": p["ink"],
        "input.border": p["rule"], "input.placeholderForeground": p["muted"],
        "badge.background": p["secondary"], "badge.foreground": p["onSurface"],
        "scrollbarSlider.background": mix(p["rule"], p["surface"], 0.35),
        "scrollbarSlider.hoverBackground": p["rule"],
        "widget.shadow": "#00000055" if dark else "#00000022",
        "diffEditor.insertedTextBackground": mix(p["ok"], p["surface"], 0.78),
        "diffEditor.removedTextBackground": mix(p["error"], p["surface"], 0.78),
        "gitDecoration.addedResourceForeground": p["ok"],
        "gitDecoration.modifiedResourceForeground": p["warn"],
        "gitDecoration.deletedResourceForeground": p["error"],
    }
    colors["statusBarItem.remoteForeground"] = p["onSurface"]

    scopes = [
        (["comment", "punctuation.definition.comment"], p["muted"], "italic"),
        (["string", "string.quoted", "punctuation.definition.string"], p["ok"], None),
        (["constant.numeric", "constant.language"], p["secondaryInk"], None),
        (["keyword", "storage.type", "storage.modifier"], p["accentInk"], None),
        (["entity.name.function", "support.function", "meta.function-call"], p["ink"], "bold"),
        (["entity.name.type", "entity.name.class", "support.class"], p["warn"], None),
        (["variable", "variable.parameter", "entity.name.variable"], p["ink2"], None),
        (["constant.character.escape", "regexp"], p["secondary"], None),
        (["keyword.operator"], p["muted"], None),
        (["punctuation", "meta.brace"], p["muted"], None),
        (["entity.name.tag", "support.type.property-name"], p["accentInk"], None),
        (["entity.other.attribute-name"], p["secondaryInk"], None),
        (["invalid", "invalid.illegal"], p["error"], "bold underline"),
        (["markup.heading"], p["ink"], "bold"),
        (["markup.bold"], p["ink"], "bold"),
        (["markup.italic"], p["ink2"], "italic"),
        (["markup.inserted"], p["ok"], None),
        (["markup.deleted"], p["error"], None),
    ]
    token_colors = []
    for scope, fg, style in scopes:
        settings = {"foreground": fg}
        if style:
            settings["fontStyle"] = style
        token_colors.append({"scope": scope, "settings": settings})

    theme = {
        "$schema": "vscode://schemas/color-theme",
        "name": f"Marble {t['label']}",
        "type": "dark" if dark else "light",
        "semanticHighlighting": True,
        "colors": colors,
        "tokenColors": token_colors,
        "semanticTokenColors": {
            "variable": p["ink2"], "parameter": p["ink2"],
            "function": p["ink"], "method": p["ink"],
            "class": p["warn"], "type": p["warn"], "interface": p["warn"],
            "keyword": p["accentInk"], "string": p["ok"], "number": p["secondaryInk"],
            "comment": {"foreground": p["muted"], "italic": True},
            "property": p["accentInk"], "enumMember": p["secondaryInk"],
        },
    }
    return json.dumps(theme, indent=2)


def emit_latex(t):
    p = t["plates"]["day"]
    slug = t["name"].replace("-", "")
    defs = "\n".join(f"\\definecolor{{theme{k}}}{{HTML}}{{{v.lstrip('#')}}}"
                     for k, v in p.items())
    return f"""% marble-theme — generated by token_engine.py. Do not hand-edit.
% Theme: {t['label']}
\\NeedsTeXFormat{{LaTeX2e}}
\\ProvidesPackage{{marble-{t['name']}}}[{t['label']}]
\\RequirePackage{{xcolor}}

{defs}

% semantic aliases — use these, never the raw names
\\colorlet{{themeBody}}{{themeink}}
\\colorlet{{themeBodySoft}}{{themeink2}}
\\colorlet{{themeCaption}}{{thememuted}}
\\colorlet{{themeRule}}{{themerule}}
\\colorlet{{themeRuleSoft}}{{themeruleSoft}}
\\colorlet{{themePanel}}{{themepanel}}
\\colorlet{{themeField}}{{themeaccent}}
\\colorlet{{themeFieldInk}}{{themeaccentInk}}
\\colorlet{{themeRegister}}{{themesecondary}}
\\colorlet{{themeRegisterInk}}{{themesecondaryInk}}
\\colorlet{{themeOnField}}{{themeonAccent}}
\\colorlet{{themeSurface}}{{themesurface}}

\\newcommand{{\\themeName}}{{{t['label']}}}
\\newcommand{{\\themeFieldRule}}{{\\textcolor{{themeField}}{{\\rule{{0.6pt}}{{1.2em}}}}}}
\\newcommand{{\\themeHairline}}{{\\textcolor{{themeRule}}{{\\rule{{\\linewidth}}{{0.4pt}}}}}}
\\newcommand{{\\themeFieldText}}[1]{{\\textcolor{{themeFieldInk}}{{#1}}}}
\\newcommand{{\\themeRegisterText}}[1]{{\\textcolor{{themeRegisterInk}}{{#1}}}}
\\newcommand{{\\themeCode}}[1]{{\\colorbox{{themePanel}}{{\\texttt{{#1}}}}}}

\\endinput
"""


def emit_skin(t):
    p = t["plates"]["day"]
    rows = [
        ("background", p["surface"]), ("ui_accent", p["accent"]),
        ("banner_accent", p["accent"]), ("ui_tool", p["secondary"]),
        ("banner_title", p["ink"]), ("banner_text", p["ink2"]),
        ("ui_text", p["ink2"]), ("ui_label", p["accentInk"]),
        ("banner_dim", p["muted"]), ("ui_thinking", p["muted"]),
        ("banner_border", p["rule"]), ("ui_border", p["rule"]),
        ("ui_ok", p["ok"]), ("ui_warn", p["warn"]), ("ui_error", p["error"]),
        ("prompt", p["ink"]), ("input_rule", p["accent"]),
        ("response_border", p["secondary"]), ("status_bar_bg", p["panel"]),
        ("status_bar_text", p["ink2"]), ("completion_menu_bg", p["panel"]),
        ("completion_menu_current_bg", p["panelDeep"]), ("selection_bg", p["selection"]),
    ]
    colors = "\n".join(f'  {k}: "{v}"' for k, v in rows)
    return f"""# {t['label']} — generated by token_engine.py
name: marble-{t['name']}
description: "{t['label']}"

colors:
{colors}

branding:
  agent_name: COOPER
  prompt_symbol: "❯"

tool_prefix: "┊"

customCSS: |
  :root[data-hermes-theme="marble-{t['name']}"] {{ --radius-scalar: 0.10; }}
  :root[data-hermes-theme="marble-{t['name']}"] body::after {{
    content: ""; position: fixed; inset: -40%; pointer-events: none; z-index: 9;
    background-image: radial-gradient(circle at 50% 50%, {p['ink']} 0.42px, transparent 0.55px);
    background-size: 5px 5px; opacity: 0.055; transform: rotate({t['ink']['angle']}deg);
  }}
"""


EMITTERS = {"css": (emit_css, "css"), "json": (emit_json, "tokens.json"),
            "vscode": (emit_vscode, "vscode-theme.json"),
            "latex": (emit_latex, "sty"), "skin": (emit_skin, "yaml")}


# ── uniqueness ──────────────────────────────────────────────────────────────
def assign(user, path="assignments.json"):
    taken = {}
    if os.path.exists(path):
        try:
            taken = json.load(open(path))
        except Exception:
            taken = {}
    if user in taken:
        return taken[user], taken
    used = set(taken.values())
    free = [c for c in all_codes() if c not in used] or all_codes()
    idx = int(hashlib.sha256(user.encode()).hexdigest()[:8], 16) % len(free)
    taken[user] = free[idx]
    json.dump(taken, open(path, "w"), indent=2, sort_keys=True)
    return taken[user], taken


# ── CLI ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="one palette, every surface")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--theme", metavar="CODE")
    ap.add_argument("--emit", choices=sorted(EMITTERS))
    ap.add_argument("--out", default=".")
    ap.add_argument("--seed", metavar="USER")
    ap.add_argument("--assign", metavar="USER")
    ap.add_argument("--all-curated", action="store_true", help="emit every curated theme")
    args = ap.parse_args()

    if args.list:
        for g in GROUNDS:
            print(f"{g[1]:14s} " + "  ".join(f"{g[0]}-{i[0]}" for i in INKS))
        print(f"\n{len(all_codes())} themes · {len(GROUNDS)} grounds × {len(INKS)} inks")
        return

    if args.report:
        weak = []
        for code in all_codes():
            t = theme(code)
            for plate in ("day", "night"):
                c = t["contrast"][plate]
                for key in ("ink/surface", "muted/surface", "accentInk/surface", "secondaryInk/surface"):
                    if c[key] < 4.5:
                        weak.append((code, plate, key, c[key]))
        for code in CURATED:
            t = theme(code)
            c = t["contrast"]["day"]
            print(f"{code:22s} body {c['ink/surface']:5.2f}  field {c['accentInk/surface']:5.2f}  "
                  f"register {c['secondaryInk/surface']:5.2f}")
        print(f"\ntext pairings under AA: {weak or 'none'}")
        return

    if args.seed:
        code, taken = assign(args.seed)
        print(f"{args.seed} -> {code}  ({len(taken)} assigned)")
        return

    if args.assign:
        code, _ = assign(args.assign)
        args.theme = code
        args.emit = args.emit or "skin"

    if not args.theme or not args.emit:
        ap.print_help()
        return

    t = theme(args.theme)
    fn, ext = EMITTERS[args.emit]
    body = fn(t)
    os.makedirs(args.out, exist_ok=True)
    stem = f"marble-{args.theme}" if args.emit == "latex" else args.theme
    path = os.path.join(args.out, f"{stem}.{ext}")
    open(path, "w").write(body)
    p = t["plates"]["day"]
    print(f"{path}  ({len(body)} bytes)")
    print(f"  ground {t['ground']['name']} {p['surface']} · field {p['accent']} · "
          f"register {p['secondary']} · body {t['contrast']['day']['ink/surface']}:1")


if __name__ == "__main__":
    main()
