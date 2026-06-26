# Built-in Themes

## Table of Contents
- [Available Themes](#available-themes)
- [Applying Themes via npm](#applying-themes-via-npm)
- [Applying Themes via CDN](#applying-themes-via-cdn)
- [Individual Component Themes](#individual-component-themes)
- [Optimized (Lite) CSS Files](#optimized-lite-css-files)

## Available Themes

Syncfusion React components provide multiple modern themes with light and dark variants:

| Theme | Light CSS | Dark CSS | Design System |
|-------|-----------|----------|---------------|
| **Tailwind 3.4** | tailwind3.css | tailwind3-dark.css | Utility-first CSS framework v3.4 |
| **Bootstrap 5.3** | bootstrap5.3.css | bootstrap5.3-dark.css | Bootstrap framework v5.3 |
| **Fluent 2** | fluent2.css | fluent2-dark.css | Microsoft Fluent Design v2 |
| **Material 3** | material3.css | material3-dark.css | Google Material Design v3 |
| **Bootstrap 5** | bootstrap5.css | bootstrap5-dark.css | Bootstrap framework v5.0 |
| **Bootstrap 4** | bootstrap4.css | - | Bootstrap framework v4.0 |
| **Bootstrap 3** | bootstrap.css | bootstrap-dark.css | Bootstrap framework v3.0 |
| **Material** | material.css | material-dark.css | Google Material Design v1 |
| **Tailwind CSS** | tailwind.css | tailwind-dark.css | Earlier Tailwind version |
| **Fluent** | fluent.css | fluent-dark.css | Microsoft Fluent Design v1 |
| **Microsoft Office Fabric** | fabric.css | fabric-dark.css | Office UI Fabric |
| **High Contrast** | highcontrast.css | - | High contrast for accessibility |

Each theme provides:
- Light and dark variants
- CSS variable support for customization
- Responsive design patterns
- Accessibility compliance (WCAG 2.1)
- Consistent visual language across all components

## Applying Themes via npm

Themes are shipped as both combined and individual CSS/SCSS files.

### All Components (Combined)

**Step 1: Install the ej2 package**

```bash
npm install @syncfusion/ej2
```

**Step 2: Import theme CSS**

```css
/* src/App.css */
@import "./node_modules/@syncfusion/ej2/tailwind3.css";
```

Or import SCSS for variable access:

```css
/* src/App.scss */
@import "./node_modules/@syncfusion/ej2/tailwind3.scss";
```

**Available combined themes:**
- `@syncfusion/ej2/tailwind3.css`
- `@syncfusion/ej2/tailwind3-dark.css`
- `@syncfusion/ej2/bootstrap5.3.css`
- `@syncfusion/ej2/bootstrap5.3-dark.css`
- `@syncfusion/ej2/fluent2.css`
- `@syncfusion/ej2/fluent2-dark.css`
- `@syncfusion/ej2/material3.css`
- `@syncfusion/ej2/material3-dark.css`

## Applying Themes via CDN

> **⚠️ Important:** The CDN version MUST match your installed npm package version to avoid style and rendering issues. Using npm imports is recommended as it automatically keeps CSS and JavaScript versions in sync.

### Find Your Installed Version

Before using CDN links, check your installed package version:

```bash
npm list @syncfusion/ej2-react-grids
```

Or check package.json:

```json
{
  "dependencies": {
    "@syncfusion/ej2-react-grids": "33.1.44"  // Your version
  }
}
```

### Usage

```html
<!-- index.html -->
<head>
  <!-- Replace {VERSION} with your installed package version -->
  <link href="https://cdn.syncfusion.com/ej2/{VERSION}/{theme_name}.css" rel="stylesheet"/>
</head>
```

### Available CDN Links

Replace `{VERSION}` with your installed version (e.g., 27.2.2, 28.1.33, 33.1.44):

| Theme | CDN Link Pattern |
|-------|------------------|
| Tailwind 3.4 | https://cdn.syncfusion.com/ej2/{VERSION}/tailwind3.css |
| Tailwind 3.4 Dark | https://cdn.syncfusion.com/ej2/{VERSION}/tailwind3-dark.css |
| Bootstrap 5.3 | https://cdn.syncfusion.com/ej2/{VERSION}/bootstrap5.3.css |
| Bootstrap 5.3 Dark | https://cdn.syncfusion.com/ej2/{VERSION}/bootstrap5.3-dark.css |
| Fluent 2 | https://cdn.syncfusion.com/ej2/{VERSION}/fluent2.css |
| Fluent 2 Dark | https://cdn.syncfusion.com/ej2/{VERSION}/fluent2-dark.css |
| Material 3 | https://cdn.syncfusion.com/ej2/{VERSION}/material3.css |
| Material 3 Dark | https://cdn.syncfusion.com/ej2/{VERSION}/material3-dark.css |

**Example:** If your package version is `33.1.44`:

```html
<link href="https://cdn.syncfusion.com/ej2/33.1.44/tailwind3.css" rel="stylesheet"/>
```

## Individual Component Themes

For smallest bundle size, import only the component themes you need.

### From Individual Packages (Recommended)

```css
/* Import base styles first (required) */
@import "ej2-base/styles/tailwind3.css";

/* Import specific component styles */
@import "ej2-react-buttons/styles/tailwind3.css";
@import "ej2-react-grids/styles/tailwind3.css";
```

### From @syncfusion/ej2 Package

```css
/* Import base styles first (required) */
@import "ej2/base/tailwind3.css";

/* Import specific component styles */
@import "ej2/button/tailwind3.css";
@import "ej2/grid/tailwind3.css";
```

### Dependency Order

Some components require styles from dependent components. Example for Grid:

```css
@import "ej2-base/styles/tailwind3.css";           /* Required base */
@import "ej2-buttons/styles/tailwind3.css";        /* Grid uses buttons */
@import "ej2-inputs/styles/tailwind3.css";         /* Grid uses inputs */
@import "ej2-calendars/styles/tailwind3.css";      /* Grid date filtering */
@import "ej2-dropdowns/styles/tailwind3.css";      /* Grid filtering */
@import "ej2-navigations/styles/tailwind3.css";    /* Grid pager */
@import "ej2-popups/styles/tailwind3.css";         /* Grid dialogs */
@import "ej2-react-grids/styles/tailwind3.css";    /* Grid itself */
```

Refer to each component's documentation for its specific dependencies.

## Optimized (Lite) CSS Files

Syncfusion provides **optimized (lite)** theme variants that exclude "bigger" size mode styles, reducing file size by approximately 25%.

### File Size Comparison

| Theme | Default Size | Lite Size | Reduction |
|-------|-------------|-----------|-----------|
| Fluent 2 | 3.97 MB | 2.96 MB | ~25% |
| Tailwind 3.4 | 3.85 MB | 2.88 MB | ~25% |
| Material 3 | 3.92 MB | 2.94 MB | ~25% |

### Using Lite Versions

**All components (combined):**

```css
/* src/App.css */
@import "@syncfusion/ej2/tailwind3-lite.css";
```

Or SCSS:

```css
/* src/App.scss */
@import "@syncfusion/ej2/tailwind3-lite.scss";
```

**Individual components:**

```css
@import "@syncfusion/ej2-buttons/styles/tailwind3-lite.css";
```

**CDN:**

```html
<!-- Replace {VERSION} with your installed package version -->
<link href="https://cdn.syncfusion.com/ej2/{VERSION}/tailwind3-lite.css" rel="stylesheet"/>

<!-- Example: If your version is 33.1.44 -->
<link href="https://cdn.syncfusion.com/ej2/33.1.44/tailwind3-lite.css" rel="stylesheet"/>
```

> **Note:** Check your installed version with `npm list @syncfusion/ej2-react-buttons` before using CDN links.
