# Product Launch Page - HTML Template

## When to Use

- User wants a polished launch or landing page in HTML
- Page should emphasize product value proposition and trust signals
- Output must stay static and sanitized (no forms or script behavior)

## Required Sections

1. Hero block with product name, tagline, and one callout metric
2. Feature grid with 3-6 concise feature cards
3. Metrics band with 3-5 KPI cards and directional deltas
4. One visual insight section (CSS/SVG only)
5. Social proof area (testimonial or proof quote)
6. Footer support cards or next-step links

## Optional Sections

- Integration logos strip
- Pricing preview cards (static only)
- FAQ snippet block

## Component Interaction Contract

- Hero message defines what all lower sections reinforce
- Feature grid explains how value is delivered
- Metrics band and visual block establish credibility
- Testimonial section should echo one of the top value claims
- Footer cards convert attention into clear next actions

## Styling Contract

- Single-page container with `max-width` around `1100px`
- Compact spacing, card-based grouping, clear hierarchy
- Use CSS variables for theme colors and semantic accents
- Responsive breakpoints for desktop, tablet, and mobile
- Keep typography dense but readable

## HTML Constraints

- No scripts, forms, buttons, input fields, or interactive widgets
- Links are allowed via `<a>`
- Use semantic sections where possible (`section`, `header`, `footer`)

## Scaffold Template

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{Product Name} - {Primary Value Prop}</title>
  <style>
    :root {
      --primary: {primary-color};
      --accent: {accent-color};
      --bg: {background-color};
      --text: {text-color};
      --border: {border-color};
      --success: {positive-color};
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
    .container { max-width: 1100px; margin: 0 auto; padding: 1rem; }

    /* Add compact card-first styles for:
       hero, features, metrics, visual section, testimonial, footer */
  </style>
</head>
<body>
  <div class="container">
    <section class="hero">
      <h1>{Product Name}</h1>
      <p>{Tagline}</p>
      <p>{Proof callout}</p>
    </section>

    <section class="features">
      <!-- Repeat feature cards -->
      <article>{Feature 1}</article>
      <article>{Feature 2}</article>
      <article>{Feature 3}</article>
    </section>

    <section class="metrics-band">
      <!-- KPI cards -->
      <article>{KPI 1 + delta}</article>
      <article>{KPI 2 + delta}</article>
      <article>{KPI 3 + delta}</article>
    </section>

    <section class="visual-section">
      <!-- CSS/SVG-only visual summary -->
      {Static visual representation}
    </section>

    <section class="testimonial">
      <blockquote>{Customer quote}</blockquote>
      <p>{Name, role, company}</p>
    </section>

    <footer class="footer-cards">
      <article>{Next step 1}</article>
      <article>{Next step 2}</article>
      <article>{Next step 3}</article>
    </footer>
  </div>
</body>
</html>
```

## Validation Checklist

- All content blocks are grounded in provided user context
- No forbidden interactive HTML elements
- Visual section works without JavaScript
- Layout remains readable on mobile widths
- No empty placeholder sections in final generated output
