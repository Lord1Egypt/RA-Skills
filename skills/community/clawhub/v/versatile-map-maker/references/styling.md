# Styling And Accessibility

Use clear, restrained map styling. The map should communicate data first.

## Choropleth Defaults

- Numeric data: sequential palette such as `YlOrRd`, `Blues`, `Greens`, or `viridis`.
- Diverging data: use a diverging palette only when values have a meaningful midpoint.
- Categories: use distinct qualitative colors; avoid too many categories.
- Missing data: neutral light gray with an explicit note when absence matters.

## Accessibility

- Prefer colorblind-safer palettes for public-facing maps.
- Avoid encoding important distinctions only through subtle hue changes.
- Keep strokes light enough not to overpower the fill.
- Use short labels; move long explanations to the caption.

## Output Polish

- Expand the SVG viewBox for titles and legends.
- Render and inspect a PNG preview before delivery.
- Check mobile or small-size readability when the map will be embedded online.

