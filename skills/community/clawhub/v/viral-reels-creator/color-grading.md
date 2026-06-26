# Color Grading & Filters Reference

15+ Instagram-inspired color grades using pure ffmpeg filters (no external LUTs needed).
Each grade is a single filter chain you can drop into `-vf` or `-filter_complex`.

---

## Quick Usage

```bash
# Apply any grade:
ffmpeg -i input.mp4 -vf "GRADE_FILTER_HERE" OUTPUT_FLAGS output.mp4

# Combine with other filters:
ffmpeg -i input.mp4 -filter_complex "
  scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,
  GRADE_FILTER_HERE,
  drawtext=...
" OUTPUT_FLAGS output.mp4
```

---

## Warm Tones

### 1. Golden Hour
Warm, sun-kissed look. Great for outdoor/travel reels.
```
eq=brightness=0.06:saturation=1.4:contrast=1.05,
colorbalance=rs=0.15:gs=0.05:bs=-0.1:rm=0.1:gm=0.02:bm=-0.05,
curves=r='0/0 0.25/0.3 0.5/0.58 0.75/0.82 1/1':g='0/0 0.5/0.52 1/1':b='0/0 0.5/0.42 1/0.9',
vignette=PI/5
```

### 2. Sunset Warm
Deep oranges and golden tones.
```
eq=brightness=0.04:saturation=1.5:contrast=1.1,
colorbalance=rs=0.2:gs=0.08:bs=-0.15:rh=0.1:gh=0.02:bh=-0.08,
hue=h=5,
vignette=PI/4
```

### 3. Cozy / Autumn
Muted warm tones with slight desaturation.
```
eq=brightness=0.03:saturation=0.9:contrast=1.1,
colorbalance=rs=0.12:gs=0.04:bs=-0.08:rm=0.08:gm=0.02:bm=-0.05,
curves=master='0/0.05 0.25/0.22 0.5/0.5 0.75/0.78 1/0.95',
vignette=PI/4.5
```

---

## Cool Tones

### 4. Ice Blue / Winter
Cold, blue-tinted aesthetic.
```
eq=brightness=0.04:saturation=0.85:contrast=1.15,
colorbalance=rs=-0.1:gs=-0.02:bs=0.18:rm=-0.05:gm=0:bm=0.1,
curves=b='0/0.1 0.5/0.55 1/1',
vignette=PI/5
```

### 5. Moonlight / Night
Deep blue shadows, cool midtones.
```
eq=brightness=-0.05:saturation=0.7:contrast=1.2,
colorbalance=rs=-0.08:gs=-0.03:bs=0.15:rm=-0.05:gm=-0.02:bm=0.08:rh=-0.02:gh=-0.01:bh=0.05,
curves=master='0/0 0.25/0.18 0.5/0.48 0.75/0.78 1/0.95',
vignette=PI/3.5
```

### 6. Teal & Orange (Hollywood)
Classic cinema color grade — teal shadows, orange highlights.
```
eq=saturation=1.3:contrast=1.15,
colorbalance=rs=-0.08:gs=-0.02:bs=0.12:rm=0.05:gm=-0.02:bm=-0.08:rh=0.12:gh=0.04:bh=-0.1,
curves=r='0/0 0.5/0.55 1/1':b='0/0.08 0.5/0.45 1/0.9',
vignette=PI/4.5
```

---

## Vintage & Film

### 7. Retro Film / Kodak
Warm, slightly faded film look.
```
eq=brightness=0.03:saturation=0.85:contrast=1.05,
curves=master='0/0.06 0.15/0.18 0.5/0.52 0.85/0.85 1/0.94':
  r='0/0.03 0.5/0.54 1/1':b='0/0 0.5/0.46 1/0.92',
noise=alls=15:allf=t,
vignette=PI/4
```

### 8. Polaroid / Instant
Faded highlights, slight green-yellow tint.
```
eq=brightness=0.05:saturation=0.75:contrast=0.95,
colorbalance=rs=0.05:gs=0.08:bs=-0.03:rm=0.03:gm=0.05:bm=-0.02,
curves=master='0/0.08 0.5/0.55 1/0.92',
vignette=PI/3.5
```

### 9. Black & White Classic
High-contrast monochrome.
```
hue=s=0,
eq=contrast=1.3:brightness=0.02,
curves=master='0/0 0.2/0.12 0.5/0.5 0.8/0.88 1/1',
vignette=PI/4
```

### 10. Sepia
Classic brown-toned monochrome.
```
hue=s=0,
colorbalance=rs=0.15:gs=0.08:bs=-0.05:rm=0.1:gm=0.05:bm=-0.03,
eq=contrast=1.1:brightness=0.03,
vignette=PI/4.5
```

---

