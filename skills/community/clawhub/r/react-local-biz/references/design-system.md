# Design System Reference

## Tailwind Config (tailwind.config.js)

Always extend with a custom color palette. Replace `primary` with the business's brand color family.

```js
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: { /* brand color scale — see business-types.md */ },
        accent:  { /* secondary accent — earthy, warm, or neutral */ },
        neutral: { /* stone/gray scale for text and backgrounds */ },
      },
      fontFamily: {
        display: ["Playfair Display", "Georgia", "serif"],   // headings
        body:    ["Inter", "system-ui", "sans-serif"],        // body text
      },
    },
  },
  plugins: [],
};
```

## Google Fonts

Always load via `<link>` in `index.html <head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
```

**Font pairings by vibe:**
| Vibe | Heading | Body |
|---|---|---|
| Elegant / Premium | Playfair Display | Inter |
| Modern / Tech | DM Sans | Inter |
| Friendly / Approachable | Nunito | Open Sans |
| Bold / Industrial | Oswald | Roboto |
| Rustic / Natural | Merriweather | Lato |

## index.css Structure

```css
/* 1. @import MUST come first */
@import url('https://fonts.googleapis.com/css2?...');

/* 2. Tailwind directives */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* 3. Base layer */
@layer base {
  html { scroll-behavior: smooth; }
  body { @apply font-body bg-white text-neutral-800 antialiased; }
  h1, h2, h3, h4 { @apply font-display; }
}

/* 4. Reusable component classes */
@layer components {
  .btn-primary   { @apply inline-flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white font-semibold px-7 py-3.5 rounded-full transition-all duration-300 hover:shadow-xl hover:-translate-y-0.5; }
  .btn-secondary { @apply inline-flex items-center gap-2 bg-white hover:bg-neutral-50 text-primary-700 font-semibold px-7 py-3.5 rounded-full transition-all duration-300 border border-neutral-200 hover:shadow-lg; }
  .btn-outline   { @apply inline-flex items-center gap-2 border-2 border-white text-white hover:bg-white hover:text-primary-700 font-semibold px-7 py-3.5 rounded-full transition-all duration-300; }
  .btn-outline-brand { @apply inline-flex items-center gap-2 border-2 border-primary-600 text-primary-600 hover:bg-primary-600 hover:text-white font-semibold px-7 py-3.5 rounded-full transition-all duration-300; }
  .section-label { @apply text-primary-600 font-semibold text-sm uppercase tracking-[0.2em] block mb-3; }
  .section-title { @apply font-display text-4xl md:text-5xl font-bold text-neutral-900 leading-tight; }
  .section-title-white { @apply font-display text-4xl md:text-5xl font-bold text-white leading-tight; }
  .card          { @apply bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden; }
  .input-field   { @apply w-full px-4 py-3 border border-neutral-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all bg-white placeholder-neutral-400; }
}
```

## Section Layouts

### Standard Section
```jsx
<section className="py-24 bg-white">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div className="text-center mb-16">
      <span className="section-label">Category Label</span>
      <h2 className="section-title">Main Heading</h2>
      <p className="text-neutral-500 text-lg max-w-2xl mx-auto mt-4">Supporting text...</p>
    </div>
    {/* Content */}
  </div>
</section>
```

### Alternating Light/Dark Sections
- `bg-white` → `bg-neutral-50` → `bg-white` → dark hero/CTA
- Never two identical bg-colors back-to-back (visual rhythm)

### Hero Section (Full Viewport)
```jsx
<section className="relative min-h-screen flex items-center justify-center overflow-hidden">
  <img src={heroImg} alt="..." className="absolute inset-0 w-full h-full object-cover" />
  <div className="absolute inset-0 bg-gradient-to-b from-black/60 via-black/50 to-black/70" />
  <div className="relative z-10 text-center px-4 max-w-5xl mx-auto">
    {/* Badge + H1 + Subtext + CTAs */}
  </div>
  {/* Scroll indicator */}
  <div className="absolute bottom-10 left-1/2 -translate-x-1/2 text-white/60 flex flex-col items-center gap-2 animate-bounce">
    <span className="text-xs uppercase tracking-widest">Scroll</span>
    <ChevronDown className="w-5 h-5" />
  </div>
</section>
```

### Page Sub-Hero (Interior Pages)
```jsx
<section className="relative py-40 overflow-hidden">
  <img src={img} className="absolute inset-0 w-full h-full object-cover" />
  <div className="absolute inset-0 bg-gradient-to-b from-black/65 to-black/50" />
  <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
    <div className="flex items-center justify-center gap-2 mb-5 text-primary-300">
      <span className="h-px w-12 bg-primary-400" />
      <span className="text-sm font-semibold uppercase tracking-widest">Page Name</span>
      <span className="h-px w-12 bg-primary-400" />
    </div>
    <h1 className="font-display text-5xl md:text-7xl font-bold text-white mb-5">Page Title</h1>
    <p className="text-white/75 text-xl max-w-2xl mx-auto">Subtext</p>
  </div>
</section>
```

