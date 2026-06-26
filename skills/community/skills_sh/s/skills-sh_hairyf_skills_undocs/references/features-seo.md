---
name: undocs-seo
description: SEO optimization and Open Graph image generation in undocs
---

# SEO and Open Graph

Undocs provides automatic SEO optimization and Open Graph image generation.

## Automatic SEO

SEO metadata is automatically generated from page frontmatter:

```markdown
---
title: Page Title
description: Page description for SEO
---
```

### Meta Tags

Undocs automatically generates:

- `<title>` - Page title with site name
- `<meta name="description">` - Page description
- `<meta property="og:title">` - Open Graph title
- `<meta property="og:description">` - Open Graph description
- `<meta property="og:image">` - Open Graph image
- `<meta name="twitter:card">` - Twitter card type
- `<link rel="canonical">` - Canonical URL

## Open Graph Images

Open Graph images are automatically generated for each page:

```
/_og/_index.png          # Landing page
/_og/guide.png          # Guide page
/_og/guide/components.png # Components page
```

### OG Image Parameters

OG images include query parameters:

- `name` - Site name
- `title` - Page title
- `description` - Page description

Example: `/_og/guide.png?name=Undocs&title=Guide&description=Getting%20started`

## Page SEO Hook

Use the `usePageSEO` composable for custom SEO:

```typescript
usePageSEO({
  title: `${page.title} - ${site.name}`,
  ogTitle: page.title,
  description: page.description,
});
```

## Site Configuration

SEO is configured via `docs.yaml`:

```yaml
name: "MyPackage"
description: "Package description"
url: "https://example.com"
socials:
  x: "https://x.com/username"
  twitter: "https://twitter.com/username"
```

### Twitter/X Integration

Twitter site is inferred from socials:

```yaml
socials:
  x: "https://x.com/unjsio"
  # or
  twitter: "https://twitter.com/unjsio"
```

## Language Configuration

Set site language:

```yaml
lang: "en"
```

This sets the `lang` attribute on the `<html>` tag.

## Robots.txt

Undocs automatically generates a `robots.txt` file:

```
User-agent: *
Allow: /
```

## Markdown Alternative Links

Pages include alternate markdown links:

```html
<link
  rel="alternate"
  href="/raw/guide.md"
  type="text/markdown"
/>
```

This allows users to access raw markdown via `Accept: text/markdown` header or curl.

## Key Points

- SEO metadata is generated automatically from frontmatter
- Open Graph images are generated for each page
- OG images include site name, title, and description
- Twitter/X cards are automatically configured
- Language is configurable via `lang` option
- Robots.txt is generated automatically
- Markdown alternate links are provided

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/app/composables/usePageSEO.ts
- https://github.com/unjs/undocs/blob/main/app/modules/og-image
-->
