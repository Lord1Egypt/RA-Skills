# GSAP Core Reference

Complete reference for GSAP Core fundamentals - tweens, timelines, easing, utilities, and callbacks.

---

## The 4 Primitives

### gsap.to() - Animate TO values

```js
gsap.to(".box", {
  x: 200,
  rotation: 360,
  duration: 1,
  ease: "power2.out"
});
```

### gsap.from() - Animate FROM values

```js
// Element starts at these values and animates to current CSS state
gsap.from(".box", {
  x: -200,
  autoAlpha: 0,
  duration: 1
});
```

### gsap.fromTo() - Explicit start and end

```js
gsap.fromTo(".box",
  { x: 0, opacity: 0 },          // FROM
  { x: 200, opacity: 1, duration: 1 }  // TO
);
```

### gsap.set() - Instant set (no animation)

```js
gsap.set(".box", { x: 100, opacity: 0.5 });
```

---

## Core Properties

### Transform Properties (Preferred - GPU Accelerated)

```js
gsap.to(".box", {
  x: 100,           // translateX
  y: 50,            // translateY
  z: 10,            // translateZ (3D)
  xPercent: -50,    // percentage-based translateX
  yPercent: -50,    // percentage-based translateY
  rotation: 360,    // rotate (degrees)
  rotationX: 45,    // 3D rotateX
  rotationY: 45,    // 3D rotateY
  rotationZ: 45,    // same as rotation
  scale: 1.5,       // uniform scale
  scaleX: 2,        // scale width
  scaleY: 0.5,      // scale height
  skewX: 15,        // skew X (degrees)
  skewY: 15,        // skew Y (degrees)
  transformOrigin: "center center",
  transformPerspective: 1000
});
```

### CSS Properties

```js
gsap.to(".box", {
  opacity: 0.5,
  backgroundColor: "#ff0000",
  color: "blue",
  borderRadius: "50%",
  boxShadow: "0 10px 20px rgba(0,0,0,0.3)",
  width: 200,       // Avoid if possible (causes layout)
  height: 100,      // Avoid if possible (causes layout)
  padding: 20,
  margin: "10px 20px"
});
```

### Special Properties

```js
gsap.to(".box", {
  autoAlpha: 0,     // opacity + visibility (hides when 0)
  clearProps: "all", // Reset to CSS on complete
  immediateRender: false,
  overwrite: "auto",
  attr: { cx: 100, cy: 50 },  // SVG attributes
  css: { display: "flex" }    // Force CSS interpretation
});
```

---

## Timing & Control Properties

```js
gsap.to(".box", {
  duration: 1,          // Seconds (default: 0.5)
  delay: 0.5,          // Delay before start
  repeat: 3,           // Number of repeats (-1 = infinite)
  repeatDelay: 0.5,    // Delay between repeats
  yoyo: true,          // Reverse on alternate repeats
  ease: "power2.out",  // Easing function
  stagger: 0.1,        // Stagger for multiple elements
  paused: true,        // Start paused
  reversed: true       // Start in reverse
});
```

---

## Easing Reference

### Power Eases (Most Common)

```js
"power1.out"    // Subtle (linear-ish)
"power2.out"    // Standard, natural feel
"power3.out"    // Pronounced deceleration
"power4.out"    // Strong deceleration

// Directions
"power2.in"     // Starts slow, ends fast
"power2.out"    // Starts fast, ends slow
"power2.inOut"  // Slow at both ends
```

### Special Eases

```js
"none" or "linear"       // Constant speed
"back.out(1.7)"          // Overshoot and settle
"elastic.out(1, 0.3)"    // Springy bounce
"bounce.out"             // Ball bounce effect
"circ.out"               // Circular motion
"expo.out"               // Exponential
"sine.inOut"             // Gentle, wave-like
"steps(5)"               // Stepped animation
```

### Custom Eases (with CustomEase plugin)

```js
gsap.registerPlugin(CustomEase);

CustomEase.create("myEase", "M0,0 C0.25,0.1 0.25,1 1,1");
gsap.to(".box", { x: 100, ease: "myEase" });
```

---

## Stagger Options

### Simple Stagger

```js
gsap.from(".item", {
  y: 50,
  autoAlpha: 0,
  stagger: 0.1  // 0.1 seconds between each
});
```

### Advanced Stagger Object

```js
gsap.from(".item", {
  y: 50,
  autoAlpha: 0,
  stagger: {
    each: 0.1,           // Time between each
    amount: 1,           // Total stagger time (alternative to each)
    from: "start",       // "start", "end", "center", "edges", "random", or index
    grid: [3, 5],        // [rows, cols] for grid layouts
    axis: "x",           // "x" or "y" for grid
    ease: "power2.in",   // Easing for stagger distribution
    repeat: -1,          // Repeat stagger sequence
    yoyo: true           // Reverse stagger on repeat
  }
});
```

### Stagger Examples

