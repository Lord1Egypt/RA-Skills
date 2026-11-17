# Style Extraction Checklist

`design-properties.json` keeps two layers:

- `raw`: Figma-like fields, trimmed and redacted.
- `normalized`: web-friendly values that the script can determine.

Important fields:

- Size and position: `x`, `y`, `width`, `height`, constraints, layout sizing.
- Auto layout and spacing: `layoutMode`, alignments, `itemSpacing`, padding, wrap.
- Text: characters, font family, style, weight, size, line height, letter spacing, alignments, mixed style ranges.
- Colors: fills, strokes, background, opacity, blend mode, RGBA, CSS `rgba(...)`, hex.
- Shape: border, radius, corner radii, shadow, blur.
- Components: component id/key/name, variant properties, component properties, overrides.
- `inferredSpacing`: spacing inferred from sibling or parent geometry. Figma has no native CSS margin field.

`css-hints.css` is reference material only. Prefer existing local design-system components, tokens, Tailwind values, and style variables before copying any raw pixel or color value.

If a value is uncertain, the script writes `null` or a comment. It must not invent deterministic CSS for uncertain Figma fields such as `lineHeight: AUTO`.
