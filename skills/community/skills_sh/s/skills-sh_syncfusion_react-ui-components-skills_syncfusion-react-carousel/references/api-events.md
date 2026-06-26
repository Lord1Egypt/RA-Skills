---
title: "API Events Reference"
description: "Complete reference guide for Syncfusion React Carousel events with detailed examples"
---

# Carousel API Events

Complete reference for carousel events that fire during slide transitions and user interactions.

## Table of Contents

- [slideChanging](#slidechanging-event)
- [slideChanged](#slidechanged-event)
- [Event Arguments](#event-arguments)
- [Complete Event Example](#complete-event-example)
- [Common Event Patterns](#common-event-patterns)

---

## slideChanging Event

Fires **BEFORE** a slide transition occurs. This event is **cancelable** - you can prevent the transition by setting `args.cancel = true`.

**Use Cases:**
- Validate before allowing slide change
- Show confirmation dialogs
- Prevent certain slides from being accessed
- Log slide change attempts
- Disable transitions during animations

**Event Signature:**
```ts
slideChanging?(args: SlideChangingEventArgs): void
```

**Event Arguments (SlideChangingEventArgs):**

| Property | Type | Description |
|----------|------|-------------|
| **cancel** | `boolean` | Set to `true` to prevent the transition (cancelable) |
| **currentIndex** | `number` | Index of the currently displayed slide |
| **currentSlide** | `HTMLElement` | HTML element of the current slide |
| **nextIndex** | `number` | Index of the slide about to be displayed |
| **nextSlide** | `HTMLElement` | HTML element of the next slide |
| **isSwiped** | `boolean` | `true` if transition triggered by swipe gesture, `false` if button/keyboard |
| **name** | `string` | Event name: `'slideChanging'` |
| **slideDirection** | `CarouselSlideDirection` | Direction of transition: `'Previous'` or `'Next'` |

**Basic Example:**
```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective,
         SlideChangingEventArgs } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

const App = () => {
  const onSlideChanging = (args: SlideChangingEventArgs): void => {
    console.log(`About to change from slide ${args.currentIndex} to ${args.nextIndex}`);
    console.log(`Direction: ${args.slideDirection}`);
    console.log(`From swipe: ${args.isSwiped}`);
  };

  return (
    <CarouselComponent slideChanging={onSlideChanging}>
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

**Example - Prevent transition to specific slide:**
```tsx
const onSlideChanging = (args: SlideChangingEventArgs): void => {
  // Don't allow transition to slide 3 (index 2)
  if (args.nextIndex === 2) {
    args.cancel = true;
    alert('This slide is currently disabled');
  }
};
```

**Example - Confirm before advancing:**
```tsx
const onSlideChanging = (args: SlideChangingEventArgs): void => {
  // Only when swiping, not button clicks
  if (args.isSwiped && args.slideDirection === 'Next') {
    const confirmed = window.confirm(
      `Move from slide ${args.currentIndex + 1} to ${args.nextIndex + 1}?`
    );
    if (!confirmed) {
      args.cancel = true;
    }
  }
};
```

**Example - Disable swipe but allow buttons:**
```tsx
const onSlideChanging = (args: SlideChangingEventArgs): void => {
  // Prevent swipe navigation only
  if (args.isSwiped) {
    args.cancel = true;
  }
};
```

**Example - Rate limiting transitions:**
```tsx
const [isTransitioning, setIsTransitioning] = React.useState(false);

const onSlideChanging = (args: SlideChangingEventArgs): void => {
  if (isTransitioning) {
    args.cancel = true;  // Prevent rapid transitions
    return;
  }
  
  setIsTransitioning(true);
  
  // Allow transition to complete
  setTimeout(() => {
    setIsTransitioning(false);
  }, 500);
};
```

---

## slideChanged Event

Fires **AFTER** a slide transition is complete. This event is **not cancelable** - the slide has already changed.

**Use Cases:**
- Track slide view analytics
- Update external UI elements (page counter, indicators)
- Load additional content for the slide
- Trigger animations or effects
- Update page title/URL
- Auto-play related content

**Event Signature:**
```ts
slideChanged?(args: SlideChangedEventArgs): void
```

**Event Arguments (SlideChangedEventArgs):**

| Property | Type | Description |
|----------|------|-------------|
| **currentIndex** | `number` | Index of the newly displayed slide |
| **currentSlide** | `HTMLElement` | HTML element of the currently displayed slide |
| **previousIndex** | `number` | Index of the slide that was just left |
| **previousSlide** | `HTMLElement` | HTML element of the previous slide |
| **isSwiped** | `boolean` | `true` if transition was a swipe gesture, `false` if button/keyboard |
| **name** | `string` | Event name: `'slideChanged'` |
| **slideDirection** | `CarouselSlideDirection` | Direction of transition: `'Previous'` or `'Next'` |

**Basic Example:**
```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective,
         SlideChangedEventArgs } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

const App = () => {
  const onSlideChanged = (args: SlideChangedEventArgs): void => {
    console.log(`Now viewing slide ${args.currentIndex}`);
    console.log(`Previous was slide ${args.previousIndex}`);
    console.log(`Navigation type: ${args.isSwiped ? 'Swipe' : 'Button/Keyboard'}`);
  };

  return (
    <CarouselComponent slideChanged={onSlideChanged}>
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

**Example - Update slide counter:**
```tsx
const [slideCount, setSlideCount] = React.useState('1/3');

const onSlideChanged = (args: SlideChangedEventArgs): void => {
  const totalSlides = 3; // or get from carousel
  setSlideCount(`${args.currentIndex + 1}/${totalSlides}`);
};

return (
  <>
    <div className="slide-counter">{slideCount}</div>
    <CarouselComponent slideChanged={onSlideChanged}>
      {/* items */}
    </CarouselComponent>
  </>
);
```

**Example - Track analytics:**
```tsx
const onSlideChanged = (args: SlideChangedEventArgs): void => {
  // Log to analytics service
  trackEvent('carousel_slide_viewed', {
    slideIndex: args.currentIndex,
    previousIndex: args.previousIndex,
    direction: args.slideDirection,
    interactionType: args.isSwiped ? 'swipe' : 'button'
  });
};
```

**Example - Load additional content for slide:**
```tsx
const onSlideChanged = (args: SlideChangedEventArgs): void => {
  // Preload content for next slide
  const nextIndex = (args.currentIndex + 1) % 3;
  loadSlideContent(nextIndex);
  
  // Lazy load images in current slide
  const images = args.currentSlide.querySelectorAll('img[data-src]');
  images.forEach(img => {
    img.src = img.getAttribute('data-src');
  });
};
```

**Example - Trigger animations:**
```tsx
const onSlideChanged = (args: SlideChangedEventArgs): void => {
  // Add animation class to current slide
  args.currentSlide.classList.add('fade-in-animation');
  
  // Remove animation from previous slide
  args.previousSlide.classList.remove('fade-in-animation');
  args.previousSlide.classList.add('fade-out-animation');
};
```

---

## Event Arguments

### SlideChangingEventArgs

Structure for `slideChanging` event:

```ts
interface SlideChangingEventArgs {
  cancel: boolean;                        // Set true to prevent transition
  currentIndex: number;                   // Currently displayed slide index
  currentSlide: HTMLElement;              // Current slide element
  nextIndex: number;                      // Next slide index (about to display)
  nextSlide: HTMLElement;                 // Next slide element
  isSwiped: boolean;                      // true = swipe, false = button/keyboard
  name: string;                           // 'slideChanging'
  slideDirection: CarouselSlideDirection; // 'Previous' or 'Next'
}
```

### SlideChangedEventArgs

Structure for `slideChanged` event:

```ts
interface SlideChangedEventArgs {
  currentIndex: number;                   // New slide index (now displayed)
  currentSlide: HTMLElement;              // Current slide element
  previousIndex: number;                  // Previous slide index (just left)
  previousSlide: HTMLElement;             // Previous slide element
  isSwiped: boolean;                      // true = swipe, false = button/keyboard
  name: string;                           // 'slideChanged'
  slideDirection: CarouselSlideDirection; // 'Previous' or 'Next'
}
```

### CarouselSlideDirection

Enum for slide transition direction:

```ts
type CarouselSlideDirection = 'Previous' | 'Next';
```

---

## Complete Event Example

Full working example demonstrating both events:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective,
         SlideChangingEventArgs, SlideChangedEventArgs } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';
import './carousel-events.css';

interface SlideHistory {
  timestamp: string;
  from: number;
  to: number;
  direction: string;
  type: string;
}

const CarouselEventsDemo = () => {
  const carouselRef = React.useRef<CarouselComponent>(null);
  const [currentSlide, setCurrentSlide] = React.useState(1);
  const [totalSlides] = React.useState(5);
  const [history, setHistory] = React.useState<SlideHistory[]>([]);
  const [status, setStatus] = React.useState('Ready');
  const [allowTransition, setAllowTransition] = React.useState(true);

  const onSlideChanging = (args: SlideChangingEventArgs): void => {
    const timestamp = new Date().toLocaleTimeString();
    
    // Example 1: Rate limiting - prevent rapid transitions
    if (!allowTransition) {
      args.cancel = true;
      setStatus('⏱️ Please wait for transition to complete');
      return;
    }

    // Example 2: Prevent specific slides
    if (args.nextIndex === 4) {
      args.cancel = true;
      setStatus('❌ Slide 5 is currently disabled');
      return;
    }

    setStatus(`🔄 Changing from slide ${args.currentIndex + 1} to ${args.nextIndex + 1}...`);
    
    // Disable transitions during animation
    setAllowTransition(false);
  };

  const onSlideChanged = (args: SlideChangedEventArgs): void => {
    const timestamp = new Date().toLocaleTimeString();
    
    // Update slide counter
    setCurrentSlide(args.currentIndex + 1);
    
    // Update status
    const navType = args.isSwiped ? 'Swipe' : args.slideDirection === 'Next' ? 'Next Button' : 'Prev Button';
    setStatus(`✅ Now viewing slide ${args.currentIndex + 1} (${navType})`);
    
    // Add to history
    const newEntry: SlideHistory = {
      timestamp,
      from: args.previousIndex,
      to: args.currentIndex,
      direction: args.slideDirection,
      type: args.isSwiped ? 'Swipe' : 'Button'
    };
    setHistory(prev => [newEntry, ...prev.slice(0, 9)]);
    
    // Re-enable transitions
    setTimeout(() => {
      setAllowTransition(true);
    }, 500);
  };

  return (
    <div className="carousel-events-demo">
      <div className="header">
        <h2>Carousel Events Demo</h2>
        <p className="status">{status}</p>
      </div>

      <div className="carousel-section">
        <CarouselComponent 
          ref={carouselRef}
          loop={true}
          showIndicators={true}
          buttonsVisibility="Visible"
          slideChanging={onSlideChanging}
          slideChanged={onSlideChanged}
        >
          <CarouselItemsDirective>
            <CarouselItemDirective template='<div class="slide slide-1"><h3>Slide 1</h3><p>Navigate forward</p></div>' />
            <CarouselItemDirective template='<div class="slide slide-2"><h3>Slide 2</h3><p>Go to next</p></div>' />
            <CarouselItemDirective template='<div class="slide slide-3"><h3>Slide 3</h3><p>Continue</p></div>' />
            <CarouselItemDirective template='<div class="slide slide-4"><h3>Slide 4</h3><p>Almost there</p></div>' />
            <CarouselItemDirective template='<div class="slide slide-5"><h3>Slide 5</h3><p>This slide is disabled</p></div>' />
          </CarouselItemsDirective>
        </CarouselComponent>
      </div>

      <div className="info-panel">
        <div className="slide-counter">
          <h3>Current Position</h3>
          <p className="counter">{currentSlide} / {totalSlides}</p>
        </div>

        <div className="history-panel">
          <h3>Navigation History (Last 10)</h3>
          <div className="history-list">
            {history.length === 0 ? (
              <p className="no-history">No navigation yet</p>
            ) : (
              <table className="history-table">
                <thead>
                  <tr>
                    <th>Time</th>
                    <th>From</th>
                    <th>To</th>
                    <th>Direction</th>
                    <th>Type</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((entry, idx) => (
                    <tr key={idx}>
                      <td>{entry.timestamp}</td>
                      <td>{entry.from + 1}</td>
                      <td>{entry.to + 1}</td>
                      <td>{entry.direction}</td>
                      <td><span className={`type-badge ${entry.type.toLowerCase()}`}>{entry.type}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>

      <div className="notes">
        <h4>Event Demo Features:</h4>
        <ul>
          <li><strong>slideChanging event:</strong> Fires before transition - can cancel slide 5</li>
          <li><strong>slideChanged event:</strong> Fires after transition - updates history</li>
          <li><strong>Rate limiting:</strong> Waits 500ms between transitions</li>
          <li><strong>Navigation tracking:</strong> Records swipes vs button clicks</li>
          <li><strong>History logging:</strong> Shows last 10 navigation events</li>
        </ul>
      </div>
    </div>
  );
};

export default CarouselEventsDemo;
```

**CSS (carousel-events.css):**
```css
.carousel-events-demo {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h2 {
  margin: 0 0 10px 0;
  color: #333;
}

.status {
  font-size: 16px;
  color: #666;
  padding: 10px;
  background: #f0f0f0;
  border-radius: 4px;
  min-height: 20px;
}

.carousel-section {
  margin: 30px 0;
  border: 2px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.slide {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: white;
  font-size: 20px;
  text-align: center;
}

.slide-1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.slide-2 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.slide-3 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.slide-4 { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
.slide-5 { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }

.slide h3 {
  margin: 0 0 10px 0;
  font-size: 32px;
}

.slide p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.info-panel {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 20px;
  margin-top: 30px;
}

.slide-counter {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 20px;
  text-align: center;
}

.slide-counter h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 14px;
}

.counter {
  font-size: 48px;
  font-weight: bold;
  color: #007bff;
  margin: 0;
}

.history-panel {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 20px;
}

.history-panel h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 14px;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.history-table thead {
  background: #f0f0f0;
  border-bottom: 2px solid #ddd;
}

.history-table th {
  padding: 10px;
  text-align: left;
  font-weight: bold;
  color: #333;
}

.history-table td {
  padding: 8px 10px;
  border-bottom: 1px solid #eee;
}

.history-table tr:hover {
  background: #fff;
}

.type-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: bold;
}

.type-badge.button {
  background: #007bff;
  color: white;
}

.type-badge.swipe {
  background: #28a745;
  color: white;
}

.no-history {
  color: #999;
  text-align: center;
  padding: 20px;
}

.notes {
  background: #fffacd;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 20px;
  margin-top: 30px;
}

.notes h4 {
  margin: 0 0 15px 0;
  color: #333;
}

.notes ul {
  margin: 0;
  padding-left: 20px;
}

.notes li {
  margin: 8px 0;
  color: #666;
}

@media (max-width: 768px) {
  .info-panel {
    grid-template-columns: 1fr;
  }
  
  .history-table {
    font-size: 11px;
  }
  
  .history-table th,
  .history-table td {
    padding: 6px 8px;
  }
}
```

---

## Common Event Patterns

### Pattern 1: Validation Before Slide Change
```tsx
const onSlideChanging = (args: SlideChangingEventArgs): void => {
  // Example: Don't allow going back from slide 3
  if (args.slideDirection === 'Previous' && args.currentIndex === 2) {
    args.cancel = true;
    alert('Cannot go back from this slide');
  }
};
```

### Pattern 2: Loading State Management
```tsx
const [isLoading, setIsLoading] = React.useState(false);

const onSlideChanging = (args: SlideChangingEventArgs): void => {
  setIsLoading(true);
};

const onSlideChanged = (args: SlideChangedEventArgs): void => {
  setIsLoading(false);
};
```

### Pattern 3: Analytics Tracking
```tsx
const onSlideChanged = (args: SlideChangedEventArgs): void => {
  // Track slide views
  gtag.event('slide_view', {
    slide_number: args.currentIndex + 1,
    total_slides: 5,
    navigation_method: args.isSwiped ? 'swipe' : 'button',
    direction: args.slideDirection
  });
};
```

### Pattern 4: Content Preloading
```tsx
const onSlideChanged = (args: SlideChangedEventArgs): void => {
  // Preload images for next slide
  const nextIndex = (args.currentIndex + 1) % totalSlides;
  const nextSlideImages = document.querySelectorAll(
    `.carousel-item:nth-child(${nextIndex + 1}) img`
  );
  nextSlideImages.forEach(img => {
    new Image().src = img.src; // Preload
  });
};
```

### Pattern 5: Disabling Swipe Only
```tsx
const onSlideChanging = (args: SlideChangingEventArgs): void => {
  // Allow buttons but disable swipe
  if (args.isSwiped) {
    args.cancel = true;
  }
};
```
