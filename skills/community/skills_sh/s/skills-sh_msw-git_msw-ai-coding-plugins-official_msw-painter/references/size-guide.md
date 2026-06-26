# Image size guide

Most entities in a Maker workspace are based on small sprites. **Always specify an appropriate size** so the size ratio matches surrounding entities.

## Recommended size table

| Use | Recommended size | Examples |
|-----|------------------|----------|
| Icon, small object, button icon | `48×48` ~ `64×64` | Heart, coin, arrow, star |
| General character, item, NPC, monster | `96×96` ~ `128×128` | Slime, sword, shield, tree |
| Tile, floor, block | `64×64` ~ `128×128` | Grass tile, brick, platform |
| Background, large object | `256×256` or larger | **Only when the user explicitly requests a large size** |

## Rules

- **The default 512×512 is too large** — always specify `--width` / `--height`.
- Use **128×128** as the default when there is no special requirement.
- Transparent background (PNG alpha) is the default — if you do not draw a background in the SVG/Canvas/HTML, the output is automatically transparent.

## Aspect ratio guide

- Square (`width === height`) is the default. Characters / icons are almost always square.
- Horizontally elongated objects (vehicles, bridges) use `2:1` (e.g. 192×96).
- Vertically elongated objects (trees, flags) use `1:2` (e.g. 96×192).
- Avoid irregular ratios when possible — they can affect collider / hit-box alignment of the entity.

## Working grid per style

The standard pixel art workflow is to draw on a **small logical grid → scaled up to a larger output canvas**. The logical grid size depends on which style you picked in `SKILL.md` step 2.

### Chunky pixel working grid (see [style-chunky-pixel.md](style-chunky-pixel.md))

Larger pixels-per-dot → chunky retro feel.

| Output size | Recommended logical grid | Pixels per dot |
|-------------|--------------------------|----------------|
| 48×48   | 16×16            | 3 |
| 64×64   | 16×16            | 4 |
| 96×96   | 24×24 or 16×16   | 4 or 6 |
| 128×128 | 16×16 or 32×32   | 8 or 4 |
| 256×256 | 32×32 or 64×64   | 8 or 4 |

### Maple cartoon working grid (see [style-maple-cartoon.md](style-maple-cartoon.md))

Smaller pixels-per-dot → room for facial features, selout, and selective AA.

| Output size | Recommended logical grid | Pixels per dot |
|-------------|--------------------------|----------------|
| 48×48   | 24×24            | 2 |
| 64×64   | 32×32            | 2 |
| 96×96   | 48×48            | 2 |
| 128×128 | 64×64            | 2 |
| 256×256 | 128×128          | 2 |

> A logical grid that is too small (≤ 24×24) does not leave room for selout + AA + facial features, so it forces the result back into chunky territory. If the requested output is below 64×64 and you want maple cartoon feel, raise the output size first.

## Character proportions (Maple cartoon style only)

Maple-style characters are **2.5 to 3 heads tall** (super-deformed / chibi).

| Total height | Head | Torso | Legs |
|--------------|------|-------|------|
| 64 px  | 26 px | 18 px | 20 px |
| 96 px  | 32 px | 28 px | 36 px |
| 128 px | 42 px | 38 px | 48 px |

Full character drawing details (face features, hair, accents) are in [style-maple-cartoon.md](style-maple-cartoon.md).
