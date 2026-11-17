# The engine — maths, CLI, uniqueness

`templates/token_engine.py` is the whole pipeline in one file: two declarative libraries, one
derivation, five emitters. Copy it beside the project and edit only the two libraries.

## 1 · The two libraries

```python
GROUNDS = [
    # slug, name, stock, press-black, dark?, note
    ("warm", "Warm Paper", "#FDF3E3", "#12100E", False, "cream, forgiving, archive"),
    ("board", "Blackboard", "#141414", "#0A0A0A", True, "hi-vis reads here"),
]

INKS = [
    # slug, name, accent, secondary, short, family, screen angle
    ("cobalt", "Cobalt & Rose", "#0F4BD8", "#E8175D", "Cobalt", "riso", 27),
    ("hivis", "Hi-Vis Yellow & Safety Orange", "#D6FF00", "#FF5F00", "Hi-Vis", "hivis", 15),
]
```

**Ground** = what the eye reads as "which theme is this". **Ink pair** = what it prints. A new
ground multiplies the whole ink library; a new ink multiplies every ground. Ten grounds × fifteen
inks = 150 themes with both a day and a night plate.

The `family` string is intent, and it is what you show a user in a picker:
`riso` (muted print), `vivid` (high-chroma), `hivis` (fluorescent/safety), `accent` (one loud colour).

## 2 · Reading a reference for its inks

Never eyeball hexes from a photograph — sample the flat fields:

```python
from PIL import Image
from collections import Counter
im = Image.open(ref).convert("RGB")
im = im.resize((700, int(im.height * 700 / im.width)), Image.NEAREST)  # NEAREST, never thumbnail
counts = Counter(im.getdata())
total = sum(counts.values())
for col, n in counts.most_common(12):
    print("#%02X%02X%02X" % col, round(100 * n / total, 1), "%")
```

Rules of thumb from the histogram:

| evidence | conclusion |
|---|---|
| one colour > 50% | that is the stock |
| 10–25% | the field ink |
| 1–5% | a register mark / accent |
| darkest of the set, 1–5% | the press black |

`Image.thumbnail()` bilinearly resamples and **invents** colours between flat fields — it destroys the
histogram. Always a NEAREST resize.

## 3 · The derivation (one function, two polarities)

```python
def derive(ground, ink, plate):
    if ground.dark:
        surface = stock if plate == "day" else mix(stock, "#000", 0.45)
        typ, towards = mix(stock, "#FFF", 0.90), "#FFFFFF"
    else:
        surface = stock if plate == "day" else press
        typ = press if plate == "day" else mix(stock, "#FFF", 0.10)
        towards = "#000000" if plate == "day" else "#FFFFFF"
    ...
    tokens["accent"]    = walk(ink.accent, surface, 3.0, towards)   # usable as a FILL
    tokens["accentInk"] = walk(ink.accent, surface, 4.5, towards)   # usable as TYPE
```

`walk(colour, bg, target, towards)` mixes toward black or white in 5% steps and returns the first
value that clears `target`. That single function is why a hi-vis ink can be a superb fill on a dark
board and unusable type on paper, with no special cases anywhere in the code.

**Token set** (every surface consumes these, none re-derives):

```
surface ink ink2 panel panelDeep muted rule ruleSoft
accent accentInk secondary secondaryInk selection onSurface onAccent
ok warn error
```

- `ink` — body type on this surface. `ink2` — copy, a hair softer.
- `muted` — captions only; walked against the *panel*, the darkest thing captions sit on.
- `accent` / `secondary` — fills. `accentInk` / `secondaryInk` — small type.
- `onSurface` / `onAccent` — a label that must sit on that fill (auto black/cream by luminance).

## 4 · Contrast gates

| what | floor |
|---|---|
| body, copy, captions, small type | **4.5:1** (WCAG AA) |
| fills, large display type (>= 24px / 18.66px bold) | 3:1 |
| hairlines and rules | no floor — they are decoration, never information |

`--report` prints the curated set and then `text pairings under AA: none`. Treat a non-empty list as
a build failure, not a warning: adjust the ink, and let the walk correct the rest.

## 5 · CLI

```bash
python3 token_engine.py --list                       # the whole grid
python3 token_engine.py --report                     # ratios + AA gate
python3 token_engine.py --theme warm-cobalt --emit css     --out build/
python3 token_engine.py --theme board-hivis  --emit vscode  --out build/
python3 token_engine.py --theme warm-cobalt  --emit latex   --out build/
python3 token_engine.py --theme warm-cobalt  --emit json    --out build/
python3 token_engine.py --theme warm-cobalt  --emit skin    --out build/
```

Emitted filenames: `<theme>.css`, `<theme>.tokens.json`, `<theme>.vscode-theme.json`,
`marble-<theme>.sty`, `<theme>.yaml`.

## 6 · Uniqueness (multi-user systems)

```bash
python3 token_engine.py --assign sakib     # assign + remember
theme = assignments["sakib"]                # stable per user
```

- Deterministic: `sha256(user) % len(free_themes)`.
- Never repeats a theme another user holds; a `assignments.json` registry is the ledger.
- Pool exhausted → start a fresh pass in a user-derived order (not the same order again).

Use this whenever more than one person sees the product: tenants, bot profiles, accounts, docs
branding per client. Two users on the same theme is a bug, not a coincidence.

## 7 · Adding to the libraries

1. Pick the ink hexes from a reference or a brand; do **not** hand-pick the derived values.
2. Add one tuple to `GROUNDS` or `INKS`; keep `family` honest.
3. Run `--report`. If something fails AA, the answer is another ink, not a hand-tuned exception.
4. Re-emit every surface. Never patch a surface file that was generated.
