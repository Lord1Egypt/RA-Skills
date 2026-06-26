# GSAP Text Animations Reference

Comprehensive recipes for stunning text animations with GSAP.

---

## SplitText Fundamentals

### Basic Setup & Cleanup

```js
gsap.registerPlugin(SplitText);

// Split into chars, words, and lines
const split = new SplitText(".headline", {
  type: "chars,words,lines",
  linesClass: "line",
  wordsClass: "word",
  charsClass: "char"
});

// Access split elements
console.log(split.chars);  // Array of char spans
console.log(split.words);  // Array of word spans
console.log(split.lines);  // Array of line wrappers

// IMPORTANT: Revert on cleanup (React/resize)
// split.revert();
```

### Split Types Explained

```js
// Characters only
new SplitText(".text", { type: "chars" });

// Words only
new SplitText(".text", { type: "words" });

// Lines only (great for mask reveals)
new SplitText(".text", { type: "lines" });

// Combined (most flexible)
new SplitText(".text", { type: "chars,words,lines" });
```

### Accessibility Considerations

```js
// SplitText automatically handles aria-label for screen readers
const split = new SplitText(".headline", {
  type: "chars",
  aria: "auto" // Default behavior
});

// For critical text, ensure original content is accessible
const element = document.querySelector(".headline");
element.setAttribute("aria-label", element.textContent);
```

---

## Character Animations

### Staggered Character Reveal

```js
const split = new SplitText(".title", { type: "chars" });

gsap.from(split.chars, {
  y: 50,
  autoAlpha: 0,
  duration: 0.6,
  stagger: 0.02,
  ease: "back.out(1.7)"
});
```

### Character Wave Effect

```js
const split = new SplitText(".wave-text", { type: "chars" });

gsap.to(split.chars, {
  y: -20,
  duration: 0.4,
  stagger: {
    each: 0.05,
    repeat: -1,
    yoyo: true
  },
  ease: "sine.inOut"
});
```

### Rotating Characters In

```js
const split = new SplitText(".rotate-text", { type: "chars" });

gsap.from(split.chars, {
  rotationX: -90,
  autoAlpha: 0,
  duration: 0.8,
  stagger: 0.03,
  transformOrigin: "50% 50% -30px",
  ease: "back.out(1.5)"
});
```

### Random Character Scatter

```js
const split = new SplitText(".scatter-text", { type: "chars" });

gsap.from(split.chars, {
  x: () => gsap.utils.random(-100, 100),
  y: () => gsap.utils.random(-100, 100),
  rotation: () => gsap.utils.random(-180, 180),
  autoAlpha: 0,
  scale: 0,
  duration: 0.8,
  stagger: 0.02,
  ease: "back.out(2)"
});
```

### Typewriter Effect (Character by Character)

```js
const split = new SplitText(".typewriter", { type: "chars" });

// Hide all initially
gsap.set(split.chars, { autoAlpha: 0 });

// Reveal one by one
gsap.to(split.chars, {
  autoAlpha: 1,
  duration: 0.05,
  stagger: 0.05,
  ease: "none"
});
```

### Character Color Wave

```js
const split = new SplitText(".color-wave", { type: "chars" });
const colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24", "#6c5ce7"];

gsap.to(split.chars, {
  color: (i) => colors[i % colors.length],
  duration: 0.3,
  stagger: {
    each: 0.02,
    repeat: -1,
    yoyo: true
  }
});
```

---

## Word Animations

### Word-by-Word Reveal

```js
const split = new SplitText(".paragraph", { type: "words" });

gsap.from(split.words, {
  y: 30,
  autoAlpha: 0,
  duration: 0.5,
  stagger: 0.08,
  ease: "power3.out"
});
```

### Words from Different Directions

```js
const split = new SplitText(".title", { type: "words" });

gsap.from(split.words, {
  x: (i) => (i % 2 === 0 ? -100 : 100),
  autoAlpha: 0,
  duration: 0.8,
  stagger: 0.1,
  ease: "power3.out"
});
```

### Word Scale Pop