## Card Patterns

### Service / Feature Card
```jsx
<div className="card group">
  <div className="relative h-48 overflow-hidden">
    <img className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
    <div className="absolute bottom-4 left-4 w-12 h-12 bg-primary-600 rounded-xl flex items-center justify-center shadow-lg">
      <Icon className="w-6 h-6 text-white" />
    </div>
  </div>
  <div className="p-6">
    <h3 className="font-display text-xl font-bold mb-2">...</h3>
    <p className="text-neutral-500 text-sm leading-relaxed mb-5">...</p>
    <Link className="text-primary-600 font-semibold text-sm flex items-center gap-1.5 group/link">
      Learn More <ArrowRight className="w-4 h-4 group-hover/link:translate-x-1 transition-transform" />
    </Link>
  </div>
</div>
```

### Testimonial Card
```jsx
<div className="bg-white/10 backdrop-blur-sm border border-white/10 rounded-2xl p-7">
  <Quote className="w-8 h-8 text-primary-400 mb-4 opacity-60" />
  <div className="flex gap-1 mb-4">{/* Star icons */}</div>
  <p className="text-white/85 text-sm leading-relaxed mb-6 italic">"{quote}"</p>
  <div className="flex items-center gap-3">
    <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
      {name[0]}
    </div>
    <div>
      <div className="text-white font-semibold text-sm">{name}</div>
      <div className="text-primary-300 text-xs">{location}</div>
    </div>
  </div>
</div>
```

### Stats Bar
```jsx
<section className="bg-primary-800 py-10">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
      {stats.map(({ value, label, icon: Icon }) => (
        <div className="text-center">
          <Icon className="w-7 h-7 text-primary-300 mx-auto mb-2" />
          <div className="font-display text-4xl font-bold text-primary-300 mb-1">{value}</div>
          <div className="text-white/70 text-sm font-medium">{label}</div>
        </div>
      ))}
    </div>
  </div>
</section>
```

## CTA Banner

```jsx
<section className="py-20 bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 relative overflow-hidden">
  <div className="relative max-w-4xl mx-auto px-4 text-center">
    <h2 className="font-display text-4xl md:text-5xl font-bold text-white mb-4">Call to Action</h2>
    <p className="text-white/80 text-xl mb-10 max-w-xl mx-auto">Supporting copy.</p>
    <div className="flex flex-wrap gap-4 justify-center">
      <Link to="/contact" className="bg-white text-primary-700 hover:bg-neutral-50 font-bold px-8 py-4 rounded-full flex items-center gap-2">
        Primary Action <ArrowRight className="w-5 h-5" />
      </Link>
      <a href="tel:+1..." className="btn-outline">Call Us</a>
    </div>
  </div>
</section>
```

## Navbar Component Logic

```jsx
// Transparent on home hero, white on scroll/other pages
const isHome = location.pathname === "/";
const transparent = isHome && !scrolled && !mobileOpen;

// Scroll listener
useEffect(() => {
  const onScroll = () => setScrolled(window.scrollY > 20);
  window.addEventListener("scroll", onScroll);
  return () => window.removeEventListener("scroll", onScroll);
}, []);

// Close mobile menu on route change
useEffect(() => setMobileOpen(false), [location]);
```

## Animation Tokens

```jsx
// Fade up (most common)
initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}

// Fade in from left
initial={{ opacity: 0, x: -30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}

// Fade in from right
initial={{ opacity: 0, x: 30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}

// Scale in (for modals/lightboxes)
initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}

// Stagger delay on lists
transition={{ delay: index * 0.08 }}

// Hero entrance (animate not whileInView)
initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
```

## Floating Badge Pattern (Trust Signals)

```jsx
<div className="absolute -bottom-6 -right-6 bg-white rounded-2xl shadow-xl p-5 border border-neutral-100">
  <div className="flex items-center gap-3">
    <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
      <Award className="w-6 h-6 text-primary-600" />
    </div>
    <div>
      <div className="font-display font-bold text-neutral-900 text-lg">15 Years</div>
      <div className="text-primary-600 text-xs font-semibold">of Excellence</div>
    </div>
  </div>
</div>
```

## Responsive Grids

```
Cards:       grid-cols-1 md:grid-cols-2 lg:grid-cols-3
Team/Awards: grid-cols-1 sm:grid-cols-2 lg:grid-cols-4
Gallery:     grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4
Contact:     grid-cols-1 lg:grid-cols-5 (form: col-span-3, info: col-span-2)
```

## Custom Scrollbar

```css
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #f5f5f4; }
::-webkit-scrollbar-thumb { background: <primary-600>; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: <primary-700>; }
```
