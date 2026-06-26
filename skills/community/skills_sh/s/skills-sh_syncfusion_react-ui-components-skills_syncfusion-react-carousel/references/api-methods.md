---
title: "API Methods Reference"
description: "Complete reference guide for all Syncfusion React Carousel methods with practical examples"
---

# Carousel API Methods

Complete reference for all available methods to control the Carousel component programmatically.

## Table of Contents

- [next()](#next-navigate-to-next-slide)
- [prev()](#prev-navigate-to-previous-slide)
- [play()](#play-play-slides-programmatically)
- [pause()](#pause-pause-slides-programmatically)
- [destroy()](#destroy-destroy-the-carousel-component)
- [Complete Method Example](#complete-method-example)

---

## next() - Navigate to Next Slide

Move carousel to the next slide in sequence. Respects the `loop` property when reaching the last slide.

**Signature:**
```ts
next(): void
```

**When to use:**
- Custom navigation buttons
- External controls outside carousel
- Event-driven navigation
- Programmatic slide advancement

**Example:**
```tsx
import { CarouselComponent } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

const App = () => {
  const carouselRef = React.useRef<CarouselComponent>(null);

  const handleNextClick = () => {
    carouselRef.current?.next();
  };

  return (
    <>
      <button onClick={handleNextClick}>Next Slide</button>
      <CarouselComponent ref={carouselRef}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </>
  );
};

export default App;
```

**With loop enabled (default):**
```tsx
// Last slide + next() → First slide
<CarouselComponent ref={carouselRef} loop={true}>
  {/* next() on slide 3 goes to slide 1 */}
</CarouselComponent>
```

**With loop disabled:**
```tsx
// Last slide + next() → No change (stays on last slide)
<CarouselComponent ref={carouselRef} loop={false}>
  {/* next() on slide 3 has no effect */}
</CarouselComponent>
```

**Advanced example - Skip to specific slide:**
```tsx
const goToSlide = (slideIndex: number) => {
  const carouselComponent = carouselRef.current;
  const currentIndex = carouselComponent?.selectedIndex || 0;
  
  if (slideIndex > currentIndex) {
    // Advance multiple slides
    for (let i = currentIndex; i < slideIndex; i++) {
      carouselComponent?.next();
    }
  }
};
```

---

## prev() - Navigate to Previous Slide

Move carousel to the previous slide in sequence. Respects the `loop` property when reaching the first slide.

**Signature:**
```ts
prev(): void
```

**When to use:**
- Custom back/previous buttons
- External controls outside carousel
- Event-driven backwards navigation
- Undo slide advancement

**Example:**
```tsx
import { CarouselComponent } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

const App = () => {
  const carouselRef = React.useRef<CarouselComponent>(null);

  const handlePrevClick = () => {
    carouselRef.current?.prev();
  };

  return (
    <>
      <button onClick={handlePrevClick}>Previous Slide</button>
      <CarouselComponent ref={carouselRef}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </>
  );
};

export default App;
```

**With loop enabled (default):**
```tsx
// First slide + prev() → Last slide
<CarouselComponent ref={carouselRef} loop={true}>
  {/* prev() on slide 1 goes to slide 3 */}
</CarouselComponent>
```

**With loop disabled:**
```tsx
// First slide + prev() → No change (stays on first slide)
<CarouselComponent ref={carouselRef} loop={false}>
  {/* prev() on slide 1 has no effect */}
</CarouselComponent>
```

**Advanced example - Go back multiple slides:**
```tsx
const goBackSlides = (count: number) => {
  const carouselComponent = carouselRef.current;
  
  for (let i = 0; i < count; i++) {
    carouselComponent?.prev();
  }
};

// Usage
<button onClick={() => goBackSlides(3)}>Back 3 Slides</button>
```

---

## play() - Play Slides Programmatically

Resume automatic slide transitions if they are paused. Starts the carousel auto-play functionality.

**Signature:**
```ts
play(): void
```

**When to use:**
- Resume auto-play after pause
- Start slideshow programmatically
- Control auto-play with custom buttons
- Resume carousel in event handlers

**Example:**
```tsx
import { CarouselComponent } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

const App = () => {
  const carouselRef = React.useRef<CarouselComponent>(null);

  const handlePlay = () => {
    carouselRef.current?.play();
  };

  return (
    <>
      <button onClick={handlePlay}>Play Slideshow</button>
      <CarouselComponent ref={carouselRef} autoPlay={false}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </>
  );
};

export default App;
```

**Example - Auto-start with delay:**
```tsx
React.useEffect(() => {
  const timer = setTimeout(() => {
    carouselRef.current?.play();
  }, 2000); // Start after 2 seconds
  
  return () => clearTimeout(timer);
}, []);
```

---

## pause() - Pause Slides Programmatically

Pause automatic slide transitions. Stops the carousel auto-play functionality without destroying the component.

**Signature:**
```ts
pause(): void
```

**When to use:**
- Pause on user interaction
- Pause during loading
- Stop auto-play for user interaction
- Control auto-play with custom buttons

**Example:**
```tsx
import { CarouselComponent } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

const App = () => {
  const carouselRef = React.useRef<CarouselComponent>(null);

  const handlePause = () => {
    carouselRef.current?.pause();
  };

  return (
    <>
      <button onClick={handlePause}>Pause Slideshow</button>
      <CarouselComponent ref={carouselRef} autoPlay={true}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </>
  );
};

export default App;
```

**Example - Pause on hover (with custom logic):**
```tsx
const handleMouseEnter = () => {
  carouselRef.current?.pause();
};

const handleMouseLeave = () => {
  carouselRef.current?.play();
};

<div onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
  <CarouselComponent ref={carouselRef} autoPlay={true}>
    {/* items */}
  </CarouselComponent>
</div>
```

---

## destroy() - Destroy the Carousel Component

Cleanup and destroy the carousel component instance. Removes all event listeners and DOM elements associated with the carousel.

**Signature:**
```ts
destroy(): void
```

**When to use:**
- Component unmounting
- Cleanup in useEffect return
- Memory management
- Removing carousel from DOM

**Example:**
```tsx
import { CarouselComponent } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

const App = () => {
  const carouselRef = React.useRef<CarouselComponent>(null);

  React.useEffect(() => {
    return () => {
      // Cleanup on unmount
      carouselRef.current?.destroy();
    };
  }, []);

  return (
    <CarouselComponent ref={carouselRef}>
      <CarouselItemsDirective>
        <CarouselItemDirective template='<h3>Slide 1</h3>' />
        <CarouselItemDirective template='<h3>Slide 2</h3>' />
        <CarouselItemDirective template='<h3>Slide 3</h3>' />
      </CarouselItemsDirective>
    </CarouselComponent>
  );
};

export default App;
```

**Example - Destroy on specific event:**
```tsx
const handleDestroy = () => {
  carouselRef.current?.destroy();
  console.log('Carousel destroyed');
};

<button onClick={handleDestroy}>Destroy Carousel</button>
```

**Example - Conditional destroy:**
```tsx
React.useEffect(() => {
  return () => {
    if (carouselRef.current) {
      carouselRef.current.destroy();
    }
  };
}, []);
```

---

## Complete Method Example

Full working example demonstrating all five methods together:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';
import './carousel-methods.css';

const CarouselMethodsDemo = () => {
  const carouselRef = React.useRef<CarouselComponent>(null);
  const [isPlaying, setIsPlaying] = React.useState(true);
  const [slideIndex, setSlideIndex] = React.useState(0);

  // Navigate to next slide
  const handleNext = () => {
    carouselRef.current?.next();
  };

  // Navigate to previous slide
  const handlePrev = () => {
    carouselRef.current?.prev();
  };

  // Play slides programmatically
  const handlePlay = () => {
    carouselRef.current?.play();
    setIsPlaying(true);
  };

  // Pause slides programmatically
  const handlePause = () => {
    carouselRef.current?.pause();
    setIsPlaying(false);
  };

  // Destroy carousel
  const handleDestroy = () => {
    carouselRef.current?.destroy();
    alert('Carousel destroyed');
  };

  // Jump to specific slide
  const goToSlide = (index: number) => {
    const current = slideIndex;
    if (index > current) {
      for (let i = 0; i < index - current; i++) {
        carouselRef.current?.next();
      }
    } else if (index < current) {
      for (let i = 0; i < current - index; i++) {
        carouselRef.current?.prev();
      }
    }
  };

  // Handle slide change
  const onSlideChanged = (args: any) => {
    setSlideIndex(args.currentIndex);
  };

  return (
    <div className="carousel-demo">
      <div className="controls">
        {/* Navigation Controls */}
        <button onClick={handlePrev} className="btn btn-prev">
          ← Prev
        </button>
        
        <button onClick={handleNext} className="btn btn-next">
          Next →
        </button>

        <div className="spacer"></div>

        {/* Play/Pause Controls */}
        <button 
          onClick={isPlaying ? handlePause : handlePlay} 
          className={`btn ${isPlaying ? 'btn-pause' : 'btn-play'}`}
        >
          {isPlaying ? '⏸ Pause' : '▶ Play'}
        </button>

        <div className="spacer"></div>

        {/* Slide Selectors */}
        <button onClick={() => goToSlide(0)} className="btn btn-slide">
          Slide 1
        </button>
        <button onClick={() => goToSlide(1)} className="btn btn-slide">
          Slide 2
        </button>
        <button onClick={() => goToSlide(2)} className="btn btn-slide">
          Slide 3
        </button>
        <button onClick={() => goToSlide(3)} className="btn btn-slide">
          Slide 4
        </button>
        <button onClick={() => goToSlide(4)} className="btn btn-slide">
          Slide 5
        </button>

        <div className="spacer"></div>

        {/* Destroy Button */}
        <button onClick={handleDestroy} className="btn btn-destroy">
          Destroy
        </button>
      </div>

      <div className="carousel-container">
        <CarouselComponent 
          ref={carouselRef} 
          loop={true}
          autoPlay={true}
          slideChanged={onSlideChanged}
        >
          <CarouselItemsDirective>
            <CarouselItemDirective template='<div class="slide slide-1"><h3>Slide 1</h3></div>' />
            <CarouselItemDirective template='<div class="slide slide-2"><h3>Slide 2</h3></div>' />
            <CarouselItemDirective template='<div class="slide slide-3"><h3>Slide 3</h3></div>' />
            <CarouselItemDirective template='<div class="slide slide-4"><h3>Slide 4</h3></div>' />
            <CarouselItemDirective template='<div class="slide slide-5"><h3>Slide 5</h3></div>' />
          </CarouselItemsDirective>
        </CarouselComponent>
      </div>

      <div className="info-panel">
        <h4>Carousel Status:</h4>
        <p>Current Slide: <strong>{slideIndex + 1}</strong> / 5</p>
        <p>Auto-Play: <strong>{isPlaying ? '🟢 Playing' : '⏸ Paused'}</strong></p>
        <p className="methods-info">
          Available Methods: next() | prev() | play() | pause() | destroy()
        </p>
      </div>
    </div>
  );
};

export default CarouselMethodsDemo;
```

**CSS styling (carousel-methods.css):**
```css
.carousel-demo {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.spacer {
  flex: 1;
}

.btn {
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  background: white;
  transition: all 0.3s ease;
}

.btn:hover {
  background: #f0f0f0;
  border-color: #999;
}

.btn-prev, .btn-next {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.btn-prev:hover, .btn-next:hover {
  background: #0056b3;
  border-color: #0056b3;
}

.btn-slide {
  background: #28a745;
  color: white;
  border-color: #28a745;
  min-width: 80px;
}

.btn-slide:hover {
  background: #218838;
  border-color: #218838;
}

.btn-play, .btn-pause {
  background: #ff9800;
  color: white;
  border-color: #ff9800;
}

.btn-play:hover, .btn-pause:hover {
  background: #f57c00;
  border-color: #f57c00;
}

.btn-destroy {
  background: #dc3545;
  color: white;
  border-color: #dc3545;
}

.btn-destroy:hover {
  background: #c82333;
  border-color: #c82333;
}

.carousel-container {
  margin: 30px 0;
  border: 2px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.slide {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  font-size: 24px;
  font-weight: bold;
  color: white;
}

.slide-1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.slide-2 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.slide-3 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.slide-4 { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.slide-5 { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }

.info-panel {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  margin-top: 20px;
}

.info-panel h4 {
  margin-top: 0;
  color: #333;
}

.info-panel p {
  margin: 8px 0;
  color: #666;
}

.info-panel strong {
  color: #007bff;
}

.methods-info {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #ddd;
  font-size: 12px;
  color: #999;
  font-weight: bold;
}
```

---

## Method Usage Patterns

### Pattern 1: Navigate and Control Play/Pause
```tsx
const [isPlaying, setIsPlaying] = React.useState(true);

const togglePlayPause = () => {
  if (isPlaying) {
    carouselRef.current?.pause();
  } else {
    carouselRef.current?.play();
  }
  setIsPlaying(!isPlaying);
};

<>
  <button onClick={() => carouselRef.current?.prev()}>Prev</button>
  <button onClick={togglePlayPause}>{isPlaying ? 'Pause' : 'Play'}</button>
  <button onClick={() => carouselRef.current?.next()}>Next</button>
</>
```

### Pattern 2: Go to Specific Slide
```tsx
const goToSlide = (targetIndex: number) => {
  const current = carouselRef.current?.selectedIndex || 0;
  const diff = targetIndex - current;
  
  if (diff > 0) {
    for (let i = 0; i < diff; i++) carouselRef.current?.next();
  } else if (diff < 0) {
    for (let i = 0; i < Math.abs(diff); i++) carouselRef.current?.prev();
  }
};

<button onClick={() => goToSlide(2)}>Go to Slide 3</button>
```

### Pattern 3: Pause on Hover, Play on Leave
```tsx
<div 
  onMouseEnter={() => carouselRef.current?.pause()}
  onMouseLeave={() => carouselRef.current?.play()}
>
  <CarouselComponent ref={carouselRef} autoPlay={true}>
    {/* items */}
  </CarouselComponent>
</div>
```

### Pattern 4: Keyboard Shortcuts
```tsx
React.useEffect(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'ArrowRight') carouselRef.current?.next();
    if (e.key === 'ArrowLeft') carouselRef.current?.prev();
    if (e.key === ' ') {
      e.preventDefault();
      // Toggle play/pause on spacebar
      isPlaying ? carouselRef.current?.pause() : carouselRef.current?.play();
    }
  };
  
  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, [isPlaying]);
```

### Pattern 5: Auto-Pause During Interaction
```tsx
const [pausedByUser, setPausedByUser] = React.useState(false);

const handleUserInteraction = () => {
  carouselRef.current?.pause();
  setPausedByUser(true);
  
  // Resume after 5 seconds
  setTimeout(() => {
    carouselRef.current?.play();
    setPausedByUser(false);
  }, 5000);
};
```

### Pattern 6: Cleanup on Unmount
```tsx
React.useEffect(() => {
  return () => {
    // Cleanup: Pause and destroy on component unmount
    carouselRef.current?.pause();
    carouselRef.current?.destroy();
  };
}, []);
```
