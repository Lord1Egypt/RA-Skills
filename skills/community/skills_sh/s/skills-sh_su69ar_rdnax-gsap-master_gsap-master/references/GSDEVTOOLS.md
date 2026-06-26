# GSDevTools Reference

Visual debugging UI for GSAP animations with playback controls, keyboard shortcuts, and inspection tools.

---

## Quick Start

### Installation

```html
<!-- CDN -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/GSDevTools.min.js"></script>

<!-- or NPM import -->
import { gsap } from "gsap";
import { GSDevTools } from "gsap/GSDevTools";
gsap.registerPlugin(GSDevTools);
```

### Basic Usage

```js
// Attach to global timeline (all animations)
GSDevTools.create();

// Better: Attach to specific animation
const tl = gsap.timeline();
tl.to(".box", { x: 200 })
  .to(".box", { rotation: 360 });

GSDevTools.create({ animation: tl });
```

---

## Configuration Options

```js
GSDevTools.create({
  // Animation to control
  animation: myTimeline,           // Timeline or Tween instance
  animation: "myId",               // Or animation ID string
  
  // Container & Styling
  container: "#devtools-container",// Element to render in
  css: { bottom: "30px", width: "50%" }, // Custom styling
  
  // Initial State
  paused: true,                    // Start paused
  loop: true,                      // Start in loop mode
  timeScale: 0.5,                  // Initial speed (0.5 = half speed)
  inTime: 0.5,                     // In-point (seconds or label)
  outTime: 2,                      // Out-point (seconds or label)
  
  // Behavior
  globalSync: false,               // Sync with global timeline
  keyboard: true,                  // Enable keyboard shortcuts
  persist: true,                   // Remember settings between refreshes
  minimal: false,                  // Minimal UI mode
  visibility: "auto",              // "auto" = auto-hide when mouse leaves
  
  // Control visibility
  hideGlobalTimeline: true,        // Hide "Global Timeline" from menu
  
  // Identification
  id: "main-devtools"              // Unique ID for this instance
});
```

---

## Animation IDs

Assign IDs to animations so they appear in the animation menu:

```js
// Timeline with ID
const tl = gsap.timeline({ id: "hero-animation" });
tl.to(".hero", { x: 100 })
  .to(".hero", { rotation: 360 });

// Individual tweens with IDs
gsap.to(".box1", { x: 200, id: "box1-slide" });
gsap.to(".box2", { y: 100, id: "box2-drop" });

// Access by ID in GSDevTools
GSDevTools.create(); // All IDs appear in dropdown
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **SPACEBAR** | Play/Pause |
| **UP ARROW** | Increase timeScale |
| **DOWN ARROW** | Decrease timeScale |
| **LEFT ARROW** | Rewind to start |
| **RIGHT ARROW** | Jump to end |
| **L** | Toggle loop |
| **I** | Set in-point at playhead |
| **O** | Set out-point at playhead |
| **H** | Hide/Show UI |

---

## Methods

### Get by ID

```js
GSDevTools.create({ id: "main" });

// Later, retrieve the instance
const devtools = GSDevTools.getById("main");
```

### Kill/Remove

```js
const devtools = GSDevTools.create({ id: "main" });

// Remove the devtools instance
devtools.kill();

// Or by ID
GSDevTools.getById("main").kill();
```

---

## Persistence

GSDevTools remembers these settings between page refreshes:
- In/out points
- Selected animation
- TimeScale
- Loop state

### Disable Persistence

```js
GSDevTools.create({
  persist: false  // Don't remember settings
});
```

### Avoid Contamination

If multiple GSDevTools instances share settings unexpectedly, use unique IDs:

```js
GSDevTools.create({ id: "page-a-devtools" });
GSDevTools.create({ id: "page-b-devtools" });
```

---

## Tips & Tricks

### Double-click to Reset Markers

Double-click on in/out markers to reset them to start/end.

### Quick Link to Docs

Click the GSAP logo (bottom right) to open documentation.

### Hide UI but Keep Shortcuts

Press **H** to hide the UI while still using keyboard shortcuts.

### Best Practice: Link to Specific Animation

```js
// ✅ Best - Simpler, no global sync needed
GSDevTools.create({ animation: myTimeline });

