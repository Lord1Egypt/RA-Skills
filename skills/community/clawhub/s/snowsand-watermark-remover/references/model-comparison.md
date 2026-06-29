# IOPaint Model Comparison for Watermark Removal

## Erase Models (Best for Watermarks)

### LaMa (Large Mask inpainting) — Recommended
- **Size:** ~100MB
- **Speed:** Fast (sub-second on GPU)
- **Quality:** Excellent on uniform/simple backgrounds
- **Best for:** Small text watermarks in corners (typical MLS placement)
- **Weakness:** Can leave slight blur on complex textures (patterned carpet, wallpaper)

### MAT (Mask-Aware Transformer) — Alternative
- **Size:** ~100MB
- **Speed:** Fast
- **Quality:** Comparable to LaMa, different artifact patterns
- **Best for:** When LaMa results aren't clean enough — try MAT as second choice

### MIGAN — Lightweight
- **Size:** ~30MB
- **Speed:** Fastest
- **Quality:** Good but lower than LaMa/MAT
- **Best for:** CPU-only systems, low VRAM, quick previews

### LDM — Highest Quality
- **Size:** ~2GB
- **Speed:** Slowest (diffusion-based)
- **Quality:** Best on complex textures
- **Best for:** Difficult backgrounds where LaMa/MAT fail

## Recommendation Order for MLS Watermarks
1. **LaMa** — handles 90%+ of MLS watermarks cleanly
2. **MAT** — if LaMa leaves visible artifacts
3. **LDM** — last resort for complex backgrounds

## Notes
- All erase models are deterministic (same input -> same output)
- Diffusion models (LDM, SD-based) have a seed parameter
- For batch processing, stick to one model for consistency
