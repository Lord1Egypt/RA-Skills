---
name: undocs-configuration
description: Configure undocs documentation site using docs.yaml
---

# Undocs Configuration

Configure your documentation site using `.config/docs.yaml`. The configuration file uses JSON Schema for validation.

## Basic Configuration

```yaml
# .config/docs.yaml
name: "MyPackage"
shortDescription: "Short description"
description: "Full description of the package"
github: "username/repo"
url: "https://mypackage.example.com"
themeColor: "blue"
```

## Configuration Options

### Site Information

- `name` (string): Name of the documentation site
- `shortDescription` (string): Short description for meta tags
- `description` (string): Full description of the site
- `github` (string): GitHub repository (format: `owner/repo`)
- `url` (string): Public URL of the site (required for production builds)
- `themeColor` (string): Theme color (default: `"amber"`). Used for `theme-color` meta tag and color palette generation
- `lang` (string): Language code (default: `"en"`)

### Landing Page

```yaml
landing:
  heroLinks:
    stackblitz:
      icon: "i-heroicons-play"
      to: "https://stackblitz.com/..."
  heroCode: "npx giget gh:unjs/undocs/template docs"
  contributors: true
  features:
    - title: "Feature 1"
      icon: "⚡"
      description: "Feature description"
```

- `heroLinks`: Links displayed in the hero section
- `heroCode`: Code snippet shown in hero (string or object with `content` and `lang`)
- `contributors`: Show contributors on landing page
- `features`: Array of feature cards

### Social Media

```yaml
socials:
  x: "https://x.com/username"
  bluesky: "https://bsky.app/profile/username"
  discord: "https://discord.gg/..."
```

### Sponsors

```yaml
sponsors:
  api: "https://sponsors.example.com/sponsors.json"
```

### Redirects

```yaml
redirects:
  "/old-path": "/new-path"
```

### Versions

```yaml
versions:
  - label: "v2"
    url: "https://v2.example.com"
  - label: "v1"
    url: "https://v1.example.com"
```

### Banner

```yaml
banner:
  id: "unique-banner-id"
  title: "Banner Title"
  icon: "i-lucide-info"
  color: "primary"
  to: "/important-page"
  close: true
```

### LLMs Integration

Generate `/llms.txt` and `/llms-full.txt` for LLM consumption:

```yaml
llms:
  domain: "https://example.com"
  title: "Package Name"
  description: "Package description"
  full:
    title: "Package Name"
    description: "Full description"
```

### Automd Integration

Enable automd integration for automatic documentation updates:

```yaml
automd: true
```

### Build Cache

Enable experimental build cache:

```yaml
buildCache: true
```

## Schema Validation

Add schema reference at the top of your config file:

```yaml
# yaml-language-server: $schema=https://unpkg.com/undocs/schema/config.json
```

This provides autocomplete and validation in editors that support YAML Language Server.

## Key Points

- Configuration file is located at `.config/docs.yaml`
- JSON Schema is available at `https://unpkg.com/undocs/schema/config.json`
- `url` is required for production builds
- `branch` is auto-detected from git or environment variables
- Theme color generates a full color palette automatically

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/schema/config.schema.ts
- https://undocs.unjs.io/config
-->
