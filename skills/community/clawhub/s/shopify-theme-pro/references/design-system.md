# Design System for Shopify Themes

Build and maintain a scalable CSS design system for Shopify themes. This document covers design tokens, component architecture, and customization patterns.

## Overview

A design system is a collection of reusable components, styles, and design tokens that ensure visual consistency and enable rapid development.

**Benefits:**
- Consistent brand expression across all pages
- Faster development (reuse components instead of rebuilding)
- Easier maintenance (update tokens, propagate changes)
- Merchant customization without code (theme settings)

## Design Tokens

Design tokens are named variables that store design decisions (colors, spacing, typography). Use CSS custom properties for runtime customization.

### Color Tokens

**Definition (`assets/variables.css`):**
```css
:root {
  /* Brand Colors */
  --color-primary: {{ settings.color_primary }};
  --color-secondary: {{ settings.color_secondary }};
  --color-accent: {{ settings.color_accent }};

  /* Neutral Scale */
  --color-text: {{ settings.color_text }};
  --color-text-muted: {{ settings.color_text_muted }};
  --color-background: {{ settings.color_background }};
  --color-border: {{ settings.color_border }};

  /* Semantic Colors */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Opacity Variants */
  --color-primary-alpha-10: rgba({{ settings.color_primary | color_extract: 'red' }}, {{ settings.color_primary | color_extract: 'green' }}, {{ settings.color_primary | color_extract: 'blue' }}, 0.1);
}
```

**Theme Settings (`config/settings_schema.json`):**
```json
{
  "name": "Colors",
  "settings": [
    {
      "type": "header",
      "content": "Brand Colors"
    },
    {
      "type": "color",
      "id": "color_primary",
      "label": "Primary",
      "default": "#000000"
    },
    {
      "type": "color",
      "id": "color_secondary",
      "label": "Secondary",
      "default": "#6b7280"
    },
    {
      "type": "color",
      "id": "color_accent",
      "label": "Accent",
      "default": "#3b82f6"
    }
  ]
}
```

### Typography Tokens

**Definition:**
```css
:root {
  /* Font Families */
  --font-heading: {{ settings.font_heading.family }}, {{ settings.font_heading.fallback_families }};
  --font-body: {{ settings.font_body.family }}, {{ settings.font_body.fallback_families }};

  /* Type Scale (1.250 - Major Third) */
  --text-xs: 0.64rem;   /* 10.24px */
  --text-sm: 0.8rem;    /* 12.8px */
  --text-base: 1rem;    /* 16px */
  --text-lg: 1.25rem;   /* 20px */
  --text-xl: 1.563rem;  /* 25px */
  --text-2xl: 1.953rem; /* 31.25px */
  --text-3xl: 2.441rem; /* 39.06px */
  --text-4xl: 3.052rem; /* 48.83px */

  /* Font Weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  /* Line Heights */
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
}
```

**Usage:**
```css
h1 {
  font-family: var(--font-heading);
  font-size: var(--text-4xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
}

p {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--line-height-normal);
}
```

### Spacing Tokens

**8px Grid System:**
```css
:root {
  --spacing-base: 8px;
  --spacing-0: 0;
  --spacing-1: 4px;    /* 0.5 × base */
  --spacing-2: 8px;    /* 1 × base */
  --spacing-3: 12px;   /* 1.5 × base */
  --spacing-4: 16px;   /* 2 × base */
  --spacing-6: 24px;   /* 3 × base */
  --spacing-8: 32px;   /* 4 × base */
  --spacing-12: 48px;  /* 6 × base */
  --spacing-16: 64px;  /* 8 × base */
  --spacing-24: 96px;  /* 12 × base */
  --spacing-32: 128px; /* 16 × base */
}
```

**Usage:**
```css
.container {
  padding: var(--spacing-4);
  gap: var(--spacing-6);
}

.section {
  margin-block: var(--spacing-16);
}
```

### Breakpoints

**Definition:**
```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}
```

**Media Query Mixin (Sass):**
```scss
@mixin respond-to($breakpoint) {
  @media (min-width: $breakpoint) {
    @content;
  }
}

// Usage
.grid {
  grid-template-columns: 1fr;

  @include respond-to(768px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @include respond-to(1024px) {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Component Library

### Buttons

**Base Button:**
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-3) var(--spacing-6);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: var(--font-weight-semibold);
  line-height: 1;
  text-decoration: none;
  border: 2px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn:active {
  transform: translateY(0);
}
```

**Button Variants:**
```css
.btn--primary {
  background-color: var(--color-primary);
  color: white;
}

.btn--secondary {
  background-color: transparent;
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.btn--outline {
  background-color: transparent;
  border-color: var(--color-border);
  color: var(--color-text);
}

.btn--small {
  padding: var(--spacing-2) var(--spacing-4);
  font-size: var(--text-sm);
}

.btn--large {
  padding: var(--spacing-4) var(--spacing-8);
  font-size: var(--text-lg);
}
```

**Usage:**
```liquid
<button class="btn btn--primary">Add to Cart</button>
<a href="/collections/all" class="btn btn--secondary btn--large">Shop Now</a>
```

