# Micro-Interactions & CSS Component Patterns
> Learned from uiverse.io/elements (3000+ community CSS components, MIT License)

## What is uiverse.io?
The largest open-source UI component library — 3000+ CSS/Tailwind components (Buttons, Cards, Inputs, Loaders, Toggles, Checkboxes, etc.) all MIT-licensed and copy-pasteable. Source: https://github.com/uiverse-io/galaxy

---

## Button Design Patterns

### 1. Icon + Label Pattern (Navigation Buttons)
Most effective nav buttons show colored icon + text label side by side.
```css
/* Pattern: icon in brand color, text inherits on hover */
.nav-btn { display: flex; align-items: center; gap: 8px; }
.nav-btn:hover { color: var(--accent-color); }
/* Icon stays its color, text changes to match */
```
Key insight: Each nav item gets its own accent color (dashboard=cyan, articles=blue, notes=yellow, reviews=orange). Color differentiation + icon = zero ambiguity.

### 2. Reveal-on-Hover (Progressive Disclosure Button)
Show label text only on hover — great for icon-only toolbars:
```css
.label { 
  transform: scaleX(0); 
  transform-origin: left;
  transition: transform 0.2s;
}
.btn:hover .label { transform: scaleX(1); }
```
Use for: compact toolbars where space is limited but discoverability matters.

### 3. Brutalist Button (High-Attention CTA)
Technique: hard offset shadow + glare sweep animation:
```css
.brutalist-btn {
  border: 3px solid #fff;
  outline: 3px solid #000;
  box-shadow: 6px 6px 0 var(--accent);
}
.brutalist-btn:hover {
  transform: translate(-4px, -4px);
  box-shadow: 10px 10px 0 #000;
}
.brutalist-btn:active {
  transform: translate(4px, 4px);
  box-shadow: none;
}
/* Glare sweep on hover */
.brutalist-btn::before {
  content: '';
  position: absolute;
  left: -100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
  animation: slide 2s infinite on-hover;
}
```
Use for: primary CTAs that need maximum attention. Neobrutalism trend.

### 4. Active/Press State (Required for all clickable elements)
Every button MUST have 3 states:
- **Default** — resting state
- **Hover** — `transform: translateY(-2px)` + glow
- **Active/Press** — `transform: translate(4px, 4px)` reverses the hover lift

Missing active state = feels broken and cheap.

---

## Card Design Patterns

### 5. Glitch Effect Card (Dark/Cyberpunk aesthetic)
For dark-mode, high-impact cards:
```css
/* CRT scan line overlay */
.card::before {
  content: '';
  background: repeating-linear-gradient(
    0deg,
    rgba(255,255,255,0.05),
    rgba(255,255,255,0.05) 1px,
    transparent 1px, transparent 2px
  );
  animation: tv-static 0.2s infinite alternate;
}
/* RGB channel split */
.card::after {
  background: linear-gradient(rgba(0,0,0,0) 50%, rgba(0,0,0,0.25) 50%),
    linear-gradient(90deg, rgba(255,0,0,0.06), rgba(0,255,0,0.02), rgba(0,0,255,0.06));
}
/* Glitch text */
.title::before { left: 2px; text-shadow: -1px 0 red; }
.title::after  { left: -2px; text-shadow: -1px 0 blue; }
```
Use for: gaming, cyberpunk, creative tech products. NOT for: B2B SaaS, medical, finance.

### 6. Card Hover Lift (Universal Pattern)
```css
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}
```
The translateY + shadow increase = sense of elevation, signals interactivity.

### 7. Spotlight/Scan Line Animation
Moving scan line across a card = attention directing:
```css
.scan-line {
  position: absolute;
  height: 6px;
  background: rgba(255,255,255,0.15);
  animation: scan 2.5s linear infinite;
}
@keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
```

---

## Input Design Patterns

### 8. Floating Label Input (Best UX Pattern)
Label starts inside the field as placeholder, floats up when focused:
```css
.input-wrap { position: relative; }
.label {
  position: absolute;
  top: 16px; left: 12px;
  transition: all 0.2s;
  pointer-events: none;
  color: #888;
}
.input:focus ~ .label,
.input:not(:placeholder-shown) ~ .label {
  top: 4px;
  font-size: 11px;
  color: var(--accent);
}
```
Why: Shows context even after user has typed. Better than disappearing placeholder.

