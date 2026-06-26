# GSAP Physics Plugins Reference

Physics-based animations with Physics2D and PhysicsProps plugins for realistic motion effects.

---

## Physics2D Plugin

Animate x/y coordinates based on velocity, angle, gravity, acceleration, and friction.

### Installation

```js
import { gsap } from "gsap";
import { Physics2DPlugin } from "gsap/Physics2DPlugin";
gsap.registerPlugin(Physics2DPlugin);
```

### Basic Usage

```js
// Ballistic throw with gravity
gsap.to(".ball", {
  duration: 2,
  physics2D: {
    velocity: 300,      // pixels per second
    angle: -60,         // degrees (upward-right)
    gravity: 400        // downward acceleration
  }
});
```

### Config Options

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `velocity` | Number | 0 | Initial velocity in pixels/second |
| `angle` | Number | 0 | Direction in degrees (0 = right, -90 = up, 90 = down) |
| `gravity` | Number | null | Downward acceleration (shortcut for acceleration at 90°) |
| `acceleration` | Number | null | Acceleration in pixels/second |
| `accelerationAngle` | Number | null | Direction of acceleration in degrees |
| `friction` | Number | 0 | 0-1 range. 0 = no friction, 1 = full stop |
| `xProp` | String | "x" | Property name for x-axis (e.g., "left") |
| `yProp` | String | "y" | Property name for y-axis (e.g., "top") |

### Examples

#### Gravity Fall

```js
gsap.to(".falling", {
  duration: 3,
  physics2D: {
    velocity: 0,
    angle: -90,
    gravity: 500
  }
});
```

#### Throw with Arc

```js
gsap.to(".projectile", {
  duration: 2.5,
  physics2D: {
    velocity: 400,
    angle: -45,        // 45 degrees upward
    gravity: 300
  }
});
```

#### Friction-Based Movement

```js
gsap.to(".sliding", {
  duration: 4,
  physics2D: {
    velocity: 500,
    angle: 0,          // straight right
    friction: 0.05     // gradual slowdown
  }
});
```

#### Custom Acceleration

```js
gsap.to(".rocket", {
  duration: 3,
  physics2D: {
    velocity: 100,
    angle: -90,                // upward
    acceleration: 200,
    accelerationAngle: -90     // accelerate upward
  }
});
```

#### Particle Explosion

```js
function explode(container, particleCount = 20) {
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";
    container.appendChild(particle);
    
    gsap.to(particle, {
      duration: gsap.utils.random(1, 2),
      physics2D: {
        velocity: gsap.utils.random(200, 500),
        angle: gsap.utils.random(-180, 180),
        gravity: 400
      },
      autoAlpha: 0,
      onComplete: () => particle.remove()
    });
  }
}
```

---

## PhysicsProps Plugin

Apply physics-based motion to ANY numeric property.

### Installation

```js
import { gsap } from "gsap";
import { PhysicsPropsPlugin } from "gsap/PhysicsPropsPlugin";
gsap.registerPlugin(PhysicsPropsPlugin);
```

### Basic Usage

```js
gsap.to(".element", {
  duration: 3,
  physicsProps: {
    x: { velocity: 200, friction: 0.05 },
    rotation: { velocity: 360 }
  }
});
```

### Config Options (per property)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `velocity` | Number | 0 | Initial velocity in units/second |
| `acceleration` | Number | 0 | Units/second acceleration |
| `friction` | Number | 0 | 0-1 range, slows movement over time |

### Examples

#### Spinning with Friction

```js
gsap.to(".wheel", {
  duration: 5,
  physicsProps: {
    rotation: {
      velocity: 720,    // 2 full rotations per second
      friction: 0.03    // slow to stop
    }
  }
});
```

#### Multi-Property Physics

```js
gsap.to(".bouncing", {
  duration: 4,
  physicsProps: {
    x: { velocity: 300, friction: 0.02 },
    y: { velocity: -200, acceleration: 500 },  // gravity effect
    rotation: { velocity: 180 }
  }
});
```

