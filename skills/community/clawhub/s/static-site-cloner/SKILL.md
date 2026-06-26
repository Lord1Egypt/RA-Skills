---
name: static-site-cloner
description: Static site reproduction expert - Analyze target websites and manually code their structure, visual style, and basic interactions using pure HTML/CSS/JavaScript.
---

# Static Site Cloner

Based on a target website URL, accurately reproduce the site's structure, visuals, and interactions using pure HTML, CSS, and JavaScript. Output only front-end code, without involving backend functionality.

## Use Cases

- User requests to "reproduce a website," "clone a website," "recreate a website," "copy a web page"
- User provides a website URL and requests code rewrite
- User needs to convert an existing website into pure front-end code
- User wants to learn or understand the front-end implementation of a particular website

## Workflow

### 1. Information Gathering

Use `web_fetch` to retrieve the HTML content of the target website:

```
web_fetch(url="target_url", extractMode="markdown")
```

Analyze and document:
- Page structure (navigation, header, main content, footer)
- Visual elements (colors, typography, spacing, shadows)
- Interactive behaviors (clicks, hovers, animations)

### 2. Structure Reproduction

Write semantic HTML:
- Use proper HTML5 tags (header, nav, main, section, article, footer)
- Maintain DOM hierarchy consistent with the original site
- Add clear comments explaining the function of each section

### 3. Style Restoration

Write CSS styles:
- Prefer Flexbox/Grid layout
- Implement responsive design (media queries)
- Pay attention to pseudo-classes and transition effects (:hover, :focus, transition)
- Use CSS variables to manage colors and spacing

### 4. Interaction Implementation

Use vanilla JavaScript:
- Event listeners (addEventListener)
- DOM manipulation (classList, style, innerHTML)
- Animation effects (requestAnimationFrame or CSS Animation)

### 5. Output Specification

Generate runnable code:

```
project_directory/
├── index.html
├── styles/
│   └── main.css
└── scripts/
    └── main.js
```

Or a single-file version (inline CSS/JS).

## Code Conventions

```
<!-- HTML: Semantic + Comments -->
<header class="site-header">
  <!-- Navigation bar -->
  <nav class="navbar">...</nav>
</header>

/* CSS: BEM Naming + CSS Variables */
:root {
  --primary-color: #3498db;
  --spacing-unit: 8px;
}

.navbar__link--active {
  color: var(--primary-color);
}

// JavaScript: Modern ES6+ Syntax
const toggleMenu = () => {
  document.body.classList.toggle('menu-open');
};
```

## Limitations

- **Pure front-end technologies only**: HTML, CSS, JavaScript (no React/Vue/jQuery)
- **No backend functionality**: No database, API, or server-side rendering
- **Image placeholders**: Use placeholder services (e.g., placeholder.com, picsum.photos)
- **Copyright compliance**: Do not copy original site text content, trademarks, or sensitive information

## References

For more detailed examples and patterns, refer to:
- [references/examples.md](references/examples.md) - Reproduction examples for common website types
- [references/patterns.md](references/patterns.md) - CSS layout and interaction pattern references