// ⚠️ Okay - Works but more complex
GSDevTools.create();  // Controls everything
```

---

## Common Issues

### Timeline Shows 1000 Seconds

You have an infinite repeat animation. GSDevTools caps at 1000 seconds.

```js
// This causes 1000s timeline
gsap.to(".box", { x: 100, repeat: -1 });

// Fix: Exclude from global, use specific animation
const tl = gsap.timeline();
tl.to(".box", { x: 100, repeat: -1 });
GSDevTools.create({ animation: tl });
```

### Doesn't Work with ScrollTrigger

GSDevTools cannot control ScrollTrigger-driven animations because ScrollTrigger needs the scrollbar to control progress.

```js
// ❌ Won't work - ScrollTrigger controls this
gsap.to(".box", {
  x: 500,
  scrollTrigger: { scrub: true }
});

// ✅ Works - No ScrollTrigger
const tl = gsap.timeline();
tl.to(".box", { x: 500 });
GSDevTools.create({ animation: tl });
```

---

## Development Workflow

### Setup for Development

```js
// Only load in development
if (process.env.NODE_ENV === "development") {
  gsap.registerPlugin(GSDevTools);
  GSDevTools.create({ animation: mainTimeline });
}
```

### React/Next.js Pattern

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";

// Only import in dev
let GSDevTools;
if (process.env.NODE_ENV === "development") {
  import("gsap/GSDevTools").then(module => {
    GSDevTools = module.GSDevTools;
    gsap.registerPlugin(GSDevTools);
  });
}

export function AnimatedSection() {
  const containerRef = useRef(null);
  const tlRef = useRef(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      tlRef.current = gsap.timeline({ id: "section-anim" });
      tlRef.current
        .from(".title", { y: 30, autoAlpha: 0 })
        .from(".content", { y: 20, autoAlpha: 0 });

      // Dev tools in development only
      if (process.env.NODE_ENV === "development" && GSDevTools) {
        GSDevTools.create({ animation: tlRef.current, id: "section" });
      }
    }, containerRef);

    return () => {
      if (process.env.NODE_ENV === "development" && GSDevTools) {
        GSDevTools.getById("section")?.kill();
      }
      ctx.revert();
    };
  }, []);

  return (
    <section ref={containerRef}>
      <h1 className="title">Title</h1>
      <div className="content">Content</div>
    </section>
  );
}
```

---

## Minimal Mode

For mobile or small viewports:

```js
GSDevTools.create({
  minimal: true  // Only scrubber, play/pause, timeScale
});

// Note: Automatically switches to minimal under 600px width
```

---

## Custom Container

```js
// Render inside a specific element
GSDevTools.create({
  container: "#my-devtools-panel",
  css: { position: "relative", width: "100%" }
});
```

---

## Global Sync

Sync all animations together:

```js
GSDevTools.create({
  globalSync: true  // Scrubbing one scrubs all
});
```

**Note:** This can be confusing with many independent animations. Use sparingly.

---

## Debugging Complex Sequences

### Add IDs to Child Tweens

```js
const tl = gsap.timeline({ id: "master" });

tl.to(".intro", { x: 100, id: "intro-slide" })
  .to(".hero", { scale: 1.2, id: "hero-scale" })
  .to(".content", { autoAlpha: 1, id: "content-fade" });

GSDevTools.create();
// Now you can jump to any of these in the dropdown
```

### Slow Motion Review

```js
// Start in slow motion for detailed inspection
GSDevTools.create({
  timeScale: 0.25,  // Quarter speed
  paused: true
});
```

### Focus on Specific Section

```js
// Isolate a section of the timeline
GSDevTools.create({
  animation: myTimeline,
  inTime: "intro",    // Start at label
  outTime: 1.5        // End at 1.5 seconds
});
```
