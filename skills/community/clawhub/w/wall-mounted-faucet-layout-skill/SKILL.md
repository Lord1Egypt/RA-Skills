---
name: wall-mounted-faucet-layout
description: Calculate, validate, and visualize wall-mounted faucet installation geometry, especially faucet reach L and outlet height H1 for product selection. Use when an agent needs to solve or check faucet reach, outlet height, basin depth, stream angle, wall setback, or drain position from K, W/WS, L, H1, H2, and theta, or generate an annotated SVG diagram for the result.
---

# Wall-Mounted Faucet Layout

Source: https://github.com/starsy/wall-mounted-faucet-layout-skill

Diagram reference:

- English: `assets/wall_mounted_faucet_geometry_v2.svg`
- Chinese: `assets/wall_mounted_faucet_geometry_v2_zh.svg`

## Purpose

Use this skill to calculate or validate the installation geometry of a wall-mounted faucet and basin.

Most faucet-selection questions should focus on:

- `L`: required faucet reach, when the basin/drain geometry and desired outlet height are known
- `H1`: required outlet height above the basin rim, when a candidate faucet reach is known

It can solve for:

- `H1`: vertical distance from the basin rim to the faucet outlet
- `L`: horizontal reach of the faucet outlet from the finished wall
- `WS`: horizontal distance from the rear inner basin wall to the drain center
- `theta`: water-flow angle measured from the vertical
- `K`: horizontal distance from the finished wall to the rear inner basin wall
- `H2`: vertical depth from the basin rim reference line to the target point at the drain

It can also use `W`, the front-to-back inner basin width, to assume a centered drain when `WS` is not supplied.

## Coordinate convention

All linear measurements must use the same unit.

- Horizontal distance increases from the wall toward the front of the basin.
- Vertical distance increases downward from the faucet outlet toward the drain.
- `theta` is measured from the vertical direction.
- A positive `theta` means the water points forward, away from the wall.

| Symbol | Meaning |
|---|---|
| `K` | Finished wall to rear inner basin wall |
| `W` | Front-to-back inner width of the basin |
| `WS` | Rear inner basin wall to drain center |
| `L` | Finished wall to faucet outlet |
| `H1` | Basin rim to faucet outlet, vertically upward |
| `H2` | Basin rim to drain target point, vertically downward |
| `theta` | Water angle from vertical, in degrees |

If the drain is centered:

\[
WS = \frac{W}{2}
\]

## Primary faucet-selection workflow

Prefer solving for `L` or `H1` when the user is choosing a faucet:

- Solve for `L` when the user knows the desired outlet height or wall rough-in height. Use the result to compare against faucet reach/spec-sheet projection from the finished wall to the outlet.
- Solve for `H1` when the user has a candidate faucet reach `L`. Use the result to decide whether the outlet height above the basin rim is practical.
- Do not treat `H1 + H2` as a fixed recommended value. It is the vertical drop required by the selected horizontal geometry and stream angle.
- If the user asks generally for the "right faucet" and provides both a desired outlet height and basin/drain geometry, solve `L` first.
- If the user provides a faucet model or faucet reach, solve `H1` first.

## Core geometry

Horizontal offset:

\[
\Delta x = K + WS - L
\]

Vertical drop:

\[
\Delta y = H1 + H2
\]

Core relationship:

\[
\tan(\theta)=\frac{K+WS-L}{H1+H2}
\]

This models the water path as a straight centerline. Real water flow curves under gravity and varies with pressure, aerator design, and flow rate.

## Solving formulas

### Solve for `H1`

\[
H1=\frac{K+WS-L}{\tan(\theta)}-H2
\]

### Solve for `L`

\[
L=K+WS-(H1+H2)\tan(\theta)
\]

### Solve for `WS`

\[
WS=L-K+(H1+H2)\tan(\theta)
\]

### Solve for `theta`

\[
\theta=\arctan\left(\frac{K+WS-L}{H1+H2}\right)
\]

Convert the result to degrees.

### Solve for `K`

\[
K=L-WS+(H1+H2)\tan(\theta)
\]

### Solve for `H2`

\[
H2=\frac{K+WS-L}{\tan(\theta)}-H1
\]

## Required calculation procedure

1. Identify the target variable. For faucet selection, prefer `L` or `H1` unless the user explicitly asks for another variable.
2. Normalize all lengths to one unit.
3. Confirm that `theta` is measured from the vertical.
4. Resolve the drain location:
   - Use supplied `WS`; or
   - If `WS` is absent and `W` is supplied, set `WS = W / 2`.
5. Select the target formula.
6. Convert degrees to radians before calling a trigonometric function.
7. Calculate with a calculator or script.
8. Report the formula, substitution, exact result, and practical rounded result.
9. Run the validation checks.
10. Recommend an on-site water test before concealed installation.
11. When the user would benefit from a visual explanation or installation handoff, generate an annotated SVG with `scripts/render_geometry_svg.py`.