### Cards

**Base Card:**
```css
.card {
  display: flex;
  flex-direction: column;
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.card__image {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}

.card__body {
  padding: var(--spacing-4);
}

.card__title {
  font-size: var(--text-xl);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--spacing-2);
}

.card__text {
  color: var(--color-text-muted);
  line-height: var(--line-height-relaxed);
}
```

**Usage:**
```liquid
<div class="card">
  <img class="card__image" src="{{ product.featured_image | image_url: width: 400 }}" alt="{{ product.title }}">
  <div class="card__body">
    <h3 class="card__title">{{ product.title }}</h3>
    <p class="card__text">{{ product.description | truncate: 100 }}</p>
  </div>
</div>
```

### Grid System

**Responsive Grid:**
```css
.grid {
  display: grid;
  gap: var(--spacing-6);
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.grid--2-col {
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
}

.grid--fixed-2 {
  grid-template-columns: repeat(2, 1fr);
}

@media (max-width: 768px) {
  .grid--fixed-2 {
    grid-template-columns: 1fr;
  }
}
```

**Usage:**
```liquid
<div class="grid">
  {% for product in collection.products %}
    {% render 'product-card', product: product %}
  {% endfor %}
</div>
```

### Forms

**Form Elements:**
```css
.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
  margin-bottom: var(--spacing-4);
}

.form-label {
  font-size: var(--text-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
}

.form-input {
  padding: var(--spacing-3);
  font-family: var(--font-body);
  font-size: var(--text-base);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  transition: border-color 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-alpha-10);
}

.form-error {
  color: var(--color-error);
  font-size: var(--text-sm);
}
```

**Usage:**
```liquid
<div class="form-group">
  <label class="form-label" for="email">Email</label>
  <input class="form-input" type="email" id="email" name="email" required>
  {% if form.errors.email %}
    <span class="form-error">{{ form.errors.email }}</span>
  {% endif %}
</div>
```

## Utility Classes

**Spacing:**
```css
.mt-0 { margin-top: 0; }
.mt-2 { margin-top: var(--spacing-2); }
.mt-4 { margin-top: var(--spacing-4); }
.mt-8 { margin-top: var(--spacing-8); }

.mb-0 { margin-bottom: 0; }
.mb-2 { margin-bottom: var(--spacing-2); }
.mb-4 { margin-bottom: var(--spacing-4); }
.mb-8 { margin-bottom: var(--spacing-8); }

.p-4 { padding: var(--spacing-4); }
.p-8 { padding: var(--spacing-8); }
```

**Text Alignment:**
```css
.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }
```

**Display:**
```css
.hidden { display: none; }
.block { display: block; }
.flex { display: flex; }
.grid { display: grid; }
```

## Merchant Customization

Enable merchants to customize the design system via theme settings:

**Color Customization:**
```json
{
  "name": "Colors",
  "settings": [
    {
      "type": "color",
      "id": "color_primary",
      "label": "Primary Brand Color"
    },
    {
      "type": "color",
      "id": "color_secondary",
      "label": "Secondary Brand Color"
    }
  ]
}
```

**Typography Customization:**
```json
{
  "name": "Typography",
  "settings": [
    {
      "type": "font_picker",
      "id": "font_heading",
      "label": "Heading Font",
      "default": "helvetica_n7"
    },
    {
      "type": "font_picker",
      "id": "font_body",
      "label": "Body Font",
      "default": "helvetica_n4"
    }
  ]
}
```

**Spacing Customization (Advanced):**
```json
{
  "type": "range",
  "id": "spacing_multiplier",
  "min": 0.5,
  "max": 2,
  "step": 0.25,
  "default": 1,
  "label": "Spacing Scale"
}
```

Apply in CSS:
```css
:root {
  --spacing-base: calc(8px * {{ settings.spacing_multiplier }});
}
```

## Documentation

Document the design system for developers and merchants:

**Component Documentation:**
- Component name and purpose
- Usage examples (code snippets)
- Available variants and modifiers
- Accessibility notes

**Example (in `references/design-system.md`):**
```markdown
### Button Component

**Purpose:** Call-to-action elements for user interaction.

**Variants:**
- `.btn--primary` — Primary brand action
- `.btn--secondary` — Secondary action
- `.btn--outline` — Low-emphasis action

**Sizes:**
- `.btn--small` — Compact button
- `.btn--large` — Prominent button

**Example:**
<button class="btn btn--primary">Add to Cart</button>
```

## Best Practices

✅ **DO:**
- Use CSS custom properties for runtime customization
- Keep token names semantic (`--color-primary`, not `--color-blue`)
- Build mobile-first (base styles for mobile, override for desktop)
- Document all components and tokens
- Test with different brand colors to ensure contrast meets WCAG AA

❌ **DON'T:**
- Hardcode colors or spacing values
- Use overly specific selectors (avoid `!important`)
- Build desktop-first (requires more media query overrides)
- Create components without merchant customization in mind

---

**Last Updated:** 2026-03-13
