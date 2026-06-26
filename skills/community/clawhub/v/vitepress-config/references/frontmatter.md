# Frontmatter Config Reference

> Source: https://vitepress.dev/reference/frontmatter-config

Frontmatter enables page-based configuration. Access via `$frontmatter` global in Vue expressions.

## Basic Options

| Option | Type | Overrides |
|--------|------|-----------|
| `title` | `string` | `config.title` |
| `titleTemplate` | `string \| boolean` | `config.titleTemplate` |
| `description` | `string` | `config.description` |
| `head` | `HeadConfig[]` | Appended after site-level |

## Default Theme Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `layout` | `doc \| home \| page` | `doc` | Page layout |
| `navbar` | `boolean` | `true` | Show navbar |
| `sidebar` | `boolean` | `true` | Show sidebar |
| `aside` | `boolean \| 'left'` | `true` | Aside position |
| `outline` | `number \| [n,n] \| 'deep' \| false` | `2` | Outline levels |
| `lastUpdated` | `boolean \| Date` | `true` | Show last updated |
| `editLink` | `boolean` | `true` | Show edit link |
| `footer` | `boolean` | `true` | Show footer |
| `pageClass` | `string` | - | Custom page class |

## Layouts

- **`doc`** - Default documentation styling with aside, edit link, prev/next
- **`home`** - Homepage layout with hero and features sections
- **`page`** - Blank page, no default styles
- **`false`** - No layout at all

## Examples

### Basic

```yaml
---
title: My Page
description: Page description
---
```

### Home Page

```yaml
---
layout: home

hero:
  name: VitePress
  text: Vite & Vue powered static site generator.
  tagline: Build fast docs sites
  image:
    src: /logo.png
    alt: Logo
  actions:
    - theme: brand
      text: Get Started
      link: /guide/getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/vuejs/vitepress

features:
  - icon: 🛠️
    title: Simple and minimal
    details: Lorem ipsum dolor sit amet
  - icon:
      src: /feature-icon.svg
    title: Another feature
    details: More description here
---
```

### Custom Page Class

```yaml
---
pageClass: custom-layout
---
```

Then in CSS:

```css
.custom-layout {
  /* page-specific styles */
}
```

## Accessing Frontmatter

In Markdown:

```md
# {{ $frontmatter.title }}
```

In Vue:

```vue
<script setup>
import { useData } from 'vitepress'
const { frontmatter } = useData()
</script>
```

## Alternative Formats

JSON frontmatter:

```json
---
{
  "title": "Blogging Like a Hacker",
  "editLink": true
}
---
```
