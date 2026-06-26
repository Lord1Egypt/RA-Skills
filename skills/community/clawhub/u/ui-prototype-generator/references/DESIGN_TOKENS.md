# Design Tokens

## Color Tokens

### Primary Colors
```
--color-primary: #1890ff
--color-primary-hover: #40a9ff
--color-primary-active: #096dd9
--color-primary-light: #e6f7ff
```

### Success Colors
```
--color-success: #52c41a
--color-success-hover: #73d13d
--color-success-active: #389e0d
--color-success-light: #f6ffed
```

### Warning Colors
```
--color-warning: #faad14
--color-warning-hover: #ffc53d
--color-warning-active: #d48806
--color-warning-light: #fffbe6
```

### Error Colors
```
--color-error: #f5222d
--color-error-hover: #ff4d4f
--color-error-active: #cf1322
--color-error-light: #fff2f0
```

### Neutral Colors
```
--color-text-primary: #333333
--color-text-secondary: #666666
--color-text-tertiary: #999999
--color-text-disabled: #bfbfbf

--color-border: #d9d9d9
--color-border-light: #f0f0f0
--color-background: #f5f5f5
--color-background-light: #fafafa
--color-white: #ffffff
--color-black: #000000
```

## Typography Tokens

### Font Family
```
--font-family-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif
--font-family-monospace: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace
```

### Font Sizes
```
--font-size-xs: 12px
--font-size-sm: 14px
--font-size-md: 16px
--font-size-lg: 20px
--font-size-xl: 24px
--font-size-xxl: 32px
```

### Font Weights
```
--font-weight-regular: 400
--font-weight-medium: 500
--font-weight-semibold: 600
--font-weight-bold: 700
```

### Line Heights
```
--line-height-tight: 1.2
--line-height-normal: 1.5
--line-height-relaxed: 1.8
```

## Spacing Tokens

### Base Unit: 4px
```
--spacing-xs: 4px    /* 1 unit */
--spacing-sm: 8px    /* 2 units */
--spacing-md: 16px   /* 4 units */
--spacing-lg: 24px   /* 6 units */
--spacing-xl: 32px   /* 8 units */
--spacing-xxl: 48px  /* 12 units */
```

### Component Spacing
```
--spacing-component-xs: 4px
--spacing-component-sm: 8px
--spacing-component-md: 12px
--spacing-component-lg: 16px
--spacing-component-xl: 24px
```

## Border Tokens

### Border Radius
```
--border-radius-sm: 2px
--border-radius-md: 4px
--border-radius-lg: 8px
--border-radius-xl: 16px
--border-radius-full: 9999px
```

### Border Width
```
--border-width-thin: 1px
--border-width-medium: 2px
--border-width-thick: 4px
```

## Shadow Tokens

### Box Shadows
```
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05)
--shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1)
--shadow-lg: 0 4px 12px rgba(0, 0, 0, 0.15)
--shadow-xl: 0 8px 24px rgba(0, 0, 0, 0.2)
```

### Focus Shadows
```
--shadow-focus-primary: 0 0 0 2px rgba(24, 144, 255, 0.2)
--shadow-focus-error: 0 0 0 2px rgba(245, 34, 45, 0.2)
```

## Size Tokens

### Component Sizes
```
--size-xs: 24px
--size-sm: 32px
--size-md: 40px
--size-lg: 48px
--size-xl: 64px
```

### Layout Sizes
```
--layout-max-width: 1200px
--layout-sidebar-width: 240px
--layout-header-height: 64px
--layout-footer-height: 48px
```

## Z-Index Tokens
```
--z-index-dropdown: 1000
--z-index-sticky: 1020
--z-index-fixed: 1030
--z-index-modal-backdrop: 1040
--z-index-modal: 1050
--z-index-popover: 1060
--z-index-tooltip: 1070
```

## Animation Tokens

### Durations
```
--duration-instant: 0ms
--duration-fast: 100ms
--duration-normal: 200ms
--duration-slow: 300ms
--duration-slower: 500ms
```

### Easing Functions
```
--ease-linear: linear
--ease-in: cubic-bezier(0.4, 0, 1, 1)
--ease-out: cubic-bezier(0, 0, 0.2, 1)
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55)
```

## Breakpoint Tokens
```
--breakpoint-xs: 0px      /* Mobile */
--breakpoint-sm: 576px    /* Large mobile */
--breakpoint-md: 768px    /* Tablet */
--breakpoint-lg: 992px    /* Desktop */
--breakpoint-xl: 1200px   /* Large desktop */
--breakpoint-xxl: 1400px  /* Extra large */
```

## Opacity Tokens
```
--opacity-0: 0
--opacity-25: 0.25
--opacity-50: 0.5
--opacity-75: 0.75
--opacity-100: 1
```

## Usage Examples

### CSS Variables
```css
:root {
  /* Import all tokens */
  --color-primary: #1890ff;
  --spacing-md: 16px;
  --border-radius-md: 4px;
  --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.button {
  background-color: var(--color-primary);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}
```

### JavaScript/JSON
```json
{
  "color": {
    "primary": "#1890ff",
    "success": "#52c41a",
    "warning": "#faad14",
    "error": "#f5222d"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px"
  }
}
```

### Figma Variables
- Create color variables for all color tokens
- Create number variables for spacing, sizing
- Create string variables for font families
- Apply variables to component properties