```js
const split = new SplitText(".pop-words", { type: "words" });

gsap.from(split.words, {
  scale: 0,
  autoAlpha: 0,
  duration: 0.6,
  stagger: 0.1,
  ease: "elastic.out(1, 0.5)"
});
```

### Word Highlight on Scroll

```js
const split = new SplitText(".story", { type: "words" });

split.words.forEach((word, i) => {
  gsap.to(word, {
    color: "#6366f1",
    fontWeight: "bold",
    scrollTrigger: {
      trigger: word,
      start: "top 80%",
      end: "top 30%",
      scrub: true
    }
  });
});
```

---

## Line Animations

### Line-by-Line Reveal (Clean)

```js
const split = new SplitText(".paragraph", { type: "lines" });

gsap.from(split.lines, {
  y: 40,
  autoAlpha: 0,
  duration: 0.8,
  stagger: 0.15,
  ease: "power3.out"
});
```

### Line Mask Reveal (Premium Effect)

```js
// CSS: .line { overflow: hidden; }
const split = new SplitText(".masked-text", { type: "lines", linesClass: "line-wrapper" });

// Wrap each line's content in an inner div
split.lines.forEach(line => {
  const inner = document.createElement("div");
  inner.className = "line-inner";
  inner.innerHTML = line.innerHTML;
  line.innerHTML = "";
  line.appendChild(inner);
});

// Animate the inner content up from below
gsap.from(".line-inner", {
  yPercent: 100,
  duration: 0.8,
  stagger: 0.1,
  ease: "power3.out"
});
```

### Alternating Line Slide

```js
const split = new SplitText(".slide-text", { type: "lines" });

gsap.from(split.lines, {
  x: (i) => (i % 2 === 0 ? -100 : 100),
  autoAlpha: 0,
  duration: 0.8,
  stagger: 0.12,
  ease: "power3.out"
});
```

### Line Clip Reveal

```js
// CSS: .line-wrapper { clip-path: inset(100% 0 0 0); }
const split = new SplitText(".clip-text", { type: "lines", linesClass: "line-wrapper" });

gsap.to(split.lines, {
  clipPath: "inset(0% 0 0 0)",
  duration: 0.8,
  stagger: 0.15,
  ease: "power3.out"
});
```

---

## ScrambleText Effects

### Basic Scramble Reveal

```js
gsap.registerPlugin(ScrambleTextPlugin);

gsap.to(".scramble-title", {
  duration: 1.5,
  scrambleText: {
    text: "WELCOME TO THE FUTURE",
    chars: "upperCase",
    revealDelay: 0.3,
    speed: 0.3
  }
});
```

### Character Set Options

```js
// Uppercase letters
gsap.to(".text1", { scrambleText: { text: "HELLO", chars: "upperCase" } });

// Lowercase letters
gsap.to(".text2", { scrambleText: { text: "hello", chars: "lowerCase" } });

// Numbers only
gsap.to(".text3", { scrambleText: { text: "12345", chars: "0123456789" } });

// Custom characters
gsap.to(".text4", { scrambleText: { text: "HACKED", chars: "!@#$%^*()_+" } });

// Binary effect
gsap.to(".text5", { scrambleText: { text: "SYSTEM", chars: "01" } });
```

### Hover Scramble Effect

```js
const elements = document.querySelectorAll(".scramble-hover");

elements.forEach(el => {
  const originalText = el.textContent;
  
  el.addEventListener("mouseenter", () => {
    gsap.to(el, {
      duration: 0.8,
      scrambleText: {
        text: originalText,
        chars: "XO!#",
        revealDelay: 0.2,
        speed: 0.4
      }
    });
  });
});
```

### Scramble + Cursor Effect

```js
function scrambleReveal(element, text) {
  const tl = gsap.timeline();
  
  tl.to(element, {
    duration: 1.2,
    scrambleText: {
      text: text,
      chars: "upperCase",
      revealDelay: 0.4,
      speed: 0.3,
      newClass: "revealed"
    }
  })
  .to(".cursor", { autoAlpha: 0, repeat: 3, yoyo: true, duration: 0.3 }, "<");
  
  return tl;
}
```

### Sequential Scramble Lines