```js
// From center outward
gsap.from(".grid-item", { scale: 0, stagger: { from: "center", amount: 0.5 } });

// Random order
gsap.from(".item", { y: 30, stagger: { each: 0.05, from: "random" } });

// Grid wave effect
gsap.from(".grid-item", {
  scale: 0,
  stagger: {
    grid: "auto",
    from: "center",
    axis: "x",
    each: 0.05
  }
});
```

---

## Callbacks

```js
gsap.to(".box", {
  x: 200,
  duration: 1,
  
  // Animation lifecycle
  onStart: () => console.log("Started"),
  onUpdate: () => console.log("Updating..."),
  onComplete: () => console.log("Complete!"),
  onRepeat: () => console.log("Repeating..."),
  onReverseComplete: () => console.log("Reverse complete"),
  
  // With parameters
  onCompleteParams: ["done", 123],
  onComplete: (msg, num) => console.log(msg, num),
  
  // Access tween/timeline inside callback
  onUpdate: function() {
    console.log(this.progress()); // 'this' = tween
  }
});
```

---

## Timeline (Sequencing Tool)

### Basic Timeline

```js
const tl = gsap.timeline();

tl.to(".box1", { x: 100, duration: 0.5 })
  .to(".box2", { x: 100, duration: 0.5 })
  .to(".box3", { x: 100, duration: 0.5 });
```

### Timeline Defaults

```js
const tl = gsap.timeline({
  defaults: {
    duration: 0.6,
    ease: "power3.out"
  }
});

// Individual tweens can override defaults
tl.to(".title", { y: 30 })
  .to(".subtitle", { y: 20, duration: 0.4 }); // Override duration
```

### Position Parameters

```js
const tl = gsap.timeline();

tl.to(".a", { x: 100 })
  .to(".b", { x: 100 }, "<")       // Same time as previous
  .to(".c", { x: 100 }, ">")       // After previous ends
  .to(".d", { x: 100 }, "+=0.5")   // 0.5s after previous
  .to(".e", { x: 100 }, "-=0.3")   // 0.3s before previous ends
  .to(".f", { x: 100 }, 2)         // At 2 seconds
  .to(".g", { x: 100 }, "myLabel") // At label position
  .to(".h", { x: 100 }, "<0.2");   // 0.2s after start of previous
```

### Labels

```js
const tl = gsap.timeline();

tl.addLabel("intro")
  .to(".title", { y: 30 })
  .to(".subtitle", { y: 20 })
  .addLabel("body")
  .to(".content", { autoAlpha: 1 })
  .addLabel("end");

// Jump to label
tl.seek("body");
```

### Timeline Control Methods

```js
const tl = gsap.timeline({ paused: true });

// Playback
tl.play();           // Play forward
tl.pause();          // Pause
tl.resume();         // Resume from current position
tl.reverse();        // Play backward
tl.restart();        // Restart from beginning
tl.seek(1.5);        // Jump to 1.5 seconds
tl.seek("labelName");// Jump to label

// Speed
tl.timeScale(2);     // 2x speed
tl.timeScale(0.5);   // Half speed

// Progress (0-1)
tl.progress();       // Get progress
tl.progress(0.5);    // Set to halfway

// State
tl.isActive();       // Is currently animating
tl.paused();         // Is paused
tl.reversed();       // Is reversed

// Cleanup
tl.kill();           // Stop and remove
tl.revert();         // Stop, remove, and reset to original state
```

### Nested Timelines

```js
function introAnimation() {
  const tl = gsap.timeline();
  tl.from(".logo", { autoAlpha: 0 })
    .from(".tagline", { y: 20, autoAlpha: 0 });
  return tl;
}

function contentAnimation() {
  const tl = gsap.timeline();
  tl.from(".hero", { y: 50, autoAlpha: 0 })
    .from(".cards", { y: 30, autoAlpha: 0, stagger: 0.1 });
  return tl;
}

// Master timeline
const master = gsap.timeline();
master
  .add(introAnimation())
  .add(contentAnimation(), "-=0.3")
  .addLabel("end");
```

---

## Utilities

### gsap.utils

```js
// Arrays
gsap.utils.toArray(".item");           // NodeList to Array
gsap.utils.shuffle([1,2,3,4,5]);       // Randomize array

// Math
gsap.utils.clamp(0, 100, value);       // Clamp between min/max
gsap.utils.mapRange(0, 100, 0, 1, 50); // Map value to new range
gsap.utils.normalize(0, 100, 50);      // Normalize to 0-1
gsap.utils.interpolate(0, 100, 0.5);   // Get value at position
gsap.utils.snap(10, 47);               // Snap to nearest 10 → 50
gsap.utils.snap([0, 25, 50, 100], 47); // Snap to nearest in array → 50
gsap.utils.wrap(0, 10, 12);            // Wrap value in range → 2
gsap.utils.wrapYoyo(0, 10, 12);        // Wrap with yoyo → 8

// Random
gsap.utils.random(1, 10);              // Random between 1-10
gsap.utils.random([1, 5, 10]);         // Random from array
gsap.utils.random(1, 10, 2);           // Random, snapped to 2

// Functions
gsap.utils.pipe(fn1, fn2, fn3);        // Compose functions
gsap.utils.unitize(fn, "px");          // Add unit to function output
gsap.utils.selector(container);        // Scoped selector function
```

