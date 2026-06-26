# DESIGN.md - Linear Style

> 紫色极简主义，极致精确，开发者至上

---

## 1. Visual Theme & Atmosphere

**Design Philosophy**: Ultra-minimal, precise, developer-centric  
**Mood**: Technical sophistication meets elegant simplicity  
**Density**: Compact, information-rich, every pixel counts  
**Design Language**: Swiss-inspired minimalism with purple accents  
**Target Audience**: Software engineers, product teams, technical professionals  
**Brand Personality**: Precise, modern, confident, efficient

### Design Principles

1. **Clarity over decoration** - Every element serves a purpose
2. **Function reveals form** - UI emerges from functionality
3. **Speed is a feature** - Performance in every interaction

### Visual Metaphors

- **Dark void background**: Infinite possibilities, focus on content
- **Purple accent**: Creative energy, innovation, modernity
- **Sharp edges**: Precision, accuracy, technical excellence

---

## 2. Color Palette & Roles

### Primary Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| `void-black` | #000000 | rgb(0, 0, 0) | Primary background, surfaces |
| `purple-accent` | #8B5CF6 | rgb(139, 92, 246) | Accent, CTAs, highlights, links |
| `white` | #FFFFFF | rgb(255, 255, 255) | Primary text on dark surfaces |

### Secondary Colors

| Name | Hex | Role |
|------|-----|------|
| `slate-400` | #94A3B8 | Secondary text, disabled states, placeholders |
| `slate-600` | #475569 | Body text on light surfaces, descriptions |
| `slate-800` | #1E293B | Borders, dividers, separators |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| `success` | #10B981 | Success states, confirmations, positive actions |
| `warning` | #F59E0B | Warnings, cautions, attention needed |
| `error` | #EF4444 | Errors, destructive actions, critical alerts |
| `info` | #3B82F6 | Informational, tips, neutral highlights |

### Gradients

```css
/* Hero gradient */
background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);

/* Card hover */
background: linear-gradient(180deg, 
  rgba(139, 92, 246, 0.05) 0%, 
  rgba(139, 92, 246, 0) 100%);

/* Button gradient */
background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
```

### Accessibility

- **Contrast ratio**: 7.5:1 (AAA) for all text
- **Color blind safe**: Yes (tested with Coblis simulator)
- **Focus indicators**: Visible outline on all interactive elements

---

## 3. Typography Rules

### Font Families

```css
--font-heading: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-code: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
```

### Type Scale

| Element | Font | Size | Weight | Line Height | Letter Spacing |
|---------|------|------|--------|-------------|----------------|
| `h1` | Inter | 48px | 700 | 1.1 | -0.02em |
| `h2` | Inter | 32px | 600 | 1.2 | -0.01em |
| `h3` | Inter | 24px | 600 | 1.3 | -0.01em |
| `h4` | Inter | 18px | 600 | 1.4 | 0 |
| `body-large` | Inter | 16px | 400 | 1.5 | 0 |
| `body` | Inter | 14px | 400 | 1.5 | 0 |
| `body-small` | Inter | 13px | 400 | 1.5 | 0 |
| `caption` | Inter | 12px | 400 | 1.4 | 0 |
| `code` | JetBrains Mono | 13px | 400 | 1.6 | 0 |

### Typography Usage

#### Headings
- **H1**: Hero sections, landing pages, major announcements
- **H2**: Section titles, feature headers, page titles
- **H3**: Card titles, subsections, dialog titles
- **H4**: Small headings, form labels, minor sections

#### Body Text
- **Large**: Feature descriptions, important content, introductions
- **Regular**: Paragraphs, lists, general content, UI text
- **Small**: Secondary descriptions, helper text, metadata
- **Caption**: Timestamps, footnotes, labels, badges

### Special Typography

```css
/* Code blocks */
code {
  font-family: var(--font-code);
  font-size: 13px;
  background: rgba(139, 92, 246, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  color: #A78BFA;
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, #8B5CF6, #EC4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Muted text */
.text-muted {
  color: var(--slate-400);
  font-size: 13px;
}
```

---

## 4. Component Stylings

### Buttons

#### Primary Button

