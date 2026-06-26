# HTML Clone Template Guide

## File Structure

```
<site-name>-clone/
├── index.html
└── images/
    ├── hero.png
    └── ...
```

## HTML Skeleton

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[Site Name]</title>
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[FONT]&display=swap" rel="stylesheet">
  <style>
    /* CSS custom properties from extracted theme */
    :root {
      --background: hsl(...);
      --foreground: hsl(...);
      --primary: hsl(...);
      /* ... */
      --font-serif: '[SerifFont]', serif;
      --font-sans: '[SansFont]', sans-serif;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { background-color: var(--background); color: var(--foreground); font-family: var(--font-sans); }
    /* All component styles */
  </style>
</head>
<body>
  <!-- All sections -->
  <script>
    // Year, navbar scroll, carousel, IntersectionObserver animations, form toast
  </script>
</body>
</html>
```

## Standard JS Patterns

### Navbar scroll effect
```js
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
});
```

### Scroll animations
```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.fade-up, .fade-in').forEach(el => observer.observe(el));
```

### Image carousel
```js
let current = 0;
const slides = document.querySelectorAll('.slide');
setInterval(() => {
  slides[current].classList.remove('active');
  current = (current + 1) % slides.length;
  slides[current].classList.add('active');
}, 6000);
```

### Form toast
```js
document.getElementById('myForm').addEventListener('submit', e => {
  e.preventDefault();
  const toast = document.getElementById('toast');
  toast.classList.add('show');
  e.target.reset();
  setTimeout(() => toast.classList.remove('show'), 4000);
});
```

## CSS Patterns

### Fade animations
```css
.fade-up { opacity: 0; transform: translateY(30px); transition: opacity 0.8s ease, transform 0.8s ease; }
.fade-up.visible { opacity: 1; transform: translateY(0); }
.fade-in { opacity: 0; transition: opacity 1s ease; }
.fade-in.visible { opacity: 1; }
```

### Carousel slides
```css
.slide { position: absolute; inset: 0; opacity: 0; transition: opacity 1.5s ease; }
.slide.active { opacity: 1; }
```

### Fixed navbar with scroll blur
```css
nav { position: fixed; top: 0; left: 0; right: 0; z-index: 50; transition: all 0.5s; }
nav.scrolled { background: hsla(..., 0.92); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); }
```

## Quality Checklist

- [ ] All images load from `/images/` folder
- [ ] Fonts load from Google Fonts
- [ ] CSS custom properties match extracted theme
- [ ] Navbar becomes opaque on scroll
- [ ] Scroll animations trigger on viewport entry
- [ ] Contact form shows toast on submit (no page reload)
- [ ] Mobile responsive (uses `clamp()` for font sizes, `@media` for layouts)
- [ ] No external JS dependencies (no jQuery, no frameworks)
- [ ] Copyright year auto-updates via JS
