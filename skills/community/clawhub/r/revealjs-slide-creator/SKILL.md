---
name: revealjs-slide-creator
description: Creates beautiful HTML slides using Reveal.js via CDN. Outputs a single HTML file.
---

# Reveal.js Slide Creator

## Objective
Use this skill when the user asks you to create a presentation, slides, or a Reveal.js slidedeck. You will generate a self-contained HTML file using the Reveal.js CDN.

## Instructions
1. Gather the presentation content (title, sections, slides, speaker notes) from the user. Use the `notify_user` tool to request clarifications if the content isn't fully provided.
2. Read the standard Reveal.js template from `templates/template.html` located in this skill's folder.
3. Replace the placeholder content within the `<div class="slides">` container with the actual slide contents. 
   - Use `<section>` for individual horizontal slides.
   - Use nested `<section>` elements for vertical slides.
   - You can also use markdown inside `<section data-markdown>` if you prefer or if the content is largely text-based.
4. Save the final output as an HTML file in the user's desired location (or in the current folder if not specified).
5. Let the user know the file has been created and that they can open it directly in their browser.

## Guidelines
- **Content Constraint (CRITICAL)**: Strictly constrain the content of each `<section>` so that the text and elements do not exceed the screen size (the default Reveal.js display area). If the provided content for a single slide is too long, you MUST split it into multiple separate slides (e.g., use sequential `<section>` elements) rather than cramming it all into one slide.
- **Advanced Features**: You must make use of the advanced features natively supported by Reveal.js to create engaging slides:
  - **Markdown**: Use `<section data-markdown><textarea data-template>...markdown content...</textarea></section>`.
  - **Backgrounds**: Use `data-background-color="color"`, `data-background-image="url"`, or `data-background-video="url"` on the `<section>`.
  - **Media & External Content**: Use standard HTML `<img>`, `<video>`, `<audio>` or iframe for interactive media.
  - **Code**: Use `<pre><code data-trim data-noescape class="language-js">...</code></pre>` for syntax highlighting.
  - **Math**: MathJax3 is configured. Use `$e^{i\pi} + 1 = 0$` for inline math and `\[...\]` for block equations.
  - **Fragments**: Add `class="fragment"`, `class="fragment fade-up"`, `class="fragment highlight-red"`, etc., to step through elements incrementally.
  - **Links**: Standard `<a href="...">` anchor tags.
- **Layout Helper Classes**: Maximize visual appeal by using native layout helper features:
  - `class="r-stack"`: Wrap multiple images/elements inside an `<div class="r-stack">` to center them on top of each other (usually paired with `class="fragment"`).
  - `class="r-fit-text"`: Add to headings (e.g., `<h2 class="r-fit-text">`) to make them perfectly fill the slide width.
  - `class="r-stretch"`: Add to an image or video to make it automatically scale to fill the remaining vertical space on the slide.
  - `class="r-frame"`: Add to an image or container to give it a neat bordered frame.
- Always use the Reveal.js CSS and JS from the CDN provided in the template (e.g., `https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.0.4/`).
- Do not download Reveal.js or use npm for this skill unless explicitly asked; stick to the CDN for a standalone HTML file.
- The default plugins (Markdown, Highlight, Notes) are enabled in the template. Use them if applicable (e.g., `<aside class="notes">` for speaker notes).
- Ensure the resulting HTML is fully functional, properly properly indented, and enclosed in standard HTML5 boilerplate.
