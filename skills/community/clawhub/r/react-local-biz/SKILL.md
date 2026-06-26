---
name: react-local-biz
description: Build complete, modern multi-page React websites for local businesses (landscapers, restaurants, salons, plumbers, gyms, etc.). Use when a user asks to build or design a website for a local/small business using React. Handles project scaffolding (Vite + React + Tailwind CSS v3 + Framer Motion + React Router v6 + Lucide React), full design system, all 5 standard pages, image strategy, responsive layout, animations, and production build — all generated directly without requiring a coding agent.
---

# React Local Business Website

Generates a complete, polished 5-page React site for any local business. No coding agent required — write all files directly.

## Stack

| Tool | Purpose |
|---|---|
| Vite + React | Project scaffold |
| Tailwind CSS v3 | Styling |
| React Router v6 | Page routing |
| Framer Motion | Scroll animations |
| Lucide React | Icons |

## Quick Workflow

1. **Identify business** — name, type, location, brand vibe
2. **Pick color palette** — see `references/business-types.md`
3. **Scaffold project** — run setup commands
4. **Write config files** — tailwind, CSS, index.html, App.jsx
5. **Write components** — Navbar, Footer, ScrollToTop
6. **Write 5 pages** — Home, Services, Portfolio/Gallery, About, Contact
7. **Build & verify** — `npm run build` must pass clean

## Setup Commands

```bash
mkdir -p <project-dir> && cd <project-dir> && git init
npm create vite@latest . -- --template react --force
npm install
npm install -D tailwindcss@3 postcss autoprefixer && npx tailwindcss init -p
npm install react-router-dom framer-motion lucide-react
```

## File Structure

```
src/
  App.jsx          # BrowserRouter + Routes + Navbar/Footer wrap
  main.jsx         # createRoot entry
  index.css        # @import fonts → @tailwind directives → @layer base/components
  components/
    Navbar.jsx     # Sticky, transparent-on-hero → white-on-scroll, mobile hamburger
    Footer.jsx     # 4-col dark footer: brand, links, services, contact
    ScrollToTop.jsx
  pages/
    Home.jsx       # Hero, stats bar, services preview, why-us, portfolio grid, testimonials, CTA
    Services.jsx   # Service cards grid + how-it-works steps
    Portfolio.jsx  # Filterable gallery + lightbox
    About.jsx      # Story, values, timeline, team, awards
    Contact.jsx    # Form with validation + contact info panel
```

## Design Principles

See `references/design-system.md` for the full design token system, reusable CSS component classes, and animation patterns.

## Pages Reference

See `references/page-templates.md` for section-by-section structure for each of the 5 pages.

## Business Types & Images

See `references/business-types.md` for per-industry color palettes and curated Unsplash image packs.

## Key Patterns

### App.jsx
```jsx
<BrowserRouter>
  <ScrollToTop />
  <div className="flex flex-col min-h-screen">
    <Navbar />
    <main className="flex-1"><Routes>...</Routes></main>
    <Footer />
  </div>
</BrowserRouter>
```

### Framer Motion — Scroll Animations
```jsx
// Standard fade-up on scroll
<motion.div
  initial={{ opacity: 0, y: 30 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
  transition={{ delay: index * 0.1 }}
>
```

### Staggered Children
```jsx
const stagger = { visible: { transition: { staggerChildren: 0.12 } } };
const fadeUp = { hidden: { opacity: 0, y: 30 }, visible: { opacity: 1, y: 0 } };
<motion.div initial="hidden" animate="visible" variants={stagger}>
  <motion.h1 variants={fadeUp}>...</motion.h1>
</motion.div>
```

### Navbar Transparency Logic
```jsx
const transparent = isHome && !scrolled && !mobileOpen;
// Apply: transparent ? "bg-transparent text-white" : "bg-white/95 backdrop-blur shadow"
```

### Contact Form Validation
```jsx
const validate = () => {
  const e = {};
  if (!form.name.trim()) e.name = "Required";
  if (!/\S+@\S+\.\S+/.test(form.email)) e.email = "Valid email required";
  if (!form.message.trim()) e.message = "Required";
  return e;
};
```

## Image Strategy

Use Unsplash with size + quality params: `?w=1920&q=80` (hero), `?w=800&q=80` (cards), `?w=600&q=80` (thumbnails). Always add `object-cover` class. See `references/business-types.md` for per-industry URL packs.

## Build Verification

```bash
npm run build   # Must exit 0 with no errors
```

CSS `@import` must come **before** `@tailwind` directives or PostCSS will warn.

## Dev Server

```bash
# Keep alive via OpenClaw background exec (not nohup):
# exec(command: "cd <dir> && npx vite --host 0.0.0.0 --port 5173", background: true)
# Access: http://localhost:5173
```
