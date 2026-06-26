# DESIGN.md - Supabase Style

> 翡翠绿深色主题，开发者友好的开源后端

---

## 1. Visual Theme & Atmosphere

**Design Philosophy**: Developer-friendly, open-source, dark-first  
**Mood**: Technical, modern, friendly, powerful  
**Density**: Information-rich but organized  
**Design Language**: Code-centric, emerald accents, documentation-style  
**Target Audience**: Developers, startups, technical teams  
**Brand Personality**: Open, powerful, developer-centric, modern

### Design Principles

1. **Developer-first** - Built by developers, for developers
2. **Open-source spirit** - Transparent, community-driven
3. **Dark mode default** - Easy on the eyes during long coding sessions

### Visual Metaphors

- **Emerald green**: Growth, success, open-source
- **Dark background**: Developer-friendly, reduces eye strain
- **Code aesthetic**: Terminal-like, technical

---

## 2. Color Palette & Roles

### Primary Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| `supabase-emerald` | #10B981 | rgb(16, 185, 129) | Primary brand, CTAs, success |
| `supabase-dark` | #0F0F0F | rgb(15, 15, 15) | Background |
| `supabase-light` | #FFFFFF | rgb(255, 255, 255) | Text on dark |
| `supabase-emerald-light` | #34D399 | rgb(52, 211, 153) | Accent, hover states |

### Secondary Colors

| Name | Hex | Role |
|------|-----|------|
| `gray-400` | #6B7280 | Secondary text |
| `gray-600` | #4B5563 | Borders |
| `gray-800` | #1F2937 | Cards, surfaces |
| `gray-900` | #111827 | Deep surfaces |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| `success` | #10B981 | Success states, deployed |
| `warning` | #F59E0B | Warnings |
| `error` | #EF4444 | Errors |
| `info` | #3B82F6 | Informational |

### Accessibility

- **Contrast ratio**: 4.5:1 (AA) for emerald on dark
- **Color blind safe**: Yes
- **Focus indicators**: Emerald outline

---

## 3. Typography Rules

### Font Families

```css
--font-heading: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-code: 'JetBrains Mono', 'Fira Code', monospace;
```

### Type Scale

| Element | Font | Size | Weight | Line Height |
|---------|------|------|--------|-------------|
| `h1` | Inter | 48px | 700 | 1.2 |
| `h2` | Inter | 32px | 600 | 1.3 |
| `h3` | Inter | 24px | 600 | 1.4 |
| `body` | Inter | 16px | 400 | 1.6 |
| `code` | JetBrains Mono | 14px | 400 | 1.6 |

---

## 4. Component Stylings

### Buttons

```css
.btn-primary {
  background: #10B981;
  color: #FFFFFF;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-primary:hover {
  background: #34D399;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-secondary {
  background: transparent;
  color: #10B981;
  border: 1px solid #10B981;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-secondary:hover {
  background: rgba(16, 185, 129, 0.1);
}
```

### Inputs

```css
.input {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 10px 14px;
  font-size: 14px;
  color: #FFFFFF;
  width: 100%;
  transition: all 0.15s ease;
}

.input:focus {
  outline: none;
  border-color: #10B981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}
```

### Cards

```css
.card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 20px;
  transition: all 0.15s ease;
}

.card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
```

---

## 5. Layout Principles

### Spacing Scale

| Name | Value | Usage |
|------|-------|-------|
| `xs` | 4px | Tight spacing |
| `sm` | 8px | Small gaps |
| `md` | 16px | Default spacing |
| `lg` | 24px | Section spacing |
| `xl` | 32px | Large spacing |

### Grid System

- **Columns**: 12
- **Gutter**: 16px
- **Max width**: 1200px

---

## 6. Depth & Elevation

### Shadow System

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
--shadow-emerald: 0 4px 12px rgba(16, 185, 129, 0.3);
```

---

## 7. Do's and Don'ts

### ✅ Do

- Use emerald green for primary actions
- Design for dark mode first
- Keep code-centric aesthetic
- Use terminal-like elements
- Maintain developer-friendly UX

### ❌ Don't

- Use bright colors excessively
- Ignore dark mode optimization
- Over-decorate interfaces
- Forget code highlighting
- Sacrifice usability for style

---

## 8. Responsive Behavior

### Breakpoints

| Name | Min Width | Max Width |
|------|-----------|-----------|
| `mobile` | 0px | 639px |
| `tablet` | 640px | 1023px |
| `desktop` | 1024px | ∞ |

---

## 9. Agent Prompt Guide

### Quick Reference

```css
--color-primary: #10B981;
--color-background: #0F0F0F;
--color-text: #FFFFFF;
--font-body: 'Inter';
--border-radius: 6px;
```

### Common Prompts

**创建页面**:
```
创建一个 [页面名称] 页面，使用 Supabase 设计风格：
- 深色背景 #0F0F0F
- 翡翠绿主色 #10B981
- Inter 字体，JetBrains Mono 代码字体
- 开发者友好风格
```

---

**Supabase Design System v2.0.0**  
**Last Updated**: 2026-04-09
