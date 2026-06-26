# SEO Meta Tag Optimizer

Analyze and generate optimized meta tags, Open Graph tags, Twitter Cards, and JSON-LD structured data for any web page. Boost search engine visibility and social media sharing.

## When to use

Use this skill when the user needs to:
- Generate meta tags for a web page or blog post
- Create Open Graph tags for social media sharing
- Add Twitter Card markup
- Generate JSON-LD structured data (Article, Product, FAQ, Organization, etc.)
- Audit existing meta tags for SEO issues
- Optimize title tags and meta descriptions for click-through rate

## How it works

1. Ask the user for the page URL or content details (title, description, type of page)
2. Determine the page type (article, product, FAQ, homepage, etc.)
3. Generate all required meta tags
4. Provide character count validation (title: 50-60 chars, description: 150-160 chars)
5. Output copy-paste ready HTML

## Meta Tags to Generate

### Basic Meta Tags
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Optimized title - 50-60 characters]</title>
<meta name="description" content="[150-160 characters]">
<meta name="robots" content="index, follow">
<link rel="canonical" href="[URL]">
```

### Open Graph Tags
```html
<meta property="og:title" content="">
<meta property="og:description" content="">
<meta property="og:type" content="website|article|product">
<meta property="og:url" content="">
<meta property="og:image" content="">
<meta property="og:site_name" content="">
<meta property="og:locale" content="">
```

### Twitter Card Tags
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="">
<meta name="twitter:description" content="">
<meta name="twitter:image" content="">
<meta name="twitter:site" content="@handle">
```

### JSON-LD Structured Data

Generate appropriate schema based on page type:
- **Article**: headline, author, datePublished, image
- **Product**: name, description, price, availability, review
- **FAQ**: mainEntity with Question/Answer pairs
- **Organization**: name, url, logo, contactPoint
- **BreadcrumbList**: navigation hierarchy
- **WebSite**: search action for sitelinks

## Validation Rules

- Title: 50-60 characters (warn if outside range)
- Meta description: 150-160 characters
- OG image: recommend 1200x630px minimum
- Canonical URL: must be absolute URL
- JSON-LD: validate against schema.org specs
- No duplicate meta tags

## Output Format

Provide the complete HTML snippet ready to paste into `<head>`:
1. Basic meta tags
2. Open Graph tags
3. Twitter Card tags
4. JSON-LD script block
5. Character count summary with pass/warn indicators

## Example

User: "Generate meta tags for my blog post about 'Best Free Invoice Generators in 2026'"

Response: Complete set of meta tags with optimized title, description, OG tags, Twitter Card, and Article JSON-LD with proper schema.org markup.
