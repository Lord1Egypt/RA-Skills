# reveal.js API Reference

## CDN URLs (v5)
```
CSS:  https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css
Theme: https://cdn.jsdelivr.net/npm/reveal.js@5/dist/theme/{name}.css
JS:   https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.js
```

## Available Themes
black (default), white, league, beige, night, serif, simple, solarized, moon, dracula, sky, blood

## Configuration Options (key ones)

| Option | Default | Description |
|--------|---------|-------------|
| controls | true | Show navigation arrows |
| progress | true | Show progress bar |
| center | true | Vertical centering |
| hash | false | Add slide index to URL hash |
| transition | 'slide' | none/fade/slide/convex/concave/zoom |
| transitionSpeed | 'default' | default/fast/slow |
| backgroundTransition | 'fade' | Transition for backgrounds |
| width | 960 | Presentation width (px) |
| height | 700 | Presentation height (px) |
| margin | 0.04 | Factor around content |
| minScale | 0.2 | Min scale to apply |
| maxScale | 2.0 | Max scale to apply |
| autoSlide | 0 | Auto-progress in ms (0=off) |
| loop | false | Loop the presentation |
| mouseWheel | false | Navigate via mouse wheel |
| fragments | true | Enable fragments |
| fragmentInURL | true | Include fragment in URL |
| slideNumber | false | Show slide number (true, "c/t", "h.v") |
| embedded | false | For embedding in a page |
| autoAnimate | true | Enable auto-animate |
| autoAnimateDuration | 1.0 | Auto-animate duration (seconds) |
| navigationMode | 'default' | default/linear/grid |

## Fragments

Add `class="fragment"` to step through elements on a slide.

### Fragment Styles
| Class | Effect |
|-------|--------|
| (default) | Fade in |
| fade-out | Start visible, fade out |
| fade-up | Slide up while fading in |
| fade-down | Slide down while fading in |
| fade-left | Slide left while fading in |
| fade-right | Slide right while fading in |
| fade-in-then-out | Fade in, then out on next step |
| fade-in-then-semi-out | Fade in, then 50% on next step |
| grow | Scale up |
| shrink | Scale down |
| strike | Strike through |
| highlight-red/green/blue | Highlight text |
| highlight-current-red/green/blue | Highlight then revert |

### Fragment Order
Use `data-fragment-index` to control order:
```html
<p class="fragment" data-fragment-index="2">Appears second</p>
<p class="fragment" data-fragment-index="1">Appears first</p>
```

## Auto-Animate

Add `data-auto-animate` to adjacent `<section>` elements. Elements with matching content or `data-id` are automatically animated.

```html
<section data-auto-animate>
  <h1>Title</h1>
</section>
<section data-auto-animate>
  <h1 style="color: red;">Title</h1>
  <p>New content fades in</p>
</section>
```

Settings: `data-auto-animate-easing`, `data-auto-animate-duration`, `data-auto-animate-delay`

## Vertical Slides (Stacks)

Nest `<section>` elements for vertical navigation:
```html
<section>
  <section>Slide 1.1 (horizontal)</section>
  <section>Slide 1.2 (vertical, below)</section>
</section>
<section>
  <section>Slide 2.1</section>
</section>
```

## Backgrounds

```html
<section data-background-color="#ff0000">Solid color</section>
<section data-background-gradient="linear-gradient(to right, #f00, #00f)">Gradient</section>
<section data-background-image="url.jpg" data-background-size="cover">Image</section>
<section data-background-video="video.mp4" data-background-video-loop>Video</section>
<section data-background-iframe="https://example.com">iFrame</section>
```

## Built-in Plugins (CDN)

| Plugin | CDN Path | Init Name |
|--------|----------|-----------|
| Highlight | reveal.js@5/plugin/highlight/highlight.js | RevealHighlight |
| Markdown | reveal.js@5/plugin/markdown/markdown.js | RevealMarkdown |
| Notes | reveal.js@5/plugin/notes/notes.js | RevealNotes |
| Math | reveal.js@5/plugin/math/math.js | RevealMath |
| Search | reveal.js@5/plugin/search/search.js | RevealSearch |
| Zoom | reveal.js@5/plugin/zoom/zoom.js | RevealZoom |

```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/highlight/highlight.js"></script>
<script>
  Reveal.initialize({ plugins: [RevealHighlight] });
</script>
```

## Speaker Notes

```html
<section>
  <h2>Slide</h2>
  <aside class="notes">Speaker notes here (press S to open)</aside>
</section>
```

## Code Highlighting (with plugin)

```html
<pre><code data-trim data-noescape data-line-numbers="1|3-5">
function hello() {
  console.log("Hello");
  return true;
}
</code></pre>
```

`data-line-numbers="1|3-5"` highlights line 1 first, then lines 3-5 as fragments.

## JavaScript API

```js
Reveal.slide(h, v, f);      // Navigate to slide
Reveal.next(); Reveal.prev(); // Relative navigation
Reveal.getTotalSlides();     // Total slide count
Reveal.getProgress();        // 0..1 progress
Reveal.isFirstSlide();       // Boolean
Reveal.isLastSlide();        // Boolean
Reveal.on('slidechanged', event => { ... });
Reveal.on('fragmentshown', event => { ... });
```

## PDF Export

Append `?print-pdf` to URL, then use browser Print → Save as PDF.
Add this CSS for print:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5/css/print/pdf.css" media="print">
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| → / Space | Next slide |
| ← | Previous slide |
| ↑ / ↓ | Vertical navigation |
| F | Fullscreen |
| S | Speaker notes |
| O | Overview mode |
| Esc | Exit overview/pause |
| B / . | Blackout |
