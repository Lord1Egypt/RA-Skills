# Design Token Reference

Complete CSS design token system from the UI Designer agent.

## Color Tokens

### Primary
```css
--color-primary-100: #f0f9ff;
--color-primary-200: #e0f2fe;
--color-primary-300: #bae6fd;
--color-primary-400: #7dd3fc;
--color-primary-500: #38bdf8;
--color-primary-600: #0284c7;
--color-primary-700: #0369a1;
--color-primary-800: #075985;
--color-primary-900: #0c4a6e;
```

### Secondary
```css
--color-secondary-100: #f3f4f6;
--color-secondary-200: #e5e7eb;
--color-secondary-300: #d1d5db;
--color-secondary-400: #9ca3af;
--color-secondary-500: #6b7280;
--color-secondary-600: #4b5563;
--color-secondary-700: #374151;
--color-secondary-800: #1f2937;
--color-secondary-900: #111827;
```

### Semantic
```css
--color-success: #10b981;
--color-success-light: #d1fae5;
--color-success-dark: #065f46;

--color-warning: #f59e0b;
--color-warning-light: #fef3c7;
--color-warning-dark: #92400e;

--color-error: #ef4444;
--color-error-light: #fee2e2;
--color-error-dark: #991b1b;

--color-info: #3b82f6;
--color-info-light: #dbeafe;
--color-info-dark: #1e40af;
```

## Typography Tokens

```css
--font-family-primary: 'Inter', system-ui, -apple-system, sans-serif;
--font-family-secondary: 'JetBrains Mono', 'Fira Code', monospace;

--font-size-xs:   0.75rem;    /* 12px */
--font-size-sm:   0.875rem;   /* 14px */
--font-size-base: 1rem;       /* 16px */
--font-size-lg:   1.125rem;   /* 18px */
--font-size-xl:   1.25rem;    /* 20px */
--font-size-2xl:  1.5rem;     /* 24px */
--font-size-3xl:  1.875rem;   /* 30px */
--font-size-4xl:  2.25rem;    /* 36px */
--font-size-5xl:  3rem;       /* 48px */

--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;

--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.75;
```

## Spacing Tokens

```css
--space-0:  0;
--space-1:  0.25rem;   /* 4px */
--space-2:  0.5rem;    /* 8px */
--space-3:  0.75rem;   /* 12px */
--space-4:  1rem;      /* 16px */
--space-5:  1.25rem;  /* 20px */
--space-6:  1.5rem;    /* 24px */
--space-8:  2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;      /* 48px */
--space-16: 4rem;      /* 64px */
--space-20: 5rem;      /* 80px */
--space-24: 6rem;      /* 96px */
```

## Border Radius

```css
--radius-none: 0;
--radius-sm: 0.25rem;   /* 4px */
--radius-md: 0.5rem;    /* 8px */
--radius-lg: 0.75rem;   /* 12px */
--radius-xl: 1rem;       /* 16px */
--radius-2xl: 1.5rem;    /* 24px */
--radius-full: 9999px;
```

## Shadow Tokens

```css
--shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
--shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
--shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
```

## Transition Tokens

```css
--transition-fast: 150ms ease;
--transition-normal: 300ms ease;
--transition-slow: 500ms ease;
--transition-bounce: 500ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

## Z-Index Scale

```css
--z-dropdown: 1000;
--z-sticky: 1020;
--z-fixed: 1030;
--z-modal-backdrop: 1040;
--z-modal: 1050;
--z-popover: 1060;
--z-tooltip: 1070;
```

## Dark Theme Override

```css
[data-theme="dark"] {
  --color-primary-100: #1e3a8a;
  --color-primary-500: #60a5fa;
  --color-primary-900: #dbeafe;

  --color-secondary-100: #111827;
  --color-secondary-500: #9ca3af;
  --color-secondary-900: #f9fafb;

  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.3), 0 1px 2px -1px rgb(0 0 0 / 0.3);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.3), 0 2px 4px -2px rgb(0 0 0 / 0.3);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.3), 0 4px 6px -4px rgb(0 0 0 / 0.3);
}
```
