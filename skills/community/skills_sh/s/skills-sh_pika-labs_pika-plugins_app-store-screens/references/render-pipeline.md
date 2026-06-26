# Render Pipeline

How to take an HTML stage and produce a 1290x2796 PNG that is deliverable to App Store Connect.

## Renderer

Use Pika MCP `html_to_png`. It runs server-side Chromium and returns a hosted PNG URL. Do not run local Chrome headless by default.

Production request shape:

```
html_to_png(
  html: screen_html,
  format: "png",
  mode: "async",
  wait_for: "domcontentloaded",
  raster_options: {
    viewport_px: { width: 1290, height: 2796 },
    device_scale: 1
  }
)
```

Use `mode:"sync"` only for quick one-page checks. Production screenshots are large; async is safer.

Example completed response:

```
{"status":"completed","file_url":"https://cdn.pika.art/v2/files/agent/4d944981-9897-40b6-9e37-533c2a90b541/5a863672-0835-4901-87a8-df8933d69cd4.png","format":"png","page_count":1,"byte_size":3806}
```

## Asset Rules

Server-side Chromium cannot read local `file://` paths. Every image/font in the HTML must be one of:

- HTTPS URL returned by Pika tools
- Public HTTPS raw asset URL
- Inline `data:` URI

For local screenshots, product photos, or generated local artifacts, call `upload_asset` first and use the returned `public_url`.

`upload_asset` does not accept font files, so fonts need public HTTPS raw URLs or inline `data:font/...` sources.

JavaScript is disabled by default in the renderer. Build static HTML/CSS stages; do not depend on runtime JS for layout.

## Stage Sizing

The HTML must declare an exact 1290x2796 canvas. Do not use viewport units (`vh`/`vw`) for the stage.

Top of every screen HTML:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; padding: 0; background: #000; }
    .stage {
      width: 1290px;
      height: 2796px;
      position: relative;
      overflow: hidden;
    }
  </style>
</head>
<body>
  <div class="stage">
    <!-- screen content -->
  </div>
</body>
</html>
```

The black body background is a guardrail. If the stage does not fill the render, black bleed makes the sizing bug obvious.

## Apple Safe Zones

App Store Connect overlays its own chrome on screenshots in certain views. Keep critical content inside the safe area.

```
0px        +---------------------------+
           | decoration only            | top 100px
100px      +---------------------------+
           |                           |
           | SAFE CONTENT ZONE         |
           |                           |
2696px     +---------------------------+
           | decoration only            | bottom 100px
2796px     +---------------------------+
```

Visuals can live in the top/bottom 100px bands. Load-bearing headlines and product UI cannot.

Strict text margin: text block bounding boxes for headlines, eyebrows, subheads,
CTA text, labels, and any product UI must be fully inside y=180..2616. The top
and bottom 100px bands are hard no-go zones; the extra 80px gives breathing room
for status-bar chrome, App Store search-result cropping, and text ascenders. If
a safe-zone audit finds load-bearing text with y < 180, or a block bottom past
y=2616, reject and rerender.

## Device Compositing

Preferred source:

- Transparent PNG export from Figma/simulator
- Individual phone screenshots, not a strip
- High enough resolution that scaling to 1000px width does not blur text

Default CSS:

```html
<div class="device" style="
  position: absolute;
  top: 580px;
  left: 50%;
  transform: translateX(-50%);
  width: 1000px;
  border-radius: 96px;
  overflow: hidden;
  filter: drop-shadow(0 80px 100px rgba(28,26,24,0.22));
">
  <img src="https://cdn.pika.art/..." style="
    width: 100%;
    display: block;
  ">
</div>
```

If the source PNG already has transparent rounded corners, remove `border-radius` and `overflow:hidden` and let the alpha channel define the shape.

Current MCP gap: there is no server-side uniform rounded-corner cleaner equivalent to the old local `clean_phone_uniform()` PIL recipe. If Figma source PNGs contain gray/colored corner triangles, ask for transparent exports or use a real phone mockup cutout. CSS masking is acceptable for iteration, but visually QA every corner because it can reveal source-background artifacts.

Position rule:

- Full-frame default: `top:580px`, `width:1000px`, bottom lands at about y=2748 with breathing room.
- Bleed variant: `top >= 819`, so the rounded bottom curve is fully past y=2796.
- Avoid any value between 581 and 818 for bleed layouts; it slices through the bottom corner mid-curve.

For tilt, wrap the device in `transform: translateX(-50%) rotate(-3deg)`. Stay under 5 degrees unless the brand is deliberately playful.

## Font Loading

Fonts that do not load make the campaign look broken. Use explicit `@font-face` declarations:

```css
@font-face {
  font-family: 'BrandDisplay';
  src: url('https://github.com/google/fonts/raw/main/ofl/fraunces/Fraunces%5Bopsz,wght%5D.ttf') format('truetype');
  font-weight: 300 900;
}
```

Inline data URI fonts are also acceptable:

```css
@font-face {
  font-family: 'BrandDisplay';
  src: url('data:font/ttf;base64,...') format('truetype');
}
```

Avoid Google Fonts `@import` chains; explicit URLs are easier for the server renderer to prefetch and inline. After the first render, inspect the screenshot before generating the rest. If type falls back to a system face, fix the font source first.

## Retina Sharpness

Text in App Store screenshots needs to look crisp on a 6.9-inch device. `viewport_px:1290x2796` and `device_scale:1` produce the exact final pixel size.

If text looks fuzzy:

- Check `.stage` is exactly 1290x2796.
- Check `raster_options.viewport_px` is exactly 1290x2796.
- Check `device_scale` is 1.
- Check no CSS `transform: scale()` is shrinking text and then scaling it back up.

## Image Asset Prep

When `generate_image` returns a hosted URL, use it directly in HTML. When the user provides local files, upload them first:

```
upload_asset(filename:"screen.png", mime_type:"image/png", size_bytes:<size>)
# PUT bytes to presigned_url
# Use public_url in <img src="...">
```

Remote assets sometimes fail if they block server requests. In that case, upload the file through Pika and use the returned CDN URL.

## Contact Sheet

After all six individual PNGs render, build a `_preview.png` contact sheet with one more `html_to_png` call. Use the six returned PNG URLs in a 3x2 grid.

```html
<div style="
  width: 2400px;
  min-height: 1800px;
  background: #f5f0e6;
  padding: 80px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
">
  <div>
    <img src="https://cdn.pika.art/.../01_hook.png" style="width: 100%; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
    <p style="font-family: sans-serif; font-size: 18px; margin-top: 12px; opacity: 0.6;">1 - Hook</p>
  </div>
  <!-- repeat for 02-06 -->
</div>
```

Render with a contact-sheet viewport large enough for the grid, usually `2400x1900` or taller if labels wrap.

## Pre-delivery Checklist

Before handing files to the user, verify:

- [ ] Every individual PNG is exactly 1290x2796.
- [ ] Brand fonts loaded, not system fallbacks.
- [ ] No black bleed at edges.
- [ ] Safe-zone audit passes: no load-bearing text block bounding boxes at y < 180 or past y=2616; reject and rerender failures.
- [ ] Device corners look consistent across all six.
- [ ] First two screens are legible when viewed at 25%.
- [ ] Contact sheet shows visual variety across the six.
- [ ] All six use colors from `brand.md`'s palette.
- [ ] Real app UI appears in the device area; no hallucinated placeholder UI.
