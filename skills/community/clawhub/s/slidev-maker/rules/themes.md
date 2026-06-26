# Slidev Themes

Using, configuring, and customizing themes.

## Using a Theme

Set theme in headmatter:
```yaml
---
theme: seriph
---
```

The theme package `@slidev/theme-seriph` is installed automatically on first run.

## Official Themes
```yaml
theme: default    # Minimal default theme
theme: seriph     # Professional, serif-based
theme: apple-basic # Apple keynote style
theme: bricks     # Colorful geometric
theme: shibainu   # Cute shiba inu theme
```

Browse all themes at [sli.dev/resources/theme-gallery](https://sli.dev/resources/theme-gallery).

## Community Themes

Use npm package name:
```yaml
---
theme: slidev-theme-geist
---
```

Or GitHub repo shorthand:
```yaml
---
theme: user/repo
---
```

## Theme Configuration

Themes may accept configuration options. Check theme documentation for available options.

Common pattern in headmatter:
```yaml
---
theme: seriph
themeConfig:
  primary: '#5d8aa8'
  secondary: '#e91e63'
---
```

## Local Theme

Use a local folder as theme:
```yaml
---
theme: ./my-theme
---
```

Structure:
```
your-slidev/
├── my-theme/
│   ├── package.json
│   ├── styles/
│   │   └── index.ts
│   ├── layouts/
│   │   └── cover.vue
│   └── components/
│       └── MyComponent.vue
├── slides.md
└── package.json
```

## Ejecting a Theme

Copy theme files locally for full customization:
```bash
slidev theme eject
```

This copies the current theme to your project. You can then modify any file.

After ejecting, update headmatter:
```yaml
---
theme: ./theme
---
```

## Overriding Theme Styles

Without ejecting, override styles in `styles/index.css`:
```css
/* styles/index.css */

:root {
  --slidev-theme-primary: #3b82f6;
}

.slidev-layout {
  background: linear-gradient(to bottom, #1a1a2e, #16213e);
}
```

## Overriding Theme Layouts

Create a layout with the same name in your `layouts/` folder:
```
your-slidev/
├── layouts/
│   └── cover.vue    # Overrides theme's cover layout
└── slides.md
```

Your local layout takes precedence over the theme's.

## Overriding Theme Components

Same approach - create in `components/` folder:
```
your-slidev/
├── components/
│   └── Logo.vue     # Overrides theme's Logo component
└── slides.md
```

## Multiple Themes

Slidev only supports one theme at a time. For additional functionality, use addons:
```yaml
---
theme: seriph
addons:
  - slidev-addon-citations
  - slidev-addon-qrcode
---
```

Addons provide components and features without replacing the theme.