#### Scale with Physics

```js
gsap.to(".pulsing", {
  duration: 2,
  physicsProps: {
    scale: {
      velocity: 0.5,
      acceleration: -0.3,  // decelerate
      friction: 0.1
    }
  }
});
```

---

## Key Differences

| Feature | Physics2D | PhysicsProps |
|---------|-----------|--------------|
| **Properties** | x/y only | Any numeric property |
| **Angle** | Yes (direction) | No (per-property) |
| **Gravity** | Yes (built-in) | No (use acceleration) |
| **Use Case** | 2D projectile motion | General physics effects |

---

## Tips & Best Practices

### 1. Easing is Ignored

Physics plugins control motion mathematically. Any `ease` property is ignored:

```js
// ❌ ease has no effect
gsap.to(".ball", {
  duration: 2,
  ease: "power2.out",  // Ignored!
  physics2D: { velocity: 300, gravity: 400 }
});
```

### 2. Timelines Work

Add physics tweens to timelines for complex sequences:

```js
const tl = gsap.timeline();

tl.to(".ball", {
  duration: 2,
  physics2D: { velocity: 400, angle: -45, gravity: 300 }
})
.to(".ball", {
  y: "+=50",
  duration: 0.5,
  ease: "bounce.out"
});
```

### 3. Reversible

Physics tweens can be reversed:

```js
const tl = gsap.timeline();
tl.to(".particles", {
  duration: 2,
  physics2D: { velocity: 300, angle: -60, gravity: 400 }
});

// Particles retrace their path!
tl.reverse();
```

### 4. Reduced Motion Fallback

```js
gsap.matchMedia().add({
  "(prefers-reduced-motion: no-preference)": () => {
    gsap.to(".ball", {
      duration: 2,
      physics2D: { velocity: 300, gravity: 400 }
    });
  },
  "(prefers-reduced-motion: reduce)": () => {
    // Simple fade instead of physics
    gsap.to(".ball", { autoAlpha: 0, duration: 0.5 });
  }
});
```

---

## Common Patterns

### Confetti

```js
function confetti(count = 50) {
  const colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24"];
  
  for (let i = 0; i < count; i++) {
    const el = document.createElement("div");
    el.className = "confetti-piece";
    el.style.background = colors[i % colors.length];
    document.body.appendChild(el);
    
    gsap.set(el, { x: window.innerWidth / 2, y: window.innerHeight });
    
    gsap.to(el, {
      duration: gsap.utils.random(2, 4),
      physics2D: {
        velocity: gsap.utils.random(300, 600),
        angle: gsap.utils.random(-120, -60),
        gravity: gsap.utils.random(200, 400)
      },
      rotation: gsap.utils.random(-360, 360),
      autoAlpha: 0,
      onComplete: () => el.remove()
    });
  }
}
```

### Slot Machine Spin

```js
function spinSlot(element) {
  gsap.to(element, {
    duration: 3,
    physicsProps: {
      y: {
        velocity: 2000,    // Fast initial spin
        friction: 0.02     // Gradually slow
      }
    },
    modifiers: {
      y: gsap.utils.unitize(y => gsap.utils.wrap(0, 300, parseFloat(y)))
    }
  });
}
```

### Drift Effect

```js
// Mouse-influenced drift
let velocityX = 0;
let velocityY = 0;

window.addEventListener("mousemove", (e) => {
  velocityX = (e.clientX - window.innerWidth / 2) * 0.5;
  velocityY = (e.clientY - window.innerHeight / 2) * 0.5;
});

gsap.to(".drifter", {
  duration: 2,
  repeat: -1,
  physicsProps: {
    x: { velocity: () => velocityX, friction: 0.1 },
    y: { velocity: () => velocityY, friction: 0.1 }
  }
});
```
