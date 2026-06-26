---
name: undocs-project-structure
description: Understand the recommended project structure for undocs documentation sites
---

# Project Structure

Undocs follows a convention-based structure for organizing documentation.

## Standard Structure

```
docs/
├── .config/
│   └── docs.yaml          # Main configuration file
├── .docs/
│   └── public/            # Static assets (icons, images)
│       └── icon.svg
├── 1.guide/               # Documentation sections (numbered for order)
│   ├── 1.index.md        # Section index page
│   └── components/
│       ├── .navigation.yml # Navigation configuration
│       └── components.md
├── 2.config/
│   └── 1.index.md
├── blog/                  # Blog posts (optional)
│   ├── 0.index.md
│   └── 1.first-post.md
└── package.json
```

## Directory Conventions

### Numbered Sections

Use numbered prefixes to control navigation order:

- `1.guide/` - First section
- `2.config/` - Second section
- `3.api/` - Third section

### Index Files

Index files use numbered prefixes:

- `1.index.md` - First page in section
- `2.getting-started.md` - Second page

### Hidden Directories

Directories starting with `.` are ignored:

- `.config/` - Configuration files
- `.docs/` - Internal documentation files
- `.partials/` - Reusable markdown partials

## Configuration Files

### `.config/docs.yaml`

Main configuration file:

```yaml
name: "MyPackage"
github: "username/repo"
url: "https://example.com"
```

### `.navigation.yml`

Navigation configuration for a section:

```yaml
icon: i-lucide-book-open
```

## Static Assets

Place static assets in `.docs/public/`:

```
.docs/
└── public/
    ├── icon.svg
    └── images/
        └── logo.png
```

Assets are served from the root (`/icon.svg`, `/images/logo.png`).

## Content Organization

### Flat Structure

Keep content relatively flat (2-3 levels deep):

```
✅ Good:
1.guide/
  ├── 1.index.md
  └── components/
      └── components.md

❌ Avoid:
1.guide/
  └── deep/
      └── nested/
          └── structure/
              └── page.md
```

### Naming Conventions

- Use kebab-case for file names
- Use descriptive names
- Number prefixes for ordering

## Key Points

- Numbered prefixes control navigation order
- Index files use `1.index.md` convention
- Hidden directories (`.`) are for configuration
- Static assets go in `.docs/public/`
- Keep structure relatively flat (2-3 levels)
- Use kebab-case for file names

<!--
Source references:
- https://github.com/unjs/undocs/tree/main/template
- https://github.com/unjs/undocs/tree/main/docs
-->