```js
const lines = gsap.utils.toArray(".terminal-line");

const tl = gsap.timeline();
lines.forEach((line, i) => {
  tl.to(line, {
    duration: 0.8,
    scrambleText: {
      text: line.dataset.text,
      chars: "upperCase",
      speed: 0.5
    }
  }, i * 0.3);
});
```

---

## TextPlugin Effects

### Basic Text Replacement

```js
gsap.registerPlugin(TextPlugin);

gsap.to(".message", {
  duration: 2,
  text: "Hello, World!",
  ease: "none"
});
```

### Typing with Delimiter

```js
// Type word by word
gsap.to(".sentence", {
  duration: 3,
  text: {
    value: "This is a sentence that appears word by word",
    delimiter: " "
  },
  ease: "none"
});
```

### Counter Animation

```js
gsap.to(".counter", {
  duration: 2,
  text: { value: "1000", oldClass: "old", newClass: "new" },
  ease: "power1.inOut"
});

// With formatting
function animateCounter(element, endValue) {
  const obj = { value: 0 };
  gsap.to(obj, {
    value: endValue,
    duration: 2,
    ease: "power1.out",
    onUpdate: () => {
      element.textContent = Math.round(obj.value).toLocaleString();
    }
  });
}
```

### Rotating Words (Text Swap)

```js
const words = ["Creative", "Innovative", "Dynamic", "Powerful"];
let index = 0;

function rotateWord() {
  gsap.to(".rotating-word", {
    duration: 0.5,
    text: words[index],
    ease: "power2.inOut",
    onComplete: () => {
      index = (index + 1) % words.length;
      gsap.delayedCall(2, rotateWord);
    }
  });
}
rotateWord();
```

### Erasing and Typing

```js
function typewriterLoop(element, texts) {
  let index = 0;
  
  function animate() {
    const text = texts[index];
    const tl = gsap.timeline({
      onComplete: () => {
        index = (index + 1) % texts.length;
        gsap.delayedCall(1.5, animate);
      }
    });
    
    // Type in
    tl.to(element, {
      duration: text.length * 0.05,
      text: text,
      ease: "none"
    })
    // Pause
    .to({}, { duration: 1 })
    // Erase
    .to(element, {
      duration: text.length * 0.03,
      text: "",
      ease: "none"
    });
  }
  
  animate();
}

typewriterLoop(".tagline", ["Developer", "Designer", "Creator"]);
```

---

## Scroll-Triggered Text Animations

### Characters Reveal on Scroll

```js
const split = new SplitText(".scroll-text", { type: "chars" });

gsap.from(split.chars, {
  y: 50,
  autoAlpha: 0,
  stagger: 0.02,
  scrollTrigger: {
    trigger: ".scroll-text",
    start: "top 80%",
    end: "top 30%",
    scrub: true
  }
});
```

### Per-Character Scrub (Premium Effect)

```js
const split = new SplitText(".hero-title", { type: "chars" });

split.chars.forEach((char, i) => {
  gsap.from(char, {
    autoAlpha: 0,
    scale: 0.5,
    y: 50,
    scrollTrigger: {
      trigger: ".hero",
      start: `top+=${i * 10} 80%`,
      end: `top+=${i * 10 + 100} 30%`,
      scrub: true
    }
  });
});
```

### Line-by-Line with Pin

```js
const split = new SplitText(".story-text", { type: "lines" });

const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".story-section",
    start: "top top",
    end: "+=200%",
    pin: true,
    scrub: 1
  }
});

split.lines.forEach((line, i) => {
  tl.from(line, { autoAlpha: 0, y: 30 }, i * 0.1);
});
```

### Text Color Fill on Scroll

```js
// Create overlay spans for color fill effect
const text = document.querySelector(".fill-text");
const clone = text.cloneNode(true);
clone.classList.add("fill-overlay");
text.parentNode.appendChild(clone);

// CSS: .fill-overlay { position: absolute; color: #6366f1; clip-path: inset(0 100% 0 0); }

gsap.to(".fill-overlay", {
  clipPath: "inset(0 0% 0 0)",
  scrollTrigger: {
    trigger: ".fill-text",
    start: "top 70%",
    end: "top 30%",
    scrub: true
  }
});
```

