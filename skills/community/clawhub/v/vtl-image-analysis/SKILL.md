---
name: vtl-image-analysis
description: >
  Measure compositional structure in AI-generated images using the Visual
  Thinking Lens (VTL) framework. Detects default-mode bias (center lock,
  radial collapse, low tension) and generates targeted re-prompts via
  configurable operators. Run after image generation to diagnose and improve
  compositional quality.
metadata:
  openclaw:
    emoji: "🎛️"
    category: image
    requires:
      bins: ["python3"]
    install:
      - id: pip
        kind: pip
        packages: ["numpy", "opencv-python-headless", "scikit-image", "scipy", "pyyaml"]
---

# VTL Image Analysis

Use this skill whenever a user asks to analyze, diagnose, or improve a
generated image's composition. Also invoke it proactively after image
generation if the user has requested better compositional quality.

## When to Use

- User says "analyze this image", "why does this look generic/flat/boring"
- User asks to improve a generated image's composition
- After generating an image with openai-image-gen or similar skills
- User asks why their prompts aren't producing interesting layouts

## Step 1 — Measure

Run the probe script on the image:

```bash
python3 scripts/vtl_probe.py <image_path>
```

This returns JSON. Example:
```json
{
  "valid": true,
  "mask_status": "PASS",
  "delta_x": -0.027,
  "delta_y": 0.008,
  "r_v": 0.875,
  "rho_r": 12.4,
  "dRC": 0.40,
  "dRC_label": "mass-dominant",
  "k_var": 1.12,
  "infl_density": 0.16,
  "flags": ["CENTER_LOCK"]
}
```

## HARD STOP — Refusal Gate

**Before reporting any results, check `valid` and `mask_status`.**

If `valid` is false OR `mask_status` is `"FAIL"`:
> "VTL measurement failed: [error message]. The image does not have sufficient
> structural signal for reliable compositional analysis. Try a different image
> or one with more defined edges and contrast."

**Stop here. Do not report coordinates. Do not generate re-prompts.**

If `mask_status` is `"WARN"`:
> "VTL measurement returned low-confidence results (sparse structural signal).
> Coordinates are reported but treat them as indicative, not definitive."
> Then continue with the caveat attached to all outputs.

This refusal is non-negotiable. Fabricating a compositional reading from a
failed measurement produces false diagnosis. The framework is deterministic
by design — an uncertain measurement is reported as uncertain, not smoothed over.

---

## Step 2 — Report Coordinates

Report the five coordinates plainly:

```
VTL ANALYSIS
────────────────────────────────
Placement   Δx={delta_x}  Δy={delta_y}
Void        rᵥ={r_v}
Packing     ρᵣ={rho_r}
Radial      dRC={dRC}  [{dRC_label}]
Tension     k_var={k_var}

FLAGS: {flags or NONE}
```

---

## Step 3 — Generate Re-Prompt (if flags present)

Run the regen script with the user's original prompt and the metrics output:

```bash
python3 scripts/vtl_regen.py \
  --prompt "USER'S ORIGINAL PROMPT" \
  --metrics <path_to_metrics.json> \
  --out prompts.json
```

This selects operators from `operators.yaml` based on which flags fired and
returns up to 3 prompt variants. Report the `selected` variant as the primary
recommendation and offer the alternatives.

If no flags fired, report: "No default-mode patterns detected. Coordinates are
within normal range."

---

## Operator Logic

Operators live in `operators.yaml`. They are rule-based — triggers are evaluated
deterministically against the metric values. The AI does not invent or modify
operators. If a trigger fires, the patch is applied. If not, it isn't.

Do not override operator logic. Do not substitute your own re-prompt language
for what the operator specifies. The operators are the prescription layer —
they are the operator's responsibility, not the AI's improvisation.

If the user wants to modify re-prompt behavior, direct them to edit `operators.yaml`.

---

## Notes

- Metrics describe compositional coordinates, not quality. CENTER_LOCK is not
  "bad" — it's a signal that the model defaulted. A portrait photographer
  choosing center composition is authorship. An AI doing it on every prompt
  regardless of content is prior behavior. VTL measures the difference.
- dRC requires radial eligibility. If mass centroid is very close to frame
  center, dRC is labeled "dual-center" — report the label, not a number
  interpretation.
- Full metric definitions: references/vtl-metrics.md
- Full framework: https://github.com/rusparrish/Visual-Thinking-Lens
- Author: Russell Parrish — https://artistinfluencer.com
