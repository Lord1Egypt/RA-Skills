# Next.js / React GSAP Patterns

Production-ready patterns for using GSAP in React and Next.js applications.

---

## Core Principles

1. **Always cleanup** - Prevent memory leaks and duplicate animations
2. **Scope selectors** - Use refs and context to avoid global selector conflicts
3. **SSR-safe** - Only run animations client-side
4. **Handle StrictMode** - Context + revert handles double-mount

---

## Pattern 1: Basic with gsap.context()

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";

export function AnimatedBox() {
  const container = useRef(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".box", { y: 50, autoAlpha: 0, duration: 0.8 });
    }, container);
    
    return () => ctx.revert();
  }, []);

  return (
    <div ref={container}>
      <div className="box">Content</div>
    </div>
  );
}
```

---

## Pattern 2: Official useGSAP Hook

```jsx
"use client";
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(useGSAP);

export function AnimatedSection() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from(".title", { y: 30, autoAlpha: 0 });
    gsap.from(".item", { y: 20, autoAlpha: 0, stagger: 0.1 });
  }, { scope: container });

  return (
    <div ref={container}>
      <h1 className="title">Hello</h1>
      <div className="item">A</div>
      <div className="item">B</div>
    </div>
  );
}
```

---

## Pattern 3: ScrollTrigger with Cleanup

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function ScrollSection() {
  const sectionRef = useRef(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      gsap.from(".reveal", {
        y: 50, autoAlpha: 0, duration: 0.8,
        scrollTrigger: {
          trigger: ".reveal",
          start: "top 80%",
          toggleActions: "play none none reverse"
        }
      });
    }, sectionRef);

    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef}>
      <div className="reveal">Reveal on scroll</div>
    </section>
  );
}
```

---

## Pattern 4: Responsive with matchMedia

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function ResponsiveAnimation() {
  const container = useRef(null);

  useLayoutEffect(() => {
    const mm = gsap.matchMedia();

    mm.add({
      // Desktop
      "(min-width: 768px)": () => {
        gsap.from(".hero", { x: -100, autoAlpha: 0 });
      },
      // Mobile
      "(max-width: 767px)": () => {
        gsap.from(".hero", { y: 50, autoAlpha: 0 });
      },
      // Reduced motion
      "(prefers-reduced-motion: reduce)": () => {
        gsap.set(".hero", { autoAlpha: 1 });
      }
    });

    return () => mm.revert();
  }, []);

  return (
    <div ref={container}>
      <div className="hero">Hero content</div>
    </div>
  );
}
```

---

## Pattern 5: Timeline with Labels

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";

export function SequencedAnimation() {
  const container = useRef(null);
  const tl = useRef(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      tl.current = gsap.timeline({ defaults: { ease: "power3.out", duration: 0.6 } });
      
      tl.current
        .from(".title", { y: 30, autoAlpha: 0 })
        .addLabel("titleDone")
        .from(".subtitle", { y: 20, autoAlpha: 0 }, "<0.2")
        .from(".cta", { scale: 0.9, autoAlpha: 0 }, "titleDone+=0.3");
    }, container);

    return () => ctx.revert();
  }, []);

  return (
    <div ref={container}>
      <h1 className="title">Title</h1>
      <p className="subtitle">Subtitle</p>
      <button className="cta">CTA</button>
    </div>
  );
}
```

---

## Pattern 6: Cursor Follower (Performance)

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";

export function CursorFollower() {
  const cursorRef = useRef(null);

  useLayoutEffect(() => {
    const xTo = gsap.quickTo(cursorRef.current, "x", { duration: 0.2, ease: "power3" });
    const yTo = gsap.quickTo(cursorRef.current, "y", { duration: 0.2, ease: "power3" });

    const handleMove = (e) => {
      xTo(e.clientX);
      yTo(e.clientY);
    };

    window.addEventListener("pointermove", handleMove);
    return () => window.removeEventListener("pointermove", handleMove);
  }, []);

  return <div ref={cursorRef} className="cursor" />;
}
```

---

## Pattern 7: Flip Layout Transition

```jsx
"use client";
import { useRef, useState } from "react";
import gsap from "gsap";
import Flip from "gsap/Flip";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(Flip);

export function FlipGrid() {
  const container = useRef(null);
  const [isGrid, setIsGrid] = useState(false);

  const toggleLayout = () => {
    const state = Flip.getState(".item");
    setIsGrid(!isGrid);
    
    // Use requestAnimationFrame to ensure state update is applied
    requestAnimationFrame(() => {
      Flip.from(state, { duration: 0.6, ease: "power2.inOut", stagger: 0.05 });
    });
  };

  return (
    <div ref={container}>
      <button onClick={toggleLayout}>Toggle</button>
      <div className={isGrid ? "grid" : "list"}>
        <div className="item">A</div>
        <div className="item">B</div>
        <div className="item">C</div>
      </div>
    </div>
  );
}
```

---

## Pattern 8: SplitText with Cleanup

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import SplitText from "gsap/SplitText";

gsap.registerPlugin(SplitText);

export function AnimatedHeadline() {
  const headlineRef = useRef(null);
  const splitRef = useRef(null);

  useLayoutEffect(() => {
    splitRef.current = new SplitText(headlineRef.current, { type: "chars,words" });

    const ctx = gsap.context(() => {
      gsap.from(splitRef.current.chars, {
        y: 20, autoAlpha: 0, stagger: 0.02, duration: 0.4, ease: "power3.out"
      });
    });

    return () => {
      ctx.revert();
      splitRef.current.revert();
    };
  }, []);

  return <h1 ref={headlineRef}>Animated Headline</h1>;
}
```

---

## Pattern 9: ScrollSmoother Setup

```jsx
"use client";
import { useLayoutEffect, useRef } from "react";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";
import ScrollSmoother from "gsap/ScrollSmoother";

gsap.registerPlugin(ScrollTrigger, ScrollSmoother);

export function SmoothScroller({ children }) {
  const wrapperRef = useRef(null);
  const contentRef = useRef(null);

  useLayoutEffect(() => {
    const smoother = ScrollSmoother.create({
      wrapper: wrapperRef.current,
      content: contentRef.current,
      smooth: 1.5,
      effects: true
    });

    return () => smoother.kill();
  }, []);

  return (
    <div ref={wrapperRef} id="smooth-wrapper">
      <div ref={contentRef} id="smooth-content">
        {children}
      </div>
    </div>
  );
}
```

---

## SSR Safety Rules

1. **Use `"use client"`** - Mark animation components as client-only
2. **Check window exists** - `if (typeof window !== 'undefined')`
3. **Register plugins in effect** - Or at module level in client files
4. **Don't import in server components** - GSAP needs browser APIs

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing cleanup | Use `ctx.revert()` in return |
| Selector scope | Use refs + context scope |
| SSR errors | Add `"use client"` directive |
| Double animations | Context handles StrictMode |
| Plugin not working | Register with `gsap.registerPlugin()` |