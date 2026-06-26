# Design Guidelines

## Visual style

- Dark card background with soft gradient header
- Clear title and short subtitle
- High-contrast QR area (white background)
- Footer with payload preview

## Payload defaults

- Prefer `clawhub install <slug>` for fastest user success
- Use direct URL mode when users scan on desktop and open browser first

## File naming

- Use timestamp + slug: `yyyy-mm-dd-hh-mm-<slug>-qr-card.svg`

## Safety

- Validate slug to lowercase/url-safe pattern
- Avoid embedding secrets/tokens in payload
