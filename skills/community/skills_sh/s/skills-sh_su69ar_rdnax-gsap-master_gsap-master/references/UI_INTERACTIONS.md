# GSAP UI Interactions Reference

Comprehensive recipes for building captivating UI interactions with GSAP.

---

## Button & Hover Effects

### Shine/Gloss Button Effect

```js
// HTML: <button class="shine-btn"><span class="shine"></span>Click Me</button>
// CSS: .shine { position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); transform: translateX(-100%); }

const btn = document.querySelector(".shine-btn");
btn.addEventListener("mouseenter", () => {
  gsap.fromTo(".shine", 
    { xPercent: -100 }, 
    { xPercent: 100, duration: 0.6, ease: "power2.inOut" }
  );
});
```

### Scale + Glow Hover

```js
const btns = gsap.utils.toArray(".glow-btn");
btns.forEach(btn => {
  btn.addEventListener("mouseenter", () => {
    gsap.to(btn, {
      scale: 1.05,
      boxShadow: "0 0 20px rgba(99, 102, 241, 0.6)",
      duration: 0.3,
      overwrite: "auto"
    });
  });
  btn.addEventListener("mouseleave", () => {
    gsap.to(btn, {
      scale: 1,
      boxShadow: "0 0 0px rgba(99, 102, 241, 0)",
      duration: 0.4,
      overwrite: "auto"
    });
  });
});
```

### Border Draw on Hover

```js
// CSS: .btn { position: relative; } .btn::before, .btn::after { content: ''; position: absolute; ... }
const btn = document.querySelector(".border-btn");
const tl = gsap.timeline({ paused: true });

tl.to(btn, { "--border-progress": 1, duration: 0.4, ease: "power2.out" });

btn.addEventListener("mouseenter", () => tl.play());
btn.addEventListener("mouseleave", () => tl.reverse());
```

### 3D Tilt Effect

```js
const card = document.querySelector(".tilt-card");
const maxRotation = 15;

card.addEventListener("mousemove", (e) => {
  const rect = card.getBoundingClientRect();
  const x = (e.clientX - rect.left) / rect.width - 0.5;
  const y = (e.clientY - rect.top) / rect.height - 0.5;
  
  gsap.to(card, {
    rotationY: x * maxRotation,
    rotationX: -y * maxRotation,
    transformPerspective: 1000,
    duration: 0.3,
    ease: "power2.out"
  });
});

card.addEventListener("mouseleave", () => {
  gsap.to(card, { rotationY: 0, rotationX: 0, duration: 0.5, ease: "elastic.out(1, 0.5)" });
});
```

---

## Magnetic Effects

### Magnetic Button (Enhanced)

```js
const magneticBtn = document.querySelector(".magnetic");
const strength = 0.4;
const returnEase = "elastic.out(1, 0.3)";

magneticBtn.addEventListener("mousemove", (e) => {
  const rect = magneticBtn.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  const deltaX = e.clientX - centerX;
  const deltaY = e.clientY - centerY;
  
  gsap.to(magneticBtn, {
    x: deltaX * strength,
    y: deltaY * strength,
    duration: 0.3,
    ease: "power2.out"
  });
  
  // Inner text moves more for depth
  gsap.to(magneticBtn.querySelector("span"), {
    x: deltaX * strength * 0.5,
    y: deltaY * strength * 0.5,
    duration: 0.3
  });
});

magneticBtn.addEventListener("mouseleave", () => {
  gsap.to(magneticBtn, { x: 0, y: 0, duration: 0.7, ease: returnEase });
  gsap.to(magneticBtn.querySelector("span"), { x: 0, y: 0, duration: 0.7, ease: returnEase });
});
```

### Magnetic Menu Items

```js
const menuItems = gsap.utils.toArray(".nav-item");

menuItems.forEach(item => {
  item.addEventListener("mouseenter", (e) => {
    gsap.to(item, { scale: 1.1, duration: 0.3 });
    gsap.to(item.querySelector(".underline"), { scaleX: 1, duration: 0.3 });
  });
  
  item.addEventListener("mousemove", (e) => {
    const rect = item.getBoundingClientRect();
    const x = (e.clientX - rect.left - rect.width / 2) * 0.2;
    gsap.to(item, { x, duration: 0.2 });
  });
  
  item.addEventListener("mouseleave", () => {
    gsap.to(item, { scale: 1, x: 0, duration: 0.5, ease: "elastic.out(1, 0.5)" });
    gsap.to(item.querySelector(".underline"), { scaleX: 0, duration: 0.3 });
  });
});
```