### 9. Focus Ring (Neon Glow for Dark UI)
```css
.input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(var(--accent-rgb), 0.2),
              0 0 12px rgba(var(--accent-rgb), 0.1);
}
```
Replace standard browser outline with theme-consistent glow.

---

## Loading State Patterns

### 10. Skeleton Screen (Best Practice)
```css
.skeleton {
  background: linear-gradient(
    90deg,
    rgba(255,255,255,0.05) 25%,
    rgba(255,255,255,0.1) 50%,
    rgba(255,255,255,0.05) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```
Always prefer skeleton screens over spinners for content-heavy areas.

### 11. Loading Button State
```css
.btn.loading {
  pointer-events: none;
  opacity: 0.8;
}
.btn.loading::after {
  content: '';
  width: 16px; height: 16px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  margin-left: 8px;
}
```

---

## Toggle / Checkbox Patterns

### 12. Custom Toggle (Avoid Native Checkboxes for Primary Settings)
```css
.toggle {
  width: 44px; height: 24px;
  background: #333;
  border-radius: 12px;
  transition: background 0.2s;
}
.toggle.on { background: var(--accent); }
.toggle-thumb {
  width: 20px; height: 20px;
  border-radius: 50%;
  background: white;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
.toggle.on .toggle-thumb { transform: translateX(20px); }
```
Minimum size: 44×24px (touch target compliance).

---

## Animation Principles from uiverse.io

### 13. The 5 Micro-interaction Rules
1. **Keep it under 300ms** — interactions above 300ms feel sluggish
2. **Use ease-out for entrances** — `cubic-bezier(0.22, 1, 0.36, 1)` feels snappy
3. **Use ease-in for exits** — things leaving the screen accelerate away
4. **Avoid linear** — only for loading spinners; everywhere else feels robotic
5. **Respect `prefers-reduced-motion`** — always add:
```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; }
}
```

### 14. CSS Custom Properties for Theming
Design all components with CSS variables:
```css
:root {
  --accent: #b14fff;
  --accent-rgb: 177, 79, 255;
  --surface: rgba(255,255,255,0.04);
  --border: rgba(255,255,255,0.08);
  --radius: 12px;
  --radius-sm: 6px;
}
/* Outer = 2× inner */
.card { border-radius: calc(var(--radius) * 2); }
.card-inner { border-radius: var(--radius); }
```

### 15. Glow Effect (Neon/Cyberpunk)
```css
/* Text glow */
.neon-text { text-shadow: 0 0 10px var(--accent), 0 0 30px var(--accent); }

/* Border glow */
.neon-border { box-shadow: 0 0 0 1px var(--accent), 0 0 20px rgba(var(--accent-rgb), 0.3); }

/* Hover intensify */
.neon-btn:hover { box-shadow: 0 0 30px rgba(var(--accent-rgb), 0.6); }
```

---

## Component Categories on uiverse.io

| Category | Count | Best Use |
|----------|-------|----------|
| Buttons | 500+ | CTAs, nav, actions |
| Cards | 400+ | Content display, pricing |
| Inputs | 300+ | Forms, search |
| Checkboxes | 200+ | Settings, filters |
| Toggles | 150+ | On/off settings |
| Loaders | 200+ | Loading states |
| Notifications | 100+ | Alerts, toasts |
| Patterns | 100+ | Backgrounds, textures |
| Radio buttons | 100+ | Single-choice forms |

All MIT licensed → copy-paste freely, attribution appreciated.
Source: https://github.com/uiverse-io/galaxy

---

## Patterns to Avoid (Anti-patterns seen in poor implementations)

- ❌ **No hover state** — every interactive element needs hover feedback
- ❌ **No active/press state** — hover without press feels broken  
- ❌ **Infinite animation on static cards** — distracting; use hover-triggered animations
- ❌ **Animation without `prefers-reduced-motion`** — accessibility failure
- ❌ **Native checkbox/radio for important settings** — always custom style or use a library
- ❌ **Spinner for page-level loading** — use skeleton screens
- ❌ **CSS only for complex interactions** — some things need JavaScript for proper UX
