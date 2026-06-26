---
name: undocs-landing-page
description: Landing page configuration and customization in undocs
---

# Landing Page

Undocs provides a configurable landing page with hero section, features, contributors, and sponsors.

## Enable/Disable

### Disable Landing

Set `landing: false` to remove the landing page. The index route will be removed; use a redirect to point `/` elsewhere:

```yaml
# .config/docs.yaml
landing: false
redirects:
  "/": "/guide"
```

## Hero Section

### Default Hero Links

When not overridden, hero links default to:

- **primary**: "Get Started" → `/guide`
- **github**: "View on GitHub" → `https://github.com/{github}`

### Custom Hero Links

```yaml
landing:
  heroLinks:
    primary:
      label: "Get Started"
      icon: "i-heroicons-rocket-launch"
      to: "/guide"
      order: 0
    stackblitz:
      icon: "i-heroicons-play"
      to: "https://stackblitz.com/..."
    github:
      label: "View on GitHub"
      icon: "i-simple-icons-github"
      to: "https://github.com/owner/repo"
      target: "_blank"
      order: 100
```

Link can be string (just `to`) or object with `label`, `icon`, `to`, `target`, `order`.

### Hero Code

Display a code snippet in the hero:

```yaml
landing:
  heroCode: "npx giget gh:unjs/undocs/template docs"
  # or
  heroCode:
    content: "npx giget gh:unjs/undocs/template docs"
    lang: "sh"
    title: "Terminal"
```

Code is highlighted with Shiki (github-dark/light themes).

### Hero Titles

```yaml
landing:
  heroTitle: "Package Name"      # Main title (default: name)
  heroSubtitle: "Short tagline"  # Subtitle (default: shortDescription)
  heroDescription: "..."         # Description (default: description)
```

### Features in Hero

When `heroCode` is not set and `featuresLayout: "hero"`:

- Features display inline in the hero (horizontal layout)
- Use when you want features instead of code snippet

## Features Section

```yaml
landing:
  features:
    - title: "Easy to use"
      icon: "⚡"   # Emoji or icon name (e.g. "logos:nuxt-icon")
      description: "Focus on writing *documentation* with Markdown."
```

- **icon**: Emoji (rendered as text) or icon name (e.g., `i-logos-nuxt-icon`)
- **description**: Markdown supported (rendered via md4w)

### Features Layout

```yaml
landing:
  featuresLayout: "default"  # or "hero"
```

- **default**: Features in separate section below hero
- **hero**: Features inline in hero (only when no heroCode)

### Features Title

```yaml
landing:
  featuresTitle: "Features"  # Section title (default: empty)
```

## Latest Blog Post

When blog exists, landing shows "Latest" button linking to most recent post:

```
queryCollection("content").where("path", "LIKE", "/blog/%").order("id", "DESC").first()
```

## Sections Order

1. Hero (title, description, links, code or features)
2. Features section (if featuresLayout is default)
3. Sponsors (if sponsors.api set)
4. Contributors (if landing.contributors true)

## Key Points

- `landing: false` removes landing page
- heroLinks: primary and github by default
- heroCode: string or object with content, lang, title
- featuresLayout: "default" or "hero"
- features support emoji or icon name, markdown description

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/app/pages/index.vue
- https://github.com/unjs/undocs/blob/main/schema/config.json
- https://github.com/unjs/undocs/blob/main/app/modules/content/index.ts
-->
