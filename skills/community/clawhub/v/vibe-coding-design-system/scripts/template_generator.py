#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESIGN.md 模板改进生成器
自动生成完整的9部分模板
"""

import json
from typing import Dict

class DesignTemplateGenerator:
    """完整模板生成器"""
    
    def generate_complete_template(self, design_data: Dict) -> str:
        """
        生成完整的9部分模板
        
        Args:
            design_data: 设计数据字典
            
        Returns:
            完整的 DESIGN.md 内容
        """
        
        template = f"""# DESIGN.md - {design_data['name']} Style

> {design_data['tagline']}

---

## 1. Visual Theme & Atmosphere

**Design Philosophy**: {design_data['philosophy']}  
**Mood**: {design_data['mood']}  
**Density**: {design_data.get('density', 'Balanced, purposeful whitespace')}  
**Design Language**: {design_data.get('language', 'Modern, clean, minimal')}  
**Target Audience**: {design_data.get('audience', 'General users, professionals')}  
**Brand Personality**: {design_data.get('personality', 'Professional, reliable, modern')}

### Design Principles

1. **{design_data.get('principle1', 'User-first')}** - Every design decision serves the user
2. **{design_data.get('principle2', 'Clarity')}** - Clear, intuitive, easy to understand
3. **{design_data.get('principle3', 'Consistency')}** - Consistent patterns throughout

### Visual Metaphors

- **{design_data.get('metaphor1', 'Primary color')}**: {design_data.get('metaphor1_desc', 'Brand identity, trust')}
- **{design_data.get('metaphor2', 'Clean layout')}**: {design_data.get('metaphor2_desc', 'Professionalism, clarity')}
- **{design_data.get('metaphor3', 'Rounded corners')}**: {design_data.get('metaphor3_desc', 'Friendliness, modern')}

---

## 2. Color Palette & Roles

### Primary Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| `{design_data['primary_name']}` | {design_data['primary_hex']} | {self._hex_to_rgb(design_data['primary_hex'])} | Primary brand, CTAs |
| `{design_data.get('secondary_name', 'secondary')}` | {design_data.get('secondary_hex', '#6B7280')} | {self._hex_to_rgb(design_data.get('secondary_hex', '#6B7280'))} | Secondary text |
| `{design_data.get('bg_name', 'background')}` | {design_data.get('bg_hex', '#FFFFFF')} | {self._hex_to_rgb(design_data.get('bg_hex', '#FFFFFF'))} | Background |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| `success` | #10B981 | Success states, confirmations |
| `warning` | #F59E0B | Warnings, cautions |
| `error` | #EF4444 | Errors, destructive actions |
| `info` | #3B82F6 | Informational, tips |

### Accessibility

- **Contrast ratio**: 4.5:1 (AA) minimum
- **Color blind safe**: Yes (tested with Coblis)
- **Focus indicators**: Visible outline on interactive elements

---

## 3. Typography Rules

### Font Families

```css
/* 中文 */
--font-cn: '{design_data.get('font_cn', 'PingFang SC')}', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;

/* 英文 */
--font-en: '{design_data.get('font_en', 'Inter')}', -apple-system, BlinkMacSystemFont, sans-serif;

/* 代码 */
--font-code: '{design_data.get('font_code', 'JetBrains Mono')}', 'Consolas', monospace;
```

### Type Scale

| Element | Font | Size | Weight | Line Height | Letter Spacing |
|---------|------|------|--------|-------------|----------------|
| `h1` | {design_data.get('font_heading', 'Inter')} | {design_data.get('h1_size', '48px')} | {design_data.get('h1_weight', '700')} | {design_data.get('h1_line', '1.2')} | {design_data.get('h1_spacing', '-0.02em')} |
| `h2` | {design_data.get('font_heading', 'Inter')} | {design_data.get('h2_size', '32px')} | {design_data.get('h2_weight', '600')} | {design_data.get('h2_line', '1.3')} | {design_data.get('h2_spacing', '-0.01em')} |
| `h3` | {design_data.get('font_heading', 'Inter')} | {design_data.get('h3_size', '24px')} | {design_data.get('h3_weight', '600')} | {design_data.get('h3_line', '1.4')} | 0 |
| `body-large` | {design_data.get('font_body', 'Inter')} | 16px | 400 | {design_data.get('body_line', '1.6')} | 0 |
| `body` | {design_data.get('font_body', 'Inter')} | 14px | 400 | {design_data.get('body_line', '1.6')} | 0 |
| `caption` | {design_data.get('font_body', 'Inter')} | 12px | 400 | 1.4 | 0 |