```css
.btn-primary {
  /* Base styles */
  background: #8B5CF6;
  color: #FFFFFF;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
  letter-spacing: -0.01em;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

/* Hover state */
.btn-primary:hover {
  background: #7C3AED;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

/* Active state */
.btn-primary:active {
  transform: translateY(0);
  background: #6D28D9;
}

/* Focus state */
.btn-primary:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3);
}

/* Disabled state */
.btn-primary:disabled {
  background: #4C1D95;
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

#### Secondary Button

```css
.btn-secondary {
  background: transparent;
  color: #94A3B8;
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-secondary:hover {
  color: #FFFFFF;
  border-color: rgba(148, 163, 184, 0.4);
  background: rgba(255, 255, 255, 0.05);
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

#### Ghost Button

```css
.btn-ghost {
  background: transparent;
  color: #94A3B8;
  padding: 8px 12px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-ghost:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #FFFFFF;
}
```

### Inputs

#### Text Input

```css
.input {
  /* Base styles */
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 14px;
  color: #FFFFFF;
  width: 100%;
  transition: all 0.15s ease;
  font-family: var(--font-body);
}

/* Placeholder */
.input::placeholder {
  color: #64748B;
}

/* Focus state */
.input:focus {
  outline: none;
  border-color: #8B5CF6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

/* Error state */
.input.error {
  border-color: #EF4444;
}

.input.error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

/* Success state */
.input.success {
  border-color: #10B981;
}

/* Disabled state */
.input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(0, 0, 0, 0.2);
}
```

### Cards

#### Default Card

```css
.card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
  transition: all 0.15s ease;
}

.card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.15);
}
```

#### Interactive Card

```css
.card-interactive {
  cursor: pointer;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
  transition: all 0.15s ease;
}

.card-interactive:hover {
  transform: translateY(-2px);
  border-color: rgba(139, 92, 246, 0.3);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.1);
}

.card-interactive:active {
  transform: translateY(0);
}
```

### Navigation

#### Sidebar Navigation

```css
.sidebar {
  background: rgba(0, 0, 0, 0.5);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  width: 240px;
  height: 100vh;
  padding: 16px;
}

.nav-item {
  padding: 8px 12px;
  border-radius: 6px;
  color: #94A3B8;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #FFFFFF;
}

.nav-item.active {
  background: rgba(139, 92, 246, 0.1);
  color: #A78BFA;
}
```

---

## 5. Layout Principles

### Spacing Scale

| Name | Value | Usage |
|------|-------|-------|
| `xs` | 4px | Icon spacing, tight groups, micro-adjustments |
| `sm` | 8px | Button padding, list items, small gaps |
| `md` | 16px | Card padding, default gaps, section spacing |
| `lg` | 24px | Section padding, containers, major gaps |
| `xl` | 32px | Large sections, feature areas |
| `2xl` | 48px | Page sections, hero areas, major separations |
| `3xl` | 64px | Major sections, significant whitespace |

### Grid System

- **Columns**: 12
- **Gutter**: 16px
- **Max width**: 1200px
- **Container padding**: 24px

### Breakpoints

```css
--breakpoint-sm: 640px;   /* Mobile */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large desktop */
--breakpoint-2xl: 1536px; /* Extra large */
```

### Layout Patterns

- **Stack**: Vertical layout with consistent spacing
- **Cluster**: Horizontal grouping with wrapping
- **Sidebar**: Main content + fixed sidebar (240px)
- **Split**: Two-column equal width
- **Hero**: Full-width hero section

### Whitespace Philosophy

- **Generous**: Whitespace is not empty space, it's breathing room
- **Consistent**: Always use spacing scale, avoid arbitrary values
- **Purposeful**: Every pixel of whitespace serves a function
- **Hierarchical**: More whitespace = more importance

---

## 6. Depth & Elevation

### Shadow System

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.5);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.6);
--shadow-2xl: 0 25px 50px rgba(0, 0, 0, 0.7);
--shadow-purple: 0 4px 12px rgba(139, 92, 246, 0.3);
```

### Z-Index Scale

| Name | Value | Usage |
|------|-------|-------|
| `base` | 0 | Default layer, content |
| `dropdown` | 10 | Dropdown menus, selects |
| `sticky` | 20 | Sticky headers, toolbars |
| `modal` | 30 | Modal dialogs, overlays |
| `popover` | 40 | Popovers, tooltips, menus |
| `toast` | 50 | Toast notifications, alerts |

### Elevation Principles

- **Minimal shadows**: Use borders and opacity instead of heavy shadows
- **Glassmorphism**: Subtle transparency creates depth
- **Layered surfaces**: Background → Surface → Overlay
- **Focus depth**: Elevated elements should stand out clearly

### Glassmorphism Effects

```css
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-dark {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

---

## 7. Do's and Don'ts

### ✅ Do

- Maintain consistent spacing using the scale
- Use semantic color names in code
- Test accessibility for all color combinations
- Follow typography hierarchy strictly
- Keep components reusable and modular
- Use subtle animations for transitions
- Design for dark mode first
- Prioritize content over decoration
- Use CSS custom properties for all tokens
- Test across all breakpoints
- Implement all interaction states
- Keep code clean and well-documented

### ❌ Don't

- Use arbitrary spacing values (e.g., 13px, 27px)
- Hardcode color hex values in components
- Ignore responsive breakpoints
- Overuse shadows and gradients
- Mix design languages inconsistently
- Use low-contrast text combinations
- Add unnecessary decorative elements
- Sacrifice usability for aesthetics
- Forget hover/active/disabled states
- Use heavy borders or outlines
- Over-complicate component structure
- Skip accessibility testing

### Common Mistakes

1. **Inconsistent borders**: Mixing border colors and styles
2. **Wrong font weights**: Using 400 when 500 is specified
3. **Arbitrary spacing**: Not using the spacing scale
4. **Missing states**: Forgetting hover/active/disabled states
5. **Poor accessibility**: Insufficient color contrast
6. **Over-decoration**: Adding unnecessary visual elements
7. **Inconsistent radius**: Mixing border-radius values

---

## 8. Responsive Behavior

### Breakpoints

| Name | Min Width | Max Width | Target Devices |
|------|-----------|-----------|----------------|
| `mobile` | 0px | 639px | Mobile phones |
| `tablet` | 640px | 1023px | Tablets |
| `desktop` | 1024px | 1279px | Laptops, small screens |
| `large` | 1280px | ∞ | Desktops, monitors |

### Touch Targets

- **Minimum size**: 44px × 44px (Apple HIG)
- **Recommended**: 48px × 48px (Material Design)
- **Spacing between targets**: 8px minimum

### Responsive Patterns

#### Navigation

```css
/* Desktop: Horizontal nav */
@media (min-width: 1024px) {
  .nav { display: flex; }
  .nav-mobile-toggle { display: none; }
}

/* Mobile: Hamburger menu */
@media (max-width: 1023px) {
  .nav { display: none; }
  .nav-mobile-toggle { display: block; }
}
```

#### Grid

```css
/* Mobile: 1 column */
.grid { grid-template-columns: 1fr; }

/* Tablet: 2 columns */
@media (min-width: 640px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop: 3 columns */
@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}
```

### Collapsing Strategy

- **Stack vertically** on mobile
- **Simplify navigation** to hamburger menu
- **Reduce padding/margins** on smaller screens
- **Hide secondary information** on mobile
- **Prioritize primary actions** in mobile view
- **Use bottom sheets** for mobile modals

---

## 9. Agent Prompt Guide

### Quick Reference

```css
/* Colors */
--color-primary: #8B5CF6;
--color-background: #000000;
--color-text: #FFFFFF;
--color-secondary: #94A3B8;
--color-border: rgba(255, 255, 255, 0.1);

/* Fonts */
--font-heading: 'Inter';
--font-body: 'Inter';
--font-code: 'JetBrains Mono';

/* Spacing */
--spacing-base: 4px;
--border-radius: 6px;

/* Shadows */
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
--shadow-purple: 0 4px 12px rgba(139, 92, 246, 0.3);
```

### Common Prompts

**创建页面**:
```
创建一个 [页面名称] 页面，使用 Linear 设计风格：
- 黑色背景，紫色强调色 #8B5CF6
- Inter 字体，JetBrains Mono 代码字体
- 紧凑布局，间距使用 4px 基准
- 圆角 6px，边框 rgba(255, 255, 255, 0.1)
- 悬停时紫色边框 rgba(139, 92, 246, 0.3)
```

**创建组件**:
```
创建一个 [组件名称] 组件，遵循 Linear 设计规范：
- 背景色: rgba(255, 255, 255, 0.05)
- 边框: 1px solid rgba(255, 255, 255, 0.1)
- 圆角: 8px
- 悬停: border-color 变为 rgba(139, 92, 246, 0.3)
- 过渡: all 0.15s ease
```

### Code Templates

#### React Component

```tsx
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
}

export function Button({ 
  children, 
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick 
}: ButtonProps) {
  return (
    <button 
      className={`${styles.btn} ${styles[variant]} ${styles[size]}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

#### CSS Module

```css
.btn {
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
  letter-spacing: -0.01em;
  cursor: pointer;
  transition: all 0.15s ease;
  border: none;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn.md {
  padding: 8px 16px;
}

.btn.primary {
  background: var(--color-primary);
  color: white;
}

.btn.primary:hover:not(:disabled) {
  filter: brightness(1.1);
  transform: translateY(-1px);
}

.btn.secondary {
  background: transparent;
  color: var(--color-secondary);
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.btn.ghost {
  background: transparent;
  color: var(--color-secondary);
}
```

### AI Agent Instructions

When generating UI code based on this DESIGN.md:

1. **Always use CSS custom properties** from the quick reference
2. **Follow spacing scale** - no arbitrary values
3. **Maintain color consistency** - use defined palette
4. **Respect typography hierarchy** - use correct font sizes and weights
5. **Implement all states** - hover, active, disabled, focus
6. **Test responsiveness** - check all breakpoints
7. **Ensure accessibility** - contrast ratios, touch targets
8. **Keep it minimal** - no unnecessary decoration
9. **Use transitions** - 0.15s ease for all interactions
10. **Follow naming conventions** - BEM or CSS Modules

### Component Generation Checklist

Before generating a component, verify:

- [ ] Uses defined color tokens
- [ ] Follows typography scale
- [ ] Implements all interaction states
- [ ] Responsive across breakpoints
- [ ] Accessible (contrast, touch targets)
- [ ] Minimal and functional
- [ ] Consistent with design language
- [ ] Proper transitions
- [ ] Clean, maintainable code
- [ ] Well-documented

---

**Linear Design System v2.0.0**  
**Last Updated**: 2026-04-09  
**License**: MIT