---

## Cursor Effects

### Custom Cursor with Trail

```js
const cursor = document.querySelector(".cursor");
const cursorTrail = document.querySelector(".cursor-trail");

const xTo = gsap.quickTo(cursor, "x", { duration: 0.15, ease: "power3" });
const yTo = gsap.quickTo(cursor, "y", { duration: 0.15, ease: "power3" });
const xToTrail = gsap.quickTo(cursorTrail, "x", { duration: 0.4, ease: "power3" });
const yToTrail = gsap.quickTo(cursorTrail, "y", { duration: 0.4, ease: "power3" });

window.addEventListener("pointermove", (e) => {
  xTo(e.clientX);
  yTo(e.clientY);
  xToTrail(e.clientX);
  yToTrail(e.clientY);
});
```

### Cursor Expand on Hover

```js
const cursor = document.querySelector(".custom-cursor");
const interactiveElements = document.querySelectorAll("a, button, .interactive");

interactiveElements.forEach(el => {
  el.addEventListener("mouseenter", () => {
    gsap.to(cursor, { scale: 2, backgroundColor: "rgba(255,255,255,0.2)", duration: 0.3 });
  });
  el.addEventListener("mouseleave", () => {
    gsap.to(cursor, { scale: 1, backgroundColor: "rgba(255,255,255,0.8)", duration: 0.3 });
  });
});
```

### Text-Following Cursor

```js
const cursorText = document.querySelector(".cursor-text");
const xTo = gsap.quickTo(cursorText, "x", { duration: 0.2, ease: "power3" });
const yTo = gsap.quickTo(cursorText, "y", { duration: 0.2, ease: "power3" });

window.addEventListener("pointermove", (e) => { xTo(e.clientX + 20); yTo(e.clientY + 20); });

document.querySelectorAll("[data-cursor-text]").forEach(el => {
  el.addEventListener("mouseenter", () => {
    cursorText.textContent = el.dataset.cursorText;
    gsap.to(cursorText, { autoAlpha: 1, scale: 1, duration: 0.3 });
  });
  el.addEventListener("mouseleave", () => {
    gsap.to(cursorText, { autoAlpha: 0, scale: 0.8, duration: 0.2 });
  });
});
```

---

## Draggable Patterns

### Carousel with Snap

```js
Draggable.create(".carousel-track", {
  type: "x",
  bounds: ".carousel-container",
  inertia: true,
  snap: {
    x: (value) => {
      const slideWidth = 320; // width + gap
      return Math.round(value / slideWidth) * slideWidth;
    }
  },
  onDrag: function() {
    // Update active indicator
    const currentSlide = Math.abs(Math.round(this.x / 320));
    updateIndicator(currentSlide);
  }
});
```

### Card Stack (Tinder-style)

```js
const cards = gsap.utils.toArray(".swipe-card");

cards.forEach((card, i) => {
  gsap.set(card, { zIndex: cards.length - i });
  
  Draggable.create(card, {
    type: "x,y",
    bounds: { minX: -500, maxX: 500, minY: -200, maxY: 200 },
    inertia: true,
    onDrag: function() {
      const rotation = this.x * 0.05;
      gsap.set(card, { rotation });
      
      // Show like/dislike indicators
      const opacity = Math.abs(this.x) / 200;
      if (this.x > 0) {
        gsap.to(".like-indicator", { autoAlpha: opacity });
      } else {
        gsap.to(".dislike-indicator", { autoAlpha: opacity });
      }
    },
    onDragEnd: function() {
      if (Math.abs(this.x) > 150) {
        // Swipe away
        gsap.to(card, {
          x: this.x > 0 ? 500 : -500,
          opacity: 0,
          rotation: this.x > 0 ? 30 : -30,
          duration: 0.3,
          onComplete: () => card.remove()
        });
      } else {
        // Snap back
        gsap.to(card, { x: 0, y: 0, rotation: 0, duration: 0.5, ease: "elastic.out(1, 0.5)" });
      }
      gsap.to(".like-indicator, .dislike-indicator", { autoAlpha: 0 });
    }
  });
});
```

### Knob/Dial Control

```js
Draggable.create(".knob", {
  type: "rotation",
  bounds: { minRotation: -150, maxRotation: 150 },
  inertia: true,
  snap: (value) => Math.round(value / 30) * 30, // Snap to 30° increments
  onDrag: function() {
    // Map rotation to value (0-100)
    const value = gsap.utils.mapRange(-150, 150, 0, 100, this.rotation);
    updateValue(Math.round(value));
  }
});
```

