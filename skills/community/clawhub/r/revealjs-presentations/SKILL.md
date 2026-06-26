---
name: revealjs-presentations
description: Create, edit, and deploy reveal.js presentations as single HTML files with optional custom CSS. Use when asked to create a presentation, slide deck, pitch deck, or talk. Supports fragments (step-by-step reveal), auto-animate, vertical slides, code highlighting, speaker notes, custom themes, background images/gradients/videos, and Vercel/GitHub Pages deployment. Output is a single HTML file using reveal.js v5 via CDN (no npm/build required). NOT for PowerPoint/Google Slides/Keynote — this creates web-based presentations only.
---

# reveal.js Presentations

Create web-based presentations as single HTML files using reveal.js v5 via CDN.

## Quick Start

1. Copy `assets/template.html` to the project directory
2. Replace `{{TITLE}}`, `{{SUBTITLE}}`, `{{THEME}}` placeholders
3. Add slides as `<section>` elements inside `<div class="slides">`
4. Open in browser or deploy to Vercel/GitHub Pages

## Slide Structure

```html
<div class="reveal">
  <div class="slides">
    <section>Slide 1</section>
    <section>Slide 2</section>
    <!-- Vertical stack -->
    <section>
      <section>Slide 3.1</section>
      <section>Slide 3.2 (down)</section>
    </section>
  </div>
</div>
```

## Key Features

### Fragments (click-to-reveal)
```html
<p class="fragment fade-up">Appears on click</p>
<p class="fragment fade-up">Then this</p>
```
Styles: `fade-in` (default), `fade-up`, `fade-down`, `fade-left`, `fade-right`, `fade-out`, `fade-in-then-out`, `grow`, `shrink`, `strike`, `highlight-red/green/blue`

### Auto-Animate
Add `data-auto-animate` to adjacent sections — matching elements animate automatically:
```html
<section data-auto-animate>
  <h1>Title</h1>
</section>
<section data-auto-animate>
  <h1 style="color: red;">Title</h1>
  <p>New content</p>
</section>
```

### Backgrounds
```html
<section data-background-color="#1a1a2e">Solid</section>
<section data-background-gradient="linear-gradient(135deg, #0f0f13, #1a1a2e)">Gradient</section>
<section data-background-image="photo.jpg" data-background-size="cover">Image</section>
```

### Speaker Notes
```html
<section>
  <h2>Slide</h2>
  <aside class="notes">Press S to see these notes</aside>
</section>
```

## Viewport Sizing

Set `width` and `height` in `Reveal.initialize()`. reveal.js scales the content to fit the browser window. Use larger values (e.g. 1400×800) if content looks too large on screen — the framework scales down automatically.

```js
Reveal.initialize({
  width: 1400,
  height: 800,
  margin: 0.04,
});
```

## Custom Styling

Use a separate `style.css` file or inline `<style>` block. Override reveal.js defaults:

```css
.reveal { font-family: 'Inter', system-ui, sans-serif; }
.reveal h1, .reveal h2 { text-transform: none; }
```

For grid backgrounds (like danielgrobelny.de):
```css
.reveal .slides section::before {
  content: "";
  position: absolute;
  inset: 0;
  opacity: 0.03;
  background-image:
    linear-gradient(var(--text) 1px, transparent 1px),
    linear-gradient(90deg, var(--text) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
}
```

## Themes

Built-in: black, white, league, beige, night, serif, simple, solarized, moon, dracula, sky, blood

Change via CDN link: `reveal.js@5/dist/theme/{name}.css`

For fully custom themes, use `black` as base and override with custom CSS.

## Plugins (via CDN)

Enable code highlighting, speaker notes, math, search, zoom:

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/highlight.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/notes/notes.js"></script>
<script>
  Reveal.initialize({ plugins: [RevealHighlight, RevealNotes] });
</script>
```

For code blocks with line highlighting:
```html
<pre><code data-trim data-line-numbers="1|3-5">
function hello() {
  return "world";
}
</code></pre>
```

## Deployment

### Vercel (static)
Just push the HTML + CSS + assets. No build step needed — Vercel serves static files.

### GitHub Pages
Push to repo, enable Pages from Settings → deploy from `main` branch root or `/docs`.

## PDF Export
Append `?print-pdf` to URL, then browser Print → Save as PDF.

## Full API Reference
Read `references/revealjs-api.md` for complete config options, fragment types, JS API methods, keyboard shortcuts, and plugin details.