### Typography Usage

#### Headings
- **H1**: Page titles, hero sections
- **H2**: Section titles, feature headers
- **H3**: Card titles, subsections

#### Body Text
- **Large**: Feature descriptions, important content
- **Regular**: Paragraphs, lists, general content
- **Caption**: Timestamps, footnotes, labels

---

## 4. Component Stylings

### Buttons

#### Primary Button

```css
.btn-primary {{
  background: {design_data['primary_hex']};
  color: #FFFFFF;
  padding: 10px 20px;
  border-radius: {design_data.get('border_radius', '8')}px;
  font-weight: 500;
  font-size: 14px;
  font-family: var(--font-cn), var(--font-en);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}}

.btn-primary:hover {{
  background: {self._adjust_brightness(design_data['primary_hex'], 0.9)};
  transform: translateY(-1px);
  box-shadow: 0 4px 12px {design_data['primary_hex']}40;
}}

.btn-primary:active {{
  transform: translateY(0);
}}

.btn-primary:focus {{
  outline: none;
  box-shadow: 0 0 0 3px {design_data['primary_hex']}30;
}}

.btn-primary:disabled {{
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}}
```

#### Secondary Button

```css
.btn-secondary {{
  background: transparent;
  color: {design_data['primary_hex']};
  border: 1px solid {design_data['primary_hex']};
  padding: 9px 19px;
  border-radius: {design_data.get('border_radius', '8')}px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}}

.btn-secondary:hover {{
  background: {design_data['primary_hex']}10;
}}
```

### Inputs

```css
.input {{
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: {design_data.get('border_radius', '8')}px;
  padding: 10px 14px;
  font-size: 14px;
  font-family: var(--font-cn), var(--font-en);
  color: #1F2937;
  width: 100%;
  transition: all 0.2s ease;
}}

.input:focus {{
  outline: none;
  border-color: {design_data['primary_hex']};
  box-shadow: 0 0 0 3px {design_data['primary_hex']}20;
}}

.input::placeholder {{
  color: #9CA3AF;
}}
```

### Cards

```css
.card {{
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: {design_data.get('card_radius', '12')}px;
  padding: 16px;
  transition: all 0.2s ease;
}}

.card:hover {{
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}}
```

---

## 5. Layout Principles

### Spacing Scale

| Name | Value | Usage |
|------|-------|-------|
| `xs` | 4px | Tight spacing, icon gaps |
| `sm` | 8px | Small gaps, inline spacing |
| `md` | 16px | Default spacing, component padding |
| `lg` | 24px | Section padding, large gaps |
| `xl` | 32px | Major sections |
| `2xl` | 48px | Page sections |

### Grid System

- **Columns**: 12
- **Gutter**: 16px
- **Max width**: {design_data.get('max_width', '1200px')}
- **Container padding**: 24px

### Breakpoints

```css
--breakpoint-sm: 640px;   /* Mobile */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large desktop */
```

### Whitespace Philosophy

- **Generous**: Give content room to breathe
- **Consistent**: Use spacing scale always
- **Purposeful**: Every pixel serves a function
- **Hierarchical**: More whitespace = more importance

---

## 6. Depth & Elevation

### Shadow System

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15);
```

### Z-Index Scale

| Name | Value | Usage |
|------|-------|-------|
| `base` | 0 | Default layer |
| `dropdown` | 10 | Dropdown menus |
| `sticky` | 20 | Sticky headers |
| `modal` | 30 | Modal dialogs |
| `toast` | 40 | Toast notifications |

---

## 7. Do's and Don'ts

### ✅ Do

- Use {design_data['primary_hex']} as primary color
- Maintain consistent spacing
- Follow typography hierarchy
- Use {design_data.get('font_cn', 'PingFang SC')} for Chinese text
- Implement all interaction states
- Test accessibility
- Keep components reusable
- Use semantic color names

### ❌ Don't

- Use arbitrary spacing values
- Hardcode color hex values
- Ignore responsive breakpoints
- Skip hover/focus states
- Use low-contrast text
- Overuse shadows
- Add unnecessary decoration
- Sacrifice usability for aesthetics

### Common Mistakes

1. **Inconsistent spacing**: Always use the spacing scale
2. **Wrong font weights**: Follow typography guidelines
3. **Missing states**: Implement all interaction states
4. **Poor contrast**: Test accessibility
5. **Over-decoration**: Keep it clean and functional

---

## 8. Responsive Behavior

### Breakpoints

| Name | Min Width | Max Width | Target Devices |
|------|-----------|-----------|----------------|
| `mobile` | 0px | 639px | Mobile phones |
| `tablet` | 640px | 1023px | Tablets |
| `desktop` | 1024px | ∞ | Desktops |

### Touch Targets

- **Minimum size**: 44px × 44px
- **Spacing between**: 8px minimum

### Responsive Patterns

```css
/* Navigation */
@media (max-width: 767px) {{
  .nav {{ display: none; }}
  .mobile-nav {{ display: block; }}
}}

