# Website Development Rules

## Visual Design (MOST IMPORTANT)

Sites MUST look distinctive and professionally designed.
Generic, template-like output is a failure.

### Typography
- Use real fonts from Google Fonts — never rely on system defaults
- Pick a display font for headings + a readable font for body
- Font sizes: hero 3-5rem, headings 1.5-2.5rem, body 1-1.125rem
- Use font-weight variation (300, 400, 600, 800) for hierarchy
- Letter-spacing on uppercase text: 0.05-0.1em

### Color
- Define a cohesive palette: 1 primary, 1 accent, 1-2 neutrals
- Store as CSS custom properties (--color-primary, etc.)
- Use gradients for backgrounds and CTAs — not flat solid colors
- AVOID: purple-on-white, all-gray, generic blue (#007bff)
- Dark sections + light sections = visual rhythm
- Accent color should appear in at least 3 places

### Layout & Depth
- Generous whitespace — padding 4-8rem between sections
- Asymmetric layouts are more interesting than centered grids
- Add depth: subtle shadows, overlapping elements, layered bg
- Use CSS Grid for complex layouts, not just centered columns
- Hero sections should be full-viewport and bold
- Break the grid occasionally — offset images, angled dividers

### Motion & Interaction
- 1-2 strong CSS animations: fade-in on scroll, hover transforms
- Smooth transitions on all interactive elements (0.2-0.3s ease)
- Subtle hover effects on cards/buttons (scale, shadow, color)
- Consider a gradient animation or floating element for hero
- Do NOT overdo — motion should enhance, not distract

### Photography (Unsplash via proxy)

Every site MUST include real, topically relevant photos.

**How to get images:**
Search for relevant photos via the image proxy (no auth needed):

```bash
# Search for photos by keyword
curl -s "https://publish.vvvlink.com/images/search?q=KEYWORD&count=5"

# With orientation filter
curl -s "https://publish.vvvlink.com/images/search?q=office&count=3&orientation=landscape"
```

Response:
```json
{
  "photos": [
    {
      "id": "abc123",
      "url": "https://images.unsplash.com/photo-...",
      "thumb": "https://images.unsplash.com/photo-...&w=400",
      "alt": "description of the photo",
      "credit": "Photographer Name",
      "credit_url": "https://unsplash.com/@photographer",
      "width": 5472,
      "height": 3648
    }
  ]
}
```

**CRITICAL: Response field is `photos`, NOT `results`.**
Parse with: `response.photos[0].url` — not `response.results`.

**Workflow:**
1. Analyze site content — pick 3-6 keywords (hero, about, features)
2. Search each keyword via the proxy
3. Parse response: access `.photos[]` array (NOT `.results[]`)
4. Use the `.url` field directly in `<img src="...">`
5. Use `.alt` field from the response as alt text
6. Do NOT add photo credits in the footer

**Usage in HTML:**
```html
<!-- Use the FULL url from .photos[].url — append size params -->
<img src="https://images.unsplash.com/photo-ABC?ixid=XYZ&w=1600&h=900&fit=crop"
     alt="description from .alt field"
     width="1600" height="900" loading="lazy">
```

**Verify before publish:** After building the HTML, check that
every `<img src="...">` contains a full Unsplash URL starting
with `https://images.unsplash.com/photo-`. If any src is empty,
broken, or a placeholder — fix it before uploading.

**Size control — use the `url` from search results as-is, then
append size params. The URL already has `?` with query params,
so always append with `&`:**
- Hero: append `&w=1600&h=900&fit=crop`
- Cards: append `&w=600&h=400&fit=crop`
- Avatars: append `&w=300&h=300&fit=crop`
- Thumbnails: append `&w=400&h=300&fit=crop`

**IMPORTANT:** Never strip the existing query string from the
Unsplash URL. The full URL with all its params is required for
the image to load. Just append your size params to the end.

**Rules:**
- Always search with relevant keywords, not generic terms
- Always set width/height attributes to prevent layout shift
- Always use `loading="lazy"` for below-the-fold images
- Do NOT add photographer credits or "Photos by ... on Unsplash"
- Use object-fit: cover for consistent framing
- Apply CSS filters (brightness, contrast) to match site palette
- Layer text over photos with semi-transparent overlays

**Where to use photos:**
- Hero section (full-width background or large feature image)
- About/team section (portraits or workspace)
- Feature cards (illustrative thumbnails)
- Testimonial backgrounds
- Gallery/portfolio sections

### Visual Elements
- Use SVG icons (inline or sprite) — never emoji as design
- Decorative shapes: blobs, circles, diagonal sections
- Combine CSS art/gradients WITH real photos for best results
- Favicon is REQUIRED — generate an inline SVG favicon that
  matches the site's brand/topic and embed it in the HTML head:
  ```html
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>☕</text></svg>">
  ```
  Or use a proper SVG shape with the site's accent color:
  ```html
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><circle cx='16' cy='16' r='14' fill='%23e63946'/></svg>">
  ```
  Pick an approach that matches the site. Emoji works for
  simple cases, custom SVG shape for more polished sites
- Use ::before/::after pseudo-elements for decorative touches

### Anti-Patterns (NEVER do these)
- Plain white background with black text and no color
- Generic Bootstrap/Tailwind default look
- Centered single-column with no visual interest
- Stock placeholder text without styling
- Buttons that look like default browser buttons
- No hover effects on interactive elements
- All sections looking identical in structure

## Performance
- Inline critical CSS in <head>, defer the rest
- Lazy-load images below the fold
- Use font-display: swap and preload critical fonts
- Load third-party scripts with async/defer

## Mobile First
- Start with mobile styles, use min-width media queries
- Touch targets: 44x44px minimum
- No horizontal scroll — test at 320px width
- Required: <meta name="viewport" content="width=device-width, initial-scale=1">

## Accessibility
- Every <img> needs alt text (empty alt="" for decorative)
- Color contrast ratio 4.5:1 minimum for body text
- Form inputs must have <label> elements
- Keyboard navigation must work for all interactive elements
- Heading hierarchy: H1-H6 in logical order, never skip

## HTML Structure
- One <h1> per page
- Semantic elements: <nav>, <main>, <article>, <aside>, <footer>
- <button> for actions, <a> for navigation
- External links: rel="noopener" with target="_blank"

## CSS Patterns
- No !important — fix specificity instead
- Relative units (rem, em, %) for text
- CSS custom properties for colors, spacing, fonts
- Flexbox for 1D, Grid for 2D layouts

## Before Publish
- Favicon included
- <html lang="..."> set correctly
- Open Graph meta tags for social sharing
- All links use https://
- Verify all `<img src>` URLs are valid Unsplash URLs (not empty/placeholder)
- If updating an existing site, images may be cached by CDN/browser