---

## Responsive Text Animations

### Handle Resize with SplitText

```js
let split;

function initSplit() {
  // Revert previous split
  if (split) split.revert();
  
  // Create new split
  split = new SplitText(".responsive-text", { type: "chars,words,lines" });
  
  // Apply animations
  gsap.from(split.chars, {
    y: 30,
    autoAlpha: 0,
    stagger: 0.02
  });
}

// Initialize
initSplit();

// Handle resize (debounced)
let resizeTimeout;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(initSplit, 250);
});
```

### React Component with SplitText

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import SplitText from "gsap/SplitText";

gsap.registerPlugin(SplitText);

export function AnimatedHeadline({ children }) {
  const textRef = useRef(null);
  const splitRef = useRef(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      splitRef.current = new SplitText(textRef.current, { type: "chars,words" });
      
      gsap.from(splitRef.current.chars, {
        y: 30,
        autoAlpha: 0,
        stagger: 0.02,
        duration: 0.6,
        ease: "power3.out"
      });
    });

    return () => {
      if (splitRef.current) splitRef.current.revert();
      ctx.revert();
    };
  }, [children]); // Re-run if text changes

  return <h1 ref={textRef}>{children}</h1>;
}
```

---

## DIY Alternatives (No Plugin)

### DIY Character Split

```js
function splitChars(element) {
  const text = element.textContent;
  element.innerHTML = "";
  element.setAttribute("aria-label", text);
  
  text.split("").forEach((char) => {
    const span = document.createElement("span");
    span.className = "char";
    span.textContent = char === " " ? "\u00A0" : char;
    span.setAttribute("aria-hidden", "true");
    element.appendChild(span);
  });
  
  return element.querySelectorAll(".char");
}

const chars = splitChars(document.querySelector(".text"));
gsap.from(chars, { y: 30, autoAlpha: 0, stagger: 0.02 });
```

### DIY Word Split

```js
function splitWords(element) {
  const text = element.textContent;
  element.innerHTML = "";
  element.setAttribute("aria-label", text);
  
  text.split(" ").forEach((word, i, arr) => {
    const span = document.createElement("span");
    span.className = "word";
    span.textContent = word;
    span.setAttribute("aria-hidden", "true");
    element.appendChild(span);
    
    if (i < arr.length - 1) {
      element.appendChild(document.createTextNode(" "));
    }
  });
  
  return element.querySelectorAll(".word");
}
```

### DIY Scramble Effect

```js
function scrambleText(element, finalText, duration = 1) {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const length = finalText.length;
  let iteration = 0;
  
  const interval = setInterval(() => {
    element.textContent = finalText
      .split("")
      .map((char, i) => {
        if (i < iteration) return finalText[i];
        return chars[Math.floor(Math.random() * chars.length)];
      })
      .join("");
    
    iteration += 1 / (duration * 30);
    
    if (iteration >= length) {
      element.textContent = finalText;
      clearInterval(interval);
    }
  }, 1000 / 30);
}

// Usage
element.addEventListener("mouseenter", () => {
  scrambleText(element, element.dataset.text);
});
```

### DIY Typewriter

```js
function typewriter(element, text, speed = 50) {
  let i = 0;
  element.textContent = "";
  
  function type() {
    if (i < text.length) {
      element.textContent += text.charAt(i);
      i++;
      setTimeout(type, speed);
    }
  }
  
  type();
}
```

---

## Performance Tips

1. **Limit split elements**: For long text, split only what's visible or in viewport
2. **Revert on cleanup**: Always call `split.revert()` when unmounting or resizing
3. **Use will-change sparingly**: Only on actively animating elements
4. **Batch DOM reads**: Cache measurements before animating
5. **Prefer transforms**: Use `y/x/scale` over `top/left/margin`
6. **Reduce stagger count**: Too many staggered elements = jank

```js
// Performance pattern: Only animate visible chars
const split = new SplitText(".long-text", { type: "chars" });

ScrollTrigger.batch(split.chars, {
  onEnter: (chars) => gsap.from(chars, { y: 20, autoAlpha: 0, stagger: 0.01 }),
  start: "top 90%"
});
```