### Sortable List

```js
const listItems = gsap.utils.toArray(".sortable-item");

listItems.forEach(item => {
  Draggable.create(item, {
    type: "y",
    bounds: ".sortable-list",
    onDrag: function() {
      const siblings = listItems.filter(i => i !== item);
      const itemCenter = this.y + item.offsetHeight / 2;
      
      siblings.forEach(sibling => {
        const siblingRect = sibling.getBoundingClientRect();
        const siblingCenter = sibling.offsetTop + sibling.offsetHeight / 2;
        
        if (Math.abs(itemCenter - siblingCenter) < item.offsetHeight / 2) {
          // Swap positions
          const direction = itemCenter < siblingCenter ? -1 : 1;
          gsap.to(sibling, { y: direction * item.offsetHeight, duration: 0.2 });
        }
      });
    },
    onDragEnd: function() {
      // Reorder DOM
      reorderList();
    }
  });
});
```

---

## Flip Layout Patterns

### Grid/List Toggle

```js
const container = document.querySelector(".items-container");
const toggleBtn = document.querySelector(".view-toggle");
let isGrid = true;

toggleBtn.addEventListener("click", () => {
  const state = Flip.getState(".item");
  
  isGrid = !isGrid;
  container.classList.toggle("grid-view", isGrid);
  container.classList.toggle("list-view", !isGrid);
  
  Flip.from(state, {
    duration: 0.6,
    ease: "power2.inOut",
    stagger: 0.02,
    absolute: true,
    onEnter: elements => gsap.fromTo(elements, { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1 }),
    onLeave: elements => gsap.to(elements, { autoAlpha: 0, scale: 0.8 })
  });
});
```

### Shared Element Modal

```js
function openModal(thumbnail) {
  const modal = document.querySelector(".modal");
  const modalImage = modal.querySelector(".modal-image");
  
  // Capture state of thumbnail
  const state = Flip.getState(thumbnail);
  
  // Move thumbnail into modal (or clone for seamless effect)
  modalImage.style.backgroundImage = thumbnail.style.backgroundImage;
  modal.classList.add("open");
  
  // Animate from thumbnail position to modal
  Flip.from(state, {
    targets: modalImage,
    duration: 0.5,
    ease: "power2.out",
    absolute: true
  });
  
  // Fade in modal overlay
  gsap.to(".modal-overlay", { autoAlpha: 1, duration: 0.3 });
}

function closeModal() {
  const modal = document.querySelector(".modal");
  const modalImage = modal.querySelector(".modal-image");
  const thumbnail = document.querySelector(".active-thumbnail");
  
  const state = Flip.getState(modalImage);
  modal.classList.remove("open");
  
  Flip.from(state, {
    targets: thumbnail,
    duration: 0.4,
    ease: "power2.in"
  });
  
  gsap.to(".modal-overlay", { autoAlpha: 0, duration: 0.3 });
}
```

### Tab Content Transition

```js
const tabs = gsap.utils.toArray(".tab");
const contents = gsap.utils.toArray(".tab-content");

tabs.forEach((tab, i) => {
  tab.addEventListener("click", () => {
    // Capture current state
    const state = Flip.getState(".tab-indicator, .tab-content");
    
    // Update active states
    tabs.forEach(t => t.classList.remove("active"));
    contents.forEach(c => c.classList.remove("active"));
    tab.classList.add("active");
    contents[i].classList.add("active");
    
    // Move indicator
    Flip.from(state, {
      duration: 0.4,
      ease: "power2.out",
      targets: ".tab-indicator"
    });
    
    // Crossfade content
    gsap.fromTo(contents[i], 
      { autoAlpha: 0, y: 10 }, 
      { autoAlpha: 1, y: 0, duration: 0.3, delay: 0.1 }
    );
  });
});
```

### Accordion Expand

```js
document.querySelectorAll(".accordion-header").forEach(header => {
  header.addEventListener("click", () => {
    const item = header.parentElement;
    const content = item.querySelector(".accordion-content");
    const isOpen = item.classList.contains("open");
    
    // Capture state
    const state = Flip.getState(".accordion-item");
    
    // Toggle
    item.classList.toggle("open");
    
    // Animate layout
    Flip.from(state, {
      duration: 0.4,
      ease: "power2.out",
      nested: true
    });
    
    // Animate content
    if (!isOpen) {
      gsap.fromTo(content, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 });
    }
  });
});
```

---

