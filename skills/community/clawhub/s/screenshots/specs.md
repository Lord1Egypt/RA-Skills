# Screenshot Specifications

## Apple App Store

### Required iPhone Sizes
| Display | Devices | Dimensions (px) | Aspect |
|---------|---------|-----------------|--------|
| 6.7" | iPhone 15 Pro Max, 14 Pro Max | 1290 × 2796 | 9:19.5 |
| 6.5" | iPhone 14 Plus, 11 Pro Max, XS Max | 1242 × 2688 | 9:19.5 |
| 5.5" | iPhone 8 Plus, 7 Plus, 6s Plus | 1242 × 2208 | 9:16 |

### Required iPad Sizes
| Display | Devices | Dimensions (px) |
|---------|---------|-----------------|
| 12.9" (3rd gen+) | iPad Pro 12.9" | 2048 × 2732 |
| 12.9" (2nd gen) | iPad Pro 12.9" 2017 | 2048 × 2732 |
| 11" | iPad Pro 11", Air (5th gen) | 1668 × 2388 |

### Format Requirements
- **Format:** PNG or JPEG (PNG preferred)
- **Color space:** sRGB or P3
- **Max file size:** 500 KB per screenshot (compressed)
- **Quantity:** 1-10 screenshots per localization
- **No alpha/transparency** — will be rejected

### Safe Zones
- **Top:** 44px (status bar area)
- **Bottom:** 34px (home indicator on notched devices)
- **Corners:** Avoid placing critical text in corners (rounded displays)

---

## Google Play Store

### Phone Screenshots
| Type | Dimensions | Notes |
|------|------------|-------|
| Phone | 1080 × 1920 to 1080 × 2400 | 16:9 to 9:20 aspect |
| Minimum | 320px shortest side | |
| Maximum | 3840px any side | |

### Tablet Screenshots
| Type | Dimensions | Notes |
|------|------------|-------|
| 7" tablet | 1200 × 1920 | Optional |
| 10" tablet | 1600 × 2560 | Optional |

### Feature Graphic
- **Required:** 1024 × 500 px
- **Used in:** Play Store header, promotional spots
- **No text in edges** — may be cropped

### Format Requirements
- **Format:** PNG or JPEG
- **Max file size:** 8 MB per image
- **Quantity:** 2-8 screenshots (minimum 2)

---

## Generation Strategy

### From Raw Captures

1. **Capture at highest resolution** (iPhone 15 Pro Max simulator)
2. **Generate smaller sizes by scaling down:**
   - 6.7" → source
   - 6.5" → scale + adjust margins
   - 5.5" → scale + center crop (different aspect ratio)

### Aspect Ratio Handling

When source aspect ≠ target aspect:
- **Letterbox:** Add background bars (preserves full content)
- **Center crop:** Cut edges (loses content, looks cleaner)
- **Scale + reframe:** Adjust text overlay positions per size

Default: letterbox with gradient background matching app colors.

---

## Pre-Upload Validation

Check before upload:
- [ ] All required sizes present
- [ ] No transparency
- [ ] File sizes under limits
- [ ] No placeholder/debug text visible
- [ ] No status bar with wrong time/carrier
- [ ] Device frame matches target device
