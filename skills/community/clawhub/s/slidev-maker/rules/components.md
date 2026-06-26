# Slidev Components

Built-in components available in all slides.

## Arrow

Draw an arrow between two points.
```html
<Arrow x1="10" y1="20" x2="100" y2="200" />

<Arrow 
  x1="10" 
  y1="10" 
  x2="200" 
  y2="200" 
  width="3"
  color="red"
  two-way
/>
```

Props:
- `x1`, `y1` - Start point (required)
- `x2`, `y2` - End point (required)
- `width` - Line width (default: 2)
- `color` - Line color (default: currentColor)
- `two-way` - Draw arrows on both ends

## VDragArrow

An Arrow that can be dragged during presentation.
```html
<VDragArrow x1="10" y1="20" x2="100" y2="200" />
```

Same props as Arrow, but position can be adjusted by dragging.

## Link

Navigate to a specific slide.
```html
<Link to="42">Go to slide 42</Link>
<Link to="42" title="Go to slide 42" />
<Link to="solutions" title="Go to solutions" />
```

Props:
- `to` - Slide number or route alias
- `title` - Link text

Use `routeAlias` in frontmatter to create named routes:
```yaml
---
routeAlias: solutions
---
```

## Toc (Table of Contents)

Generate a table of contents from slide titles.
```html
<Toc />

<Toc 
  columns="2"
  maxDepth="2"
  minDepth="1"
  mode="all"
/>
```

Props:
- `columns` - Number of columns (default: 1)
- `maxDepth` - Maximum heading depth (default: Infinity)
- `minDepth` - Minimum heading depth (default: 1)
- `mode` - Display mode:
  - `'all'` - Show all items
  - `'onlyCurrentTree'` - Active item and its parents/children
  - `'onlySiblings'` - Current tree and siblings

Hide a slide from TOC:
```yaml
---
hideInToc: true
---
```

## SlidevVideo

Embed videos with presentation controls.
```html
<SlidevVideo autoplay controls>
  <source src="/video.mp4" type="video/mp4" />
  <source src="/video.webm" type="video/webm" />
</SlidevVideo>
```

Props:
- `controls` - Show video controls (default: false)
- `autoplay` - Auto-start video (default: false)
- `autoreset` - Reset video on navigation:
  - `'slide'` - Reset when returning to slide
  - `'click'` - Reset when returning to click
- `poster` - Image shown when not playing
- `timestamp` - Start time in seconds

## Youtube

Embed YouTube videos.
```html
<Youtube id="luoMHjh-XcQ" />

<Youtube 
  id="luoMHjh-XcQ" 
  width="600" 
  height="400" 
/>
```

Start at specific time with query parameter:
```html
<Youtube id="luoMHjh-XcQ?start=120" />
```

## Tweet

Embed tweets.
```html
<Tweet id="1234567890" />

<Tweet 
  id="1234567890" 
  scale="0.8"
  cards="hidden"
/>
```

## Transform

Scale or transform elements.
```html
<Transform :scale="0.5">
  <YourContent />
</Transform>

<Transform :scale="1.5" origin="top left">
  <LargerContent />
</Transform>
```

## AutoFitText

Text that scales to fit container.
```html
<AutoFitText :max="200" :min="50" modelValue="Your text here" />
```

Similar to PowerPoint/Keynote auto-fit text boxes.

## LightOrDark

Show different content based on theme.
```html
<LightOrDark>
  <template #dark>Dark mode content</template>
  <template #light>Light mode content</template>
</LightOrDark>
```

With images:
```html
<LightOrDark>
  <template #dark>
    <img src="/dark-logo.png" />
  </template>
  <template #light>
    <img src="/light-logo.png" />
  </template>
</LightOrDark>
```

## RenderWhen

Conditionally render based on context.
```html
<RenderWhen context="presenter">
  Only visible in presenter view
</RenderWhen>

<RenderWhen context="slide">
  Only visible in main slide view
</RenderWhen>
```

Context options:
- `'slide'` - Main slide view
- `'presenter'` - Presenter view
- `'previewNext'` - Next slide preview
- `'overview'` - Overview mode
- `'print'` - Print mode

## SlideCurrentNo and SlidesTotal

Display slide numbers.
```html
<SlideCurrentNo /> / <SlidesTotal />
```

Output: "5 / 20"