## Add to Cart Effects

### Add to Cart with Flip

```js
function addToCart(productCard) {
  const productImage = productCard.querySelector(".product-image");
  const cartIcon = document.querySelector(".cart-icon");
  
  // Clone the image for animation
  const clone = productImage.cloneNode(true);
  clone.classList.add("flying-item");
  document.body.appendChild(clone);
  
  // Position clone at product location
  const startRect = productImage.getBoundingClientRect();
  gsap.set(clone, {
    position: "fixed",
    top: startRect.top,
    left: startRect.left,
    width: startRect.width,
    height: startRect.height,
    zIndex: 1000
  });
  
  // Animate to cart
  const endRect = cartIcon.getBoundingClientRect();
  gsap.to(clone, {
    top: endRect.top,
    left: endRect.left,
    width: 30,
    height: 30,
    opacity: 0.5,
    duration: 0.6,
    ease: "power2.inOut",
    onComplete: () => {
      clone.remove();
      // Bounce cart icon
      gsap.fromTo(cartIcon, { scale: 1.3 }, { scale: 1, duration: 0.4, ease: "elastic.out(1, 0.3)" });
      updateCartCount();
    }
  });
}
```

### Confetti Celebration

```js
function celebrateAddToCart() {
  const colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24", "#6c5ce7"];
  
  for (let i = 0; i < 30; i++) {
    const confetti = document.createElement("div");
    confetti.className = "confetti";
    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    document.body.appendChild(confetti);
    
    gsap.set(confetti, {
      x: window.innerWidth / 2,
      y: window.innerHeight / 2,
      width: gsap.utils.random(5, 10),
      height: gsap.utils.random(5, 10)
    });
    
    gsap.to(confetti, {
      x: `+=${gsap.utils.random(-200, 200)}`,
      y: `+=${gsap.utils.random(-300, -100)}`,
      rotation: gsap.utils.random(-360, 360),
      duration: gsap.utils.random(0.5, 1),
      ease: "power2.out",
      onComplete: () => {
        gsap.to(confetti, {
          y: `+=${gsap.utils.random(200, 400)}`,
          opacity: 0,
          duration: gsap.utils.random(0.5, 1),
          ease: "power1.in",
          onComplete: () => confetti.remove()
        });
      }
    });
  }
}
```

---

## Loading & Skeleton States

### Skeleton Shimmer

```js
// CSS: .skeleton { background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); background-size: 200% 100%; }

gsap.to(".skeleton", {
  backgroundPosition: "-200% 0",
  duration: 1.5,
  ease: "none",
  repeat: -1
});
```

### Content Load Transition

```js
function loadContent() {
  // Show skeletons
  gsap.set(".content", { autoAlpha: 0 });
  gsap.set(".skeleton", { autoAlpha: 1 });
  
  // Fetch content...
  fetchData().then(data => {
    // Populate content
    populateContent(data);
    
    // Fade out skeleton, fade in content
    gsap.to(".skeleton", { autoAlpha: 0, duration: 0.3 });
    gsap.to(".content", { autoAlpha: 1, duration: 0.4, delay: 0.2 });
    
    // Stagger reveal content items
    gsap.from(".content-item", {
      y: 20, autoAlpha: 0, stagger: 0.1, delay: 0.3, ease: "power3.out"
    });
  });
}
```

---

## Observer-Based UI

### Swipe Navigation (Observer)

```js
let currentSection = 0;
const sections = gsap.utils.toArray(".section");

Observer.create({
  target: window,
  type: "wheel,touch,pointer",
  onUp: () => gotoSection(currentSection - 1),
  onDown: () => gotoSection(currentSection + 1),
  tolerance: 50,
  preventDefault: true,
  wheelSpeed: -1
});

function gotoSection(index) {
  index = gsap.utils.clamp(0, sections.length - 1, index);
  if (index === currentSection) return;
  
  gsap.to(sections[currentSection], { autoAlpha: 0, duration: 0.3 });
  gsap.to(sections[index], { autoAlpha: 1, duration: 0.3 });
  
  currentSection = index;
  updateNav();
}
```

### Pull to Refresh