### gsap.getProperty / gsap.setProperty

```js
// Get computed value
gsap.getProperty(".box", "x");         // Returns number
gsap.getProperty(".box", "x", "px");   // Returns with unit

// Set value instantly
gsap.setProperty(".box", "x", 100);
```

### gsap.quickTo / gsap.quickSetter

```js
// quickTo - For animated tracking (mouse followers)
const xTo = gsap.quickTo(".cursor", "x", { duration: 0.3, ease: "power3" });
const yTo = gsap.quickTo(".cursor", "y", { duration: 0.3, ease: "power3" });
window.addEventListener("pointermove", e => { xTo(e.clientX); yTo(e.clientY); });

// quickSetter - For immediate updates (no animation)
const setX = gsap.quickSetter(".cursor", "x", "px");
const setY = gsap.quickSetter(".cursor", "y", "px");
window.addEventListener("pointermove", e => { setX(e.clientX); setY(e.clientY); });
```

---

## Responsive & Accessibility

### gsap.matchMedia()

```js
const mm = gsap.matchMedia();

mm.add({
  // Conditions
  isDesktop: "(min-width: 800px)",
  isMobile: "(max-width: 799px)",
  reduceMotion: "(prefers-reduced-motion: reduce)"
}, (context) => {
  let { isDesktop, isMobile, reduceMotion } = context.conditions;
  
  if (reduceMotion) {
    // No animations for reduced motion preference
    gsap.set(".hero", { autoAlpha: 1 });
  } else if (isDesktop) {
    // Desktop animations
    gsap.from(".hero", { x: -100, autoAlpha: 0 });
  } else {
    // Mobile animations
    gsap.from(".hero", { y: 50, autoAlpha: 0 });
  }
  
  // Cleanup happens automatically when condition changes
});
```

### gsap.context()

```js
// Scope animations and auto-cleanup
const ctx = gsap.context(() => {
  gsap.to(".box", { x: 100 });
  gsap.from(".title", { autoAlpha: 0 });
  
  ScrollTrigger.create({ ... });
}, containerElement);

// Cleanup all animations/triggers in context
ctx.revert();
```

---

## Global Timeline

```js
// Access global timeline
gsap.globalTimeline.pause();
gsap.globalTimeline.timeScale(0.5);  // Slow motion everything
gsap.globalTimeline.getChildren();   // Get all active tweens/timelines
```

---

## Keyframes

### Array Syntax

```js
gsap.to(".box", {
  keyframes: [
    { x: 100, duration: 1 },
    { y: 100, duration: 0.5 },
    { x: 0, duration: 1 },
    { y: 0, duration: 0.5 }
  ]
});
```

### Object Syntax (Percentage-based)

```js
gsap.to(".box", {
  keyframes: {
    "0%": { x: 0, y: 0 },
    "25%": { x: 100, y: 0 },
    "50%": { x: 100, y: 100 },
    "75%": { x: 0, y: 100 },
    "100%": { x: 0, y: 0 }
  },
  duration: 4
});
```

---

## Modifiers

```js
// Modify values on each frame
gsap.to(".box", {
  x: 500,
  modifiers: {
    x: (x) => gsap.utils.snap(100, x) // Snap to 100px increments
  }
});

// Wrap infinite carousel
gsap.to(".item", {
  x: "+=500",
  duration: 5,
  repeat: -1,
  ease: "none",
  modifiers: {
    x: gsap.utils.unitize(x => gsap.utils.wrap(0, 500, parseFloat(x)))
  }
});
```

---

## Effects (Reusable Animations)

```js
// Register a custom effect
gsap.registerEffect({
  name: "fade",
  effect: (targets, config) => {
    return gsap.to(targets, {
      duration: config.duration,
      autoAlpha: config.endAlpha,
      ease: config.ease
    });
  },
  defaults: { duration: 1, endAlpha: 0, ease: "power2.out" },
  extendTimeline: true
});

// Use the effect
gsap.effects.fade(".box");
gsap.effects.fade(".box", { duration: 2, endAlpha: 0.5 });

// In timeline (if extendTimeline: true)
const tl = gsap.timeline();
tl.fade(".box1")
  .fade(".box2", { duration: 0.5 }, "<");
```

---

## Ticker (Frame Loop)

```js
// Add function to run on every frame
function update(time, deltaTime, frame) {
  // Custom logic
}
gsap.ticker.add(update);

// Remove function
gsap.ticker.remove(update);

// Get frame rate
gsap.ticker.fps(60);          // Set target FPS
gsap.ticker.lagSmoothing(0);  // Disable lag smoothing

// Sync with requestAnimationFrame
gsap.ticker.deltaRatio();     // Get ratio for frame-rate independence
```