/* Grid */
@media (min-width: 768px) {{
  .grid {{ grid-template-columns: repeat(2, 1fr); }}
}}

@media (min-width: 1024px) {{
  .grid {{ grid-template-columns: repeat(3, 1fr); }}
}}
```

---

## 9. Agent Prompt Guide

### Quick Reference

```css
/* Colors */
--color-primary: {design_data['primary_hex']};
--color-background: {design_data.get('bg_hex', '#FFFFFF')};
--color-text: #1F2937;

/* Fonts */
--font-heading: '{design_data.get('font_heading', 'Inter')}';
--font-body: '{design_data.get('font_body', 'Inter')}';

/* Spacing */
--spacing-base: 8px;
--border-radius: {design_data.get('border_radius', '8')}px;
```

### Common Prompts

**创建页面**:
```
创建一个 [页面名称] 页面，使用 {design_data['name']} 设计风格：
- 主色 {design_data['primary_hex']}
- {design_data.get('font_cn', 'PingFang SC')} 中文字体
- {design_data.get('font_en', 'Inter')} 英文字体
- 圆角 {design_data.get('border_radius', '8')}px
```

**创建组件**:
```
创建一个 [组件名称] 组件：
- 使用 {design_data['primary_hex']} 主色
- 圆角 {design_data.get('border_radius', '8')}px
- 包含所有交互状态
```

### Code Templates

#### React Component

```tsx
import React from 'react';
import styles from './Button.module.css';

interface ButtonProps {{
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  onClick?: () => void;
}}

export function Button({{ 
  children, 
  variant = 'primary',
  disabled = false,
  onClick 
}}: ButtonProps) {{
  return (
    <button 
      className={{`${{styles.btn}} ${{styles[variant]}}}}
      disabled={{disabled}}
      onClick={{onClick}}
    >
      {{children}}
    </button>
  );
}}
```

### AI Agent Instructions

When generating UI code:

1. **Use primary color** {design_data['primary_hex']}
2. **Follow spacing scale** - no arbitrary values
3. **Implement all states** - hover, active, disabled, focus
4. **Test responsiveness** - check all breakpoints
5. **Ensure accessibility** - contrast ratios, touch targets
6. **Keep it clean** - no unnecessary decoration

### Component Checklist

- [ ] Uses {design_data['primary_hex']} primary color
- [ ] Follows typography scale
- [ ] Implements all states
- [ ] Responsive design
- [ ] Accessible (contrast, touch targets)
- [ ] Clean and functional

---

**{design_data['name']} Design System v2.0.0**  
**Last Updated**: 2026-04-09  
**License**: MIT
"""
        
        return template
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """将HEX颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"rgb({r}, {g}, {b})"
    
    def _adjust_brightness(self, hex_color: str, factor: float) -> str:
        """调整颜色亮度"""
        hex_color = hex_color.lstrip('#')
        r = int(int(hex_color[0:2], 16) * factor)
        g = int(int(hex_color[2:4], 16) * factor)
        b = int(int(hex_color[4:6], 16) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"


def main():
    """示例使用"""
    generator = DesignTemplateGenerator()
    
    # 示例设计数据
    sample_data = {
        'name': 'Example',
        'tagline': 'Example design system',
        'philosophy': 'Modern, clean, user-focused',
        'mood': 'Professional, friendly',
        'primary_hex': '#3B82F6',
        'primary_name': 'primary',
        'font_cn': 'PingFang SC',
        'font_en': 'Inter',
        'border_radius': '8'
    }
    
    template = generator.generate_complete_template(sample_data)
    print(template)


if __name__ == '__main__':
    main()