```js
let pullDistance = 0;
const threshold = 100;

Observer.create({
  target: ".scrollable-content",
  type: "touch",
  onDrag: (self) => {
    if (self.startY < 100 && self.deltaY > 0) {
      pullDistance = Math.min(self.deltaY, threshold * 1.5);
      gsap.set(".refresh-indicator", { y: pullDistance, opacity: pullDistance / threshold });
      gsap.set(".refresh-icon", { rotation: pullDistance * 3 });
    }
  },
  onDragEnd: () => {
    if (pullDistance >= threshold) {
      // Trigger refresh
      gsap.to(".refresh-indicator", { y: 60, duration: 0.3 });
      refreshContent().then(() => {
        gsap.to(".refresh-indicator", { y: 0, opacity: 0, duration: 0.3 });
      });
    } else {
      gsap.to(".refresh-indicator", { y: 0, opacity: 0, duration: 0.3 });
    }
    pullDistance = 0;
  }
});
```

---

## Micro-interactions

### Success Checkmark

```js
function showSuccess() {
  const tl = gsap.timeline();
  
  tl.to(".submit-btn", { scale: 0.9, duration: 0.1 })
    .to(".submit-btn", { scale: 1, borderRadius: "50%", width: 50, duration: 0.3 })
    .to(".btn-text", { autoAlpha: 0, duration: 0.1 }, "<")
    .fromTo(".checkmark", 
      { drawSVG: 0 }, 
      { drawSVG: "100%", duration: 0.4, ease: "power2.out" }
    )
    .to(".submit-btn", { backgroundColor: "#10b981", duration: 0.2 }, "<");
  
  return tl;
}
```

### Shake on Error

```js
function shakeError(element) {
  gsap.to(element, {
    x: [-10, 10, -10, 10, -5, 5, 0],
    duration: 0.5,
    ease: "power2.out"
  });
  
  gsap.to(element, {
    borderColor: "#ef4444",
    boxShadow: "0 0 0 3px rgba(239, 68, 68, 0.2)",
    duration: 0.2
  });
}
```

### Input Focus Animation

```js
const inputs = document.querySelectorAll(".floating-input");

inputs.forEach(input => {
  const label = input.parentElement.querySelector("label");
  const underline = input.parentElement.querySelector(".underline");
  
  input.addEventListener("focus", () => {
    gsap.to(label, { y: -20, scale: 0.8, color: "#6366f1", duration: 0.3 });
    gsap.to(underline, { scaleX: 1, duration: 0.3, ease: "power2.out" });
  });
  
  input.addEventListener("blur", () => {
    if (!input.value) {
      gsap.to(label, { y: 0, scale: 1, color: "#9ca3af", duration: 0.3 });
    }
    gsap.to(underline, { scaleX: 0, duration: 0.3 });
  });
});
```

### Copy to Clipboard Feedback

```js
function copyToClipboard(text, button) {
  navigator.clipboard.writeText(text);
  
  const originalText = button.textContent;
  
  gsap.timeline()
    .to(button, { scale: 0.9, duration: 0.1 })
    .to(button, { scale: 1, duration: 0.1 })
    .call(() => { button.textContent = "Copied!"; })
    .to(button, { backgroundColor: "#10b981", duration: 0.2 })
    .to(button, { backgroundColor: "", duration: 0.3 }, "+=1")
    .call(() => { button.textContent = originalText; });
}
```

---

## Tooltip & Popover

### Animated Tooltip

```js
const tooltips = document.querySelectorAll("[data-tooltip]");

tooltips.forEach(el => {
  const tooltip = document.createElement("div");
  tooltip.className = "tooltip";
  tooltip.textContent = el.dataset.tooltip;
  el.appendChild(tooltip);
  
  gsap.set(tooltip, { autoAlpha: 0, y: 10, scale: 0.9 });
  
  el.addEventListener("mouseenter", () => {
    gsap.to(tooltip, { autoAlpha: 1, y: 0, scale: 1, duration: 0.2, ease: "back.out(2)" });
  });
  
  el.addEventListener("mouseleave", () => {
    gsap.to(tooltip, { autoAlpha: 0, y: 10, scale: 0.9, duration: 0.15 });
  });
});
```

### Context Menu

```js
const contextMenu = document.querySelector(".context-menu");

document.addEventListener("contextmenu", (e) => {
  e.preventDefault();
  
  gsap.set(contextMenu, { x: e.clientX, y: e.clientY });
  gsap.fromTo(contextMenu, 
    { autoAlpha: 0, scale: 0.9 }, 
    { autoAlpha: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }
  );
  
  gsap.from(".context-menu-item", {
    y: -10, autoAlpha: 0, stagger: 0.03, duration: 0.2, delay: 0.05
  });
});

document.addEventListener("click", () => {
  gsap.to(contextMenu, { autoAlpha: 0, scale: 0.95, duration: 0.15 });
});
```