## Moody & Dramatic

### 11. Dark Moody
Crushed blacks, desaturated, dramatic.
```
eq=brightness=-0.06:saturation=0.65:contrast=1.3,
curves=master='0/0 0.15/0.05 0.5/0.45 0.85/0.82 1/0.95',
colorbalance=rs=-0.03:gs=-0.02:bs=0.05:rm=0.02:gm=-0.01:bm=-0.02,
vignette=PI/3
```

### 12. Cyberpunk / Neon
High saturation, magenta-cyan push.
```
eq=brightness=0.02:saturation=1.8:contrast=1.25,
colorbalance=rs=0.1:gs=-0.08:bs=0.15:rm=-0.05:gm=0.03:bm=0.1:rh=0.08:gh=-0.05:bh=0.12,
curves=master='0/0 0.3/0.22 0.5/0.52 0.7/0.78 1/1',
vignette=PI/4
```

### 13. Faded Pastel
Lifted blacks, soft pastel tones.
```
eq=brightness=0.08:saturation=0.6:contrast=0.85,
curves=master='0/0.12 0.25/0.32 0.5/0.55 0.75/0.78 1/0.95':
  r='0/0.05 0.5/0.55 1/1':g='0/0.03 0.5/0.52 1/0.98':b='0/0.06 0.5/0.53 1/0.97',
vignette=PI/5
```

---

## Special Effects Grades

### 14. High Key (bright, airy)
```
eq=brightness=0.12:saturation=0.8:contrast=0.9,
curves=master='0/0.1 0.3/0.4 0.5/0.6 0.8/0.9 1/1',
vignette=PI/6
```

### 15. Low Key (dark, dramatic shadows)
```
eq=brightness=-0.1:saturation=0.75:contrast=1.4,
curves=master='0/0 0.2/0.08 0.5/0.4 0.8/0.75 1/0.9',
vignette=PI/3
```

### 16. Cross-Process (experimental color shift)
```
curves=r='0/0.1 0.4/0.5 0.6/0.55 1/0.9':
  g='0/0 0.3/0.35 0.7/0.65 1/1':
  b='0/0.15 0.5/0.4 0.8/0.85 1/0.95',
eq=saturation=1.2:contrast=1.15,
vignette=PI/4
```

### 17. Duotone (two-color grade)
```
# Teal and magenta duotone
hue=s=0,
curves=r='0/0.1 0.5/0.3 1/0.9':g='0/0.05 0.5/0.5 1/0.6':b='0/0.15 0.5/0.55 1/0.95',
eq=contrast=1.2
```

---

## Instagram Filter Clones

### 18. "Clarendon" Style (bright, high contrast, blue tint)
```
eq=brightness=0.06:saturation=1.35:contrast=1.2,
colorbalance=rs=-0.03:gs=-0.01:bs=0.08:rm=0:gm=0:bm=0.04,
curves=master='0/0 0.2/0.25 0.5/0.55 0.8/0.88 1/1',
vignette=PI/5
```

### 19. "Juno" Style (warm highlights, cool shadows)
```
eq=brightness=0.04:saturation=1.3:contrast=1.1,
colorbalance=rs=-0.05:gs=-0.03:bs=0.08:rh=0.1:gh=0.05:bh=-0.05,
curves=master='0/0 0.25/0.28 0.5/0.55 1/1',
vignette=PI/5
```

### 20. "Lark" Style (bright, desaturated, blue shadows)
```
eq=brightness=0.08:saturation=0.8:contrast=1.05,
colorbalance=rs=-0.06:gs=-0.02:bs=0.1:rm=0.02:gm=0.02:bm=-0.01,
curves=master='0/0.05 0.5/0.58 1/0.98'
```

---

## Adjustment Quick Reference

| Adjustment     | ffmpeg filter                              | Range          |
|----------------|--------------------------------------------|----------------|
| Brightness     | `eq=brightness=0.05`                       | -1.0 to 1.0   |
| Contrast       | `eq=contrast=1.2`                          | 0.0 to 2.0    |
| Saturation     | `eq=saturation=1.3`                        | 0.0 to 3.0    |
| Hue shift      | `hue=h=10`                                 | -180 to 180°  |
| Gamma          | `eq=gamma=1.2`                             | 0.1 to 10.0   |
| Sharpen        | `unsharp=5:5:1.0:5:5:0.0`                | varies         |
| Blur           | `avgblur=5`                                | 1 to 100       |
| Noise (grain)  | `noise=alls=20:allf=t`                    | 0 to 100       |
| Vignette       | `vignette=PI/4`                            | PI/2 to PI/20  |
| Temperature    | `colorbalance=rs=0.1:bs=-0.1` (warmer)    | -1.0 to 1.0   |
