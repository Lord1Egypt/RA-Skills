# DESIGN.md - Claude Style

> 温暖陶土色调，AI 助手的友好面孔

---

## 1. Visual Theme & Atmosphere

**Design Philosophy**: Warm, approachable, helpful AI assistant  
**Mood**: Friendly, professional, intelligent, trustworthy  
**Density**: Comfortable, breathing room for clarity  
**Design Language**: Warm neutrals, editorial clarity, conversational UI  
**Target Audience**: AI users, professionals, knowledge workers  
**Brand Personality**: Warm, intelligent, helpful, trustworthy

### Design Principles

1. **Warmth through design** - Friendly, not cold or robotic
2. **Clarity in communication** - Clear, easy to understand
3. **Helpful by default** - Every element serves the user

### Visual Metaphors

- **Terracotta accent**: Warmth, earthiness, approachability
- **Clear typography**: Editorial quality, trust
- **Rounded corners**: Friendliness, no sharp edges

---

## 2. Color Palette & Roles

### Primary Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| `claude-terracotta` | #D97706 | rgb(217, 119, 6) | Primary brand, CTAs |
| `claude-dark` | #1F2937 | rgb(31, 41, 55) | Primary text |
| `claude-light` | #FFFFFF | rgb(255, 255, 255) | Background |
| `claude-amber` | #F59E0B | rgb(245, 158, 11) | Accent, highlights |

### Secondary Colors

| Name | Hex | Role |
|------|-----|------|
| `gray-400` | #9CA3AF | Secondary text |
| `gray-200` | #E5E7EB | Borders |
| `amber-100` | #FEF3C7 | Warning background |
| `amber-50` | #FFFBEB | Light amber surface |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| `success` | #10B981 | Success states |
| `warning` | #F59E0B | Warnings |
| `error` | #EF4444 | Errors |
| `info` | #D97706 | Informational |

### Accessibility

- **Contrast ratio**: 4.5:1 (AA) for text
- **Color blind safe**: Yes
- **Focus indicators**: Terracotta outline

---

## 3. Typography Rules

### Font Families

```css
--font-heading: 'Source Serif Pro', Georgia, serif;
--font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-code: 'JetBrains Mono', 'Fira Code', monospace;
```

### Type Scale

| Element | Font | Size | Weight | Line Height |
|---------|------|------|--------|-------------|
| `h1` | Source Serif Pro | 40px | 700 | 1.2 |
| `h2` | Source Serif Pro | 32px | 700 | 1.3 |
| `h3` | Source Serif Pro | 24px | 600 | 1.4 |
| `body` | Inter | 16px | 400 | 1.6 |
| `code` | JetBrains Mono | 14px | 400 | 1.6 |

---

## 4. Component Stylings

### Buttons

```css
.btn-primary {
  background: #D97706;
  color: #FFFFFF;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-primary:hover {
  background: #F59E0B;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3);
}

.btn-secondary {
  background: transparent;
  color: #D97706;
  border: 2px solid #D97706;
  padding: 10px 22px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-secondary:hover {
  background: #FEF3C7;
}
```

### Inputs

```css
.input {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 16px;
  color: #1F2937;
  width: 100%;
  transition: all 0.15s ease;
}

.input:focus {
  outline: none;
  border-color: #D97706;
  box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.1);
}
```

### Cards

```css
.card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.15s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
- **Gutter**: 24px
- **Max width**: 1200px

---

## 6. Depth & Elevation

### Shadow System

```css
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
--shadow-md: 0 4px 12px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.15);
```

---

## 7. Do's and Don'ts

### ✅ Do

- Use warm, friendly colors
- Keep typography clear and readable
- Use serif fonts for headings
- Maintain approachable feel
- Implement smooth transitions

### ❌ Don't

- Use cold, sterile colors
- Overcrowd interfaces
- Use sharp, aggressive elements
- Ignore accessibility
- Sacrifice warmth for minimalism

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
--color-primary: #D97706;
--color-background: #FFFFFF;
--color-text: #1F2937;
--font-heading: 'Source Serif Pro';
--font-body: 'Inter';
--border-radius: 8px;
```

### Common Prompts

**创建页面**:
```
创建一个 [页面名称] 页面，使用 Claude 设计风格：
- 白色背景
- 陶土色主色 #D97706
- Source Serif Pro 标题，Inter 正文
- 圆角 8px
- 温暖友好的风格
```

---

**Claude Design System v2.0.0**  
**Last Updated**: 2026-04-09
