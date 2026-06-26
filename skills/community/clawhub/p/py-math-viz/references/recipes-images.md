# Recipes: Images (OpenCV tiling)

## Tile multiple plots into a single image

```bash
/root/.openclaw/workspace/.venv-math/bin/python \
  skills/py-math-viz/scripts/tile_images.py \
  --out out/plots/tiled.png --cols 2 --cell 1200x800 \
  out/plots/plot1.png out/plots/plot2.png out/plots/plot3.png out/plots/plot4.png
```

Tips:
- Increase `--cell` if plots look cramped
- Use `--cols 3` for 6–9 small plots
