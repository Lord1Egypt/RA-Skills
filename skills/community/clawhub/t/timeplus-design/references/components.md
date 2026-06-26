# Timeplus Console — Component Implementations

Full CSS and React reference for the Timeplus Console design system. Token values
are normative and match [`../DESIGN.md`](../DESIGN.md). Use these as ready-to-adapt
implementations rather than reinventing component styling.

## CSS custom properties

```css
:root {
  /* Gray scale */
  --color-gray-100: #120F1A;
  --color-gray-200: #231F2B;
  --color-gray-300: #3A3741;
  --color-gray-400: #514E58;
  --color-gray-500: #7D7B82;
  --color-gray-600: #B5B4B8;
  --color-gray-700: #DAD9DB;
  --color-gray-800: #ECECED;
  --color-gray-900: #F7F6F6;
  --color-white: #FFFFFF;

  /* Accent */
  --color-pink-400: #B83280;
  --color-pink-500: #D53F8C;

  /* Destructive */
  --color-red-400: #751025;
  --color-red-500: #D12D50;
}
```

## Tailwind configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        gray: {
          100: '#120F1A', 200: '#231F2B', 300: '#3A3741', 400: '#514E58',
          500: '#7D7B82', 600: '#B5B4B8', 700: '#DAD9DB', 800: '#ECECED',
          900: '#F7F6F6',
        },
        pink: { 400: '#B83280', 500: '#D53F8C' },
        red: { 400: '#751025', 500: '#D12D50' },
      },
      fontFamily: { sans: ['Inter', 'sans-serif'] },
    },
  },
}
```

## Base typography

```css
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: #120F1A;
}
h1 { font-size: 18px; font-weight: 600; color: #231F2B; }
h2 { font-size: 14px; font-weight: 600; color: #231F2B; }
h3 { font-size: 12px; font-weight: 600; color: #231F2B; }
p  { font-size: 14px; font-weight: 400; color: #120F1A; }
```

## Buttons

32px tall, 4px radius, Inter Semi-Bold 14px, 16px horizontal padding.

```css
.btn-primary {
  height: 32px; padding: 0 16px;
  background-color: #D53F8C; color: #FFFFFF;
  font: 600 14px 'Inter', sans-serif;
  border: none; border-radius: 4px; cursor: pointer;
}
.btn-primary:hover { background-color: #B83280; }
.btn-primary:disabled { background-color: #DAD9DB; color: #7D7B82; cursor: not-allowed; }

.btn-secondary {
  height: 32px; padding: 0 16px;
  background-color: #FFFFFF; color: #231F2B;
  font: 600 14px 'Inter', sans-serif;
  border: 1px solid #B5B4B8; border-radius: 4px; cursor: pointer;
}
.btn-secondary:hover { background-color: #F7F6F6; }
.btn-secondary:disabled { background-color: #DAD9DB; color: #514E58; cursor: not-allowed; }

.btn-primary-delete { /* like .btn-primary */ background-color: #D12D50; }
.btn-primary-delete:hover { background-color: #751025; }

.btn-secondary-delete { /* like .btn-secondary */ color: #D12D50; }
.btn-secondary-delete:hover { background-color: #F7F6F6; }

/* Icon: 16x16, 8px gap, color matches text */
.btn-with-icon { display: flex; align-items: center; gap: 8px; }
.btn-with-icon svg { width: 16px; height: 16px; }
```

```jsx
const Button = ({ variant = 'primary', destructive = false, disabled = false, icon, children, onClick }) => {
  const base = "h-8 px-4 font-semibold text-sm rounded flex items-center gap-2 transition-colors";
  const variants = {
    primary: destructive
      ? "bg-[#D12D50] text-white hover:bg-[#751025] disabled:bg-[#DAD9DB] disabled:text-[#7D7B82]"
      : "bg-[#D53F8C] text-white hover:bg-[#B83280] disabled:bg-[#DAD9DB] disabled:text-[#7D7B82]",
    secondary: destructive
      ? "bg-white text-[#D12D50] border border-[#B5B4B8] hover:bg-[#F7F6F6] disabled:bg-[#DAD9DB] disabled:text-[#514E58]"
      : "bg-white text-[#231F2B] border border-[#B5B4B8] hover:bg-[#F7F6F6] disabled:bg-[#DAD9DB] disabled:text-[#514E58]",
  };
  return (
    <button className={`${base} ${variants[variant]}`} disabled={disabled} onClick={onClick}>
      {icon && <span className="w-4 h-4">{icon}</span>}
      {children}
    </button>
  );
};
```

## Text inputs

40px tall, 4px radius, 12px horizontal padding; 12px gray-300 label with 8px gap.

```css
.input-field { display: flex; flex-direction: column; gap: 8px; }
.input-label { font: 400 12px 'Inter', sans-serif; color: #3A3741; }
.input-label.required::after { content: ' *'; color: #D12D50; }

.input {
  height: 40px; padding: 0 12px;
  background-color: #FFFFFF; border: 1px solid #B5B4B8; border-radius: 4px;
  font: 400 14px 'Inter', sans-serif; color: #120F1A;
}
.input::placeholder { color: #B5B4B8; }
.input:focus { outline: none; border-color: #3A3741; }
.input.error { border-color: #D12D50; }
.input-label.error { color: #D12D50; }
.input:disabled { background-color: #ECECED; color: #7D7B82; cursor: not-allowed; }
.input-label.disabled { color: #7D7B82; }
```

```jsx
const Input = ({ label, placeholder, value, onChange, error, disabled, required }) => (
  <div className="flex flex-col gap-2">
    {label && (
      <label className={`text-xs ${error ? 'text-[#D12D50]' : disabled ? 'text-[#7D7B82]' : 'text-[#3A3741]'}`}>
        {label}{required && <span className="text-[#D12D50]"> *</span>}
      </label>
    )}
    <input
      type="text" value={value} onChange={onChange} placeholder={placeholder} disabled={disabled}
      className={`h-10 px-3 rounded text-sm font-normal
        ${disabled ? 'bg-[#ECECED] text-[#7D7B82]' : 'bg-white text-[#120F1A]'}
        border ${error ? 'border-[#D12D50]' : 'border-[#B5B4B8]'}
        focus:outline-none focus:border-[#3A3741] placeholder:text-[#B5B4B8] disabled:cursor-not-allowed`}
    />
  </div>
);
```

## Toggle switch

36×20 pill track, 14px knob inset 3px.

```css
.toggle {
  position: relative; width: 36px; height: 20px;
  background-color: #B5B4B8; border-radius: 10px; cursor: pointer;
  transition: background-color 0.2s ease;
}
.toggle.on { background-color: #D53F8C; }
.toggle::after {
  content: ''; position: absolute; top: 3px; left: 3px;
  width: 14px; height: 14px; background-color: #FFFFFF; border-radius: 50%;
  transition: transform 0.2s ease;
}
.toggle.on::after { transform: translateX(16px); }
.toggle.disabled { background-color: #7D7B82; cursor: not-allowed; }
.toggle.disabled::after { background-color: #B5B4B8; }
.toggle.on.disabled { background-color: #B83280; }
```

```jsx
const Toggle = ({ checked, onChange, disabled }) => (
  <button
    role="switch" aria-checked={checked} disabled={disabled}
    onClick={() => !disabled && onChange(!checked)}
    className={`relative w-9 h-5 rounded-full transition-colors
      ${disabled ? (checked ? 'bg-[#B83280]' : 'bg-[#7D7B82]') : (checked ? 'bg-[#D53F8C]' : 'bg-[#B5B4B8]')}
      ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'}`}
  >
    <span className={`absolute top-[3px] w-[14px] h-[14px] rounded-full transition-transform
      ${disabled ? 'bg-[#B5B4B8]' : 'bg-white'} ${checked ? 'translate-x-[19px] left-0' : 'left-[3px]'}`} />
  </button>
);
```

## Containers / cards

```css
.container {
  background-color: #FFFFFF;
  border: 1px solid #DAD9DB;
  border-radius: 4px;
  padding: 24px;
}
```

## Tables

```css
.table { width: 100%; border-collapse: collapse; background-color: #FFFFFF; }
.table th {
  text-align: left; font-weight: 600; font-size: 12px; color: #231F2B;
  padding: 8px 12px; border-bottom: 1px solid #DAD9DB;
}
.table td {
  font-size: 14px; color: #120F1A; padding: 8px 12px;
  border-bottom: 1px solid #DAD9DB; min-height: 32px;
}
.table tr:hover td { background-color: #ECECED; }
```

## Links & dividers

```css
a { color: #B83280; text-decoration: none; }
a:hover { text-decoration: underline; }

.divider { height: 1px; background-color: #DAD9DB; border: none; }
```

## Icons

- Size in buttons: 16×16. Standalone: ~20×20.
- Static (non-button) icon color: `#3A3741` (gray-300).
- Clickable icon color: matches its associated text.
- Destructive icon color: `#D12D50` (red-500).

## Accessibility

All body text meets WCAG AA:

- Primary text `#120F1A` on `#FFFFFF` → 16.3:1 ✓
- Heading text `#231F2B` on `#FFFFFF` → 13.8:1 ✓
- Placeholder `#B5B4B8` on `#FFFFFF` → 2.2:1 (decorative only — never load-bearing)

Required practices:

```css
:focus-visible { outline: 2px solid #D53F8C; outline-offset: 2px; }
```

- Minimum interactive touch target: 32px height.
- Always associate `<label>` with inputs via `for`/`id`.

## Assets

- **Font:** Load Inter (weights 400 & 600) from Google Fonts.
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  ```
- **Icons:** A consistent library (Lucide, Heroicons) at 16–20px.
- **Export:** SVG for icons/illustrations; PNG/WebP for complex images.
