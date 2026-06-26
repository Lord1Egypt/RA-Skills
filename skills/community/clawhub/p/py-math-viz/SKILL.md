---
name: py-math-viz
description: Create clear math/data visualizations in Python and export to PNG (matplotlib/seaborn; optional OpenCV post-processing). Use when the user asks to plot functions, draw graphs, visualize simulations/trajectories, compare models, make publication-quality plots, or needs a PNG chart for Telegram/notes. Includes scripts to render plots from a JSON spec and to tile/annotate images.
---

# Py Math Viz

Use Python to produce **clean, readable plots** and **export to PNG by default**.

Assumptions (this workspace):
- Preferred interpreter: `/root/.openclaw/workspace/.venv-math/bin/python`
- Libraries: `matplotlib`, `seaborn`, `numpy` (already), `opencv-python-headless` (installed)

## Defaults (quality rules)

- Output: PNG, `dpi>=200`, white background
- Always label axes; add title if it helps
- Use legend when multiple series exist (and place it so it doesn’t cover data)
- Avoid overlap:
  - prefer `constrained_layout=True` and/or `plt.tight_layout()`
  - rotate dense x-ticks, shorten tick labels
  - increase figure size instead of cramming
- Use consistent styling:
  - `seaborn.set_theme(style="whitegrid")`
  - colorblind-friendly palette if unsure

## Quick start (script)

Render a plot from a JSON spec.
To keep the workspace root clean, **write outputs into `out/`** (or `out/_scratch/` for throwaway experiments):

```bash
/root/.openclaw/workspace/.venv-math/bin/python \
  skills/py-math-viz/scripts/plot_from_spec.py \
  --spec spec.json --out out/plots/plot.png
```

Then send `out/plots/plot.png` (Telegram: use the `message` tool with `filePath`).

## Plot spec

The spec is intentionally small.
Read:
- `references/spec.md` — schema + examples
- `references/quick-recipes.md` — recipes index (points to JSON specs / seaborn snippets / image tiling)

## OpenCV helpers

Tile multiple PNGs into one (for comparisons):

```bash
/root/.openclaw/workspace/.venv-math/bin/python \
  skills/py-math-viz/scripts/tile_images.py \
  --out tiled.png img1.png img2.png img3.png
```

## When NOT to use

- Interactive dashboards (Plotly/Dash) unless explicitly asked
- 3D/mesh-heavy rendering (use specialized tools if needed)