## Validation checks

- Require all inputs needed by the selected formula.
- Require one consistent length unit.
- Normally require `0° < theta < 90°` for forward flow.
- If `W` is known, require `0 < WS < W`.
- If `H1 < 0`, the geometry or reference lines are incompatible.
- If `K + WS - L < 0`, the target point lies behind the outlet under this coordinate convention.

Reverse-check the result by substituting it into:

\[
\tan(\theta)=\frac{K+WS-L}{H1+H2}
\]

If `W` is known, report the drain offset from basin center:

\[
\text{center offset}=WS-\frac{W}{2}
\]

- Positive: forward of center
- Negative: rearward of center
- Zero: centered

## Sensitivity

For fixed `K`, `WS`, `H2`, and `theta`:

\[
\frac{\partial H1}{\partial L}=-\frac{1}{\tan(\theta)}
\]

At `theta = 10°`:

\[
\frac{1}{\tan(10^\circ)}\approx5.67
\]

So increasing `L` by 1 cm lowers theoretical `H1` by about 5.67 cm.

## Response template

```text
Known:
K = ...
WS = ...  (or W = ... and WS = W/2)
H1 = ...
H2 = ...
L = ...
theta = ... degrees

Formula:
[target formula]

Substitution:
[...]

Result:
[target] = ... [unit]

Selection guidance:
- If solving L: compare this against faucet reach/spec-sheet projection from finished wall to outlet.
- If solving H1: compare this against the desired outlet height above the basin rim and available wall rough-in.

Validation:
- Horizontal offset Δx = ...
- Vertical drop Δy = ...
- Reverse check = ...
- Drain offset from basin center = ... (when W is known)

Practical note:
This is a straight-line geometric estimate. Confirm with a full-scale mock-up or water-flow test.
```

## Visual SVG output

When the user asks for a visual, diagram, annotated layout, client handoff, or installer handoff, render a custom SVG with the included script. Use the same inputs and target variable that you used for the numeric calculation.

```bash
python scripts/render_geometry_svg.py --solve L --K 5 --WS 20 --H1 15 --H2 14 --theta 10 --unit cm --output faucet-layout.svg
```

The generated SVG marks the supplied dimensions, solved value, horizontal offset, vertical drop, reverse-check angle, and practical warning note directly in the diagram. Prefer writing the output to a user-visible path named for the project or scenario.

## Worked examples

### Example 1: choose faucet reach, solve for `L`

Given `K=5 cm`, `WS=20 cm`, `H1=15 cm`, `H2=14 cm`, `theta=10°`:

\[
L=5+20-(15+14)\tan(10^\circ)\approx19.89\text{ cm}
\]

Interpretation: choose a faucet whose outlet projects about `19.9 cm` from the finished wall, then verify with real water flow.

### Example 2: check mounting height, solve for `H1`

Given `K=5 cm`, `W=40 cm`, `H2=14 cm`, `L=20.5 cm`, `theta=10°`:

\[
WS=20
\]

\[
H1=\frac{5+20-20.5}{\tan(10^\circ)}-14\approx11.52\text{ cm}
\]

Interpretation: this faucet reach works geometrically if the outlet can sit about `11.5 cm` above the basin rim.

### Example 3: short reach, solve for `H1`

Given `K=5 cm`, `WS=20 cm`, `H2=14 cm`, `L=16 cm`, `theta=10°`:

\[
H1=\frac{5+20-16}{\tan(10^\circ)}-14\approx37.04\text{ cm}
\]

The large result is expected because a 10-degree stream is close to vertical.

### Example 4: secondary check, solve for `WS`

Given `K=5 cm`, `H1=15 cm`, `H2=14 cm`, `L=20.5 cm`, `theta=10°`:

\[
WS=20.5-5+(15+14)\tan(10^\circ)\approx20.61\text{ cm}
\]

For `W=40 cm`, the drain is approximately `0.61 cm` forward of center.

## Agent implementation note

Prefer deterministic calculation with the included script. Do not estimate trigonometric values mentally when exact dimensions matter.

The script calculates with full floating-point precision internally, then prints practical engineering precision by default:

- `--unit mm`: whole millimeters
- `--unit cm`: `0.1 cm`
- `--unit m`: `0.001 m`
- Angles: `0.1°`

Use `--precision` or `--angle-precision` only when the user explicitly needs a different display precision.

Reference calculator:

```text
scripts/faucet_geometry.py
```

Reference visual renderer:

```text
scripts/render_geometry_svg.py
```

Primary calculator commands:

```bash
python scripts/faucet_geometry.py --solve L --K 5 --WS 20 --H1 15 --H2 14 --theta 10 --unit cm
python scripts/faucet_geometry.py --solve H1 --K 5 --W 40 --H2 14 --L 20.5 --theta 10 --unit cm
```
