# GSAP Recipes Reference

Quick-reference recipes for common animation patterns.

---

## Scroll Recipes

### Reveal on scroll
```js
gsap.from(".reveal", {
  y: 24, autoAlpha: 0, duration: 0.8, ease: "power3.out",
  scrollTrigger: { trigger: ".reveal", start: "top 85%", toggleActions: "play none none reverse" }
});
```

### Staggered list reveal
```js
gsap.from(".list-item", {
  y: 30, autoAlpha: 0, duration: 0.6, stagger: 0.1, ease: "power3.out",
  scrollTrigger: { trigger: ".list", start: "top 80%" }
});
```

### Batched reveals (performance)
```js
ScrollTrigger.batch(".card", {
  onEnter: (elements) => gsap.from(elements, { y: 30, autoAlpha: 0, stagger: 0.1 }),
  start: "top 85%"
});
```

### Parallax background
```js
gsap.to(".bg", {
  yPercent: 30, ease: "none",
  scrollTrigger: { trigger: ".section", start: "top bottom", end: "bottom top", scrub: true }
});
```

### Pinned section with timeline
```js
const tl = gsap.timeline();
tl.from(".step1", { autoAlpha: 0 }).to(".step1", { autoAlpha: 0 }).from(".step2", { autoAlpha: 0 }, "<");
ScrollTrigger.create({ animation: tl, trigger: ".pinned", start: "top top", end: "+=2000", scrub: 1, pin: true });
```

### Horizontal scroll
```js
const panels = gsap.utils.toArray(".panel");
gsap.to(panels, {
  xPercent: -100 * (panels.length - 1), ease: "none",
  scrollTrigger: { trigger: ".container", pin: true, scrub: 1, end: () => "+=" + document.querySelector(".container").offsetWidth }
});
```

### Smooth scroll to anchor
```js
gsap.to(window, { duration: 1, scrollTo: { y: "#section", offsetY: 80 }, ease: "power2.out" });
```

---

## Interaction Recipes

### Hover scale
```js
el.addEventListener("mouseenter", () => gsap.to(el, { scale: 1.03, duration: 0.2, overwrite: "auto" }));
el.addEventListener("mouseleave", () => gsap.to(el, { scale: 1, duration: 0.25, overwrite: "auto" }));
```

### Magnetic button
```js
btn.addEventListener("mousemove", (e) => {
  const rect = btn.getBoundingClientRect();
  const x = (e.clientX - rect.left - rect.width / 2) * 0.3;
  const y = (e.clientY - rect.top - rect.height / 2) * 0.3;
  gsap.to(btn, { x, y, duration: 0.3 });
});
btn.addEventListener("mouseleave", () => gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: "elastic.out(1, 0.3)" }));
```

### Cursor follower (quickTo)
```js
const xTo = gsap.quickTo(".cursor", "x", { duration: 0.2, ease: "power3" });
const yTo = gsap.quickTo(".cursor", "y", { duration: 0.2, ease: "power3" });
window.addEventListener("pointermove", (e) => { xTo(e.clientX); yTo(e.clientY); });
```

### Draggable carousel
```js
Draggable.create(".slider", { type: "x", bounds: ".container", inertia: true, snap: v => Math.round(v / 300) * 300 });
```

---

## Text Recipes

### Character stagger (SplitText)
```js
const split = new SplitText(".headline", { type: "chars" });
gsap.from(split.chars, { y: 20, autoAlpha: 0, stagger: 0.02, duration: 0.4, ease: "power3.out" });
```

### Scramble text reveal
```js
gsap.to(".title", { duration: 1.5, scrambleText: { text: "REVEALED", chars: "XO", revealDelay: 0.5 } });
```

### Typing effect
```js
gsap.to(".text", { duration: 2, text: { value: "Hello World", delimiter: "" }, ease: "none" });
```

---

## SVG Recipes

### Stroke draw
```js
gsap.from(".path", { drawSVG: 0, duration: 2, ease: "power2.inOut" });
```

### Shape morph
```js
gsap.to("#shape1", { morphSVG: "#shape2", duration: 1, ease: "power2.inOut" });
```

### Motion path animation
```js
gsap.to(".element", { duration: 5, motionPath: { path: "#curve", align: "#curve", autoRotate: true }, ease: "none" });
```

---

## Layout Recipes

### Flip grid toggle
```js
const state = Flip.getState(".cards");
container.classList.toggle("grid");
Flip.from(state, { duration: 0.6, ease: "power2.inOut", stagger: 0.05 });
```

### Shared element transition
```js
const state = Flip.getState(".thumbnail");
modal.appendChild(thumbnail);
Flip.from(state, { duration: 0.5, ease: "power2.out" });
```

---

## Physics Recipes

### Ballistic throw
```js
gsap.to(".ball", { duration: 3, physics2D: { velocity: 500, angle: -60, gravity: 500 } });
```

### Wiggle shake
```js
CustomWiggle.create("shake", { wiggles: 8, type: "easeOut" });
gsap.to(".element", { rotation: 10, ease: "shake", duration: 0.5 });
```

### Bounce drop
```js
CustomBounce.create("drop", { strength: 0.6, squash: 2 });
gsap.to(".box", { y: 300, ease: "drop", duration: 1.2 });
```
