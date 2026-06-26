---
title: "API Properties Reference"
description: "Complete reference guide for all Syncfusion React Carousel properties with code examples"
---

# Carousel API Properties

Comprehensive reference for all available Carousel component properties organized by functionality.

## Table of Contents

- [Core Data & Selection Properties](#core-data--selection-properties)
- [Animation & Timing Properties](#animation--timing-properties)
- [Navigation & Indicator Properties](#navigation--indicator-properties)
- [Template & Customization Properties](#template--customization-properties)
- [Interaction & Accessibility Properties](#interaction--accessibility-properties)
- [Layout & Localization Properties](#layout--localization-properties)

## Core Data & Selection Properties

### dataSource

External data source for carousel items. Pairs with `itemTemplate` for data-driven carousels.

**Type:** `any[]`

**Example:**
```tsx
const carouselData = [
  { id: 1, imageUrl: '/img1.jpg', title: 'Image 1' },
  { id: 2, imageUrl: '/img2.jpg', title: 'Image 2' },
  { id: 3, imageUrl: '/img3.jpg', title: 'Image 3' }
];

<CarouselComponent dataSource={carouselData} itemTemplate={itemTemplate} />
```

### itemTemplate

Template for rendering data-bound carousel items. Function receives item data as parameter.

**Type:** `(props: any) => JSX.Element | string`

**Example:**
```tsx
const itemTemplate = (props: any): JSX.Element => (
  <div className="carousel-item">
    <img src={props.imageUrl} alt={props.title} style={{width: '100%', height: '100%'}} />
    <h3>{props.title}</h3>
  </div>
);

<CarouselComponent dataSource={data} itemTemplate={itemTemplate} />
```

### items

Collection of CarouselItemModel for declarative item definition (alternative to dataSource).

**Type:** `CarouselItemModel[]`

**Example:**
```tsx
<CarouselComponent>
  <CarouselItemsDirective>
    <CarouselItemDirective template='<h3>Slide 1</h3>' />
    <CarouselItemDirective template='<h3>Slide 2</h3>' />
    <CarouselItemDirective template='<h3>Slide 3</h3>' />
  </CarouselItemsDirective>
</CarouselComponent>
```

### selectedIndex

Get or set the currently displayed slide by zero-based index. Updates when slide changes.

**Type:** `number`

**Default:** `0`

**Example:**
```tsx
// Set initial slide to 3rd item
<CarouselComponent selectedIndex={2}>
  {/* Carousel starts at index 2 */}
</CarouselComponent>

// Change slide programmatically
const [index, setIndex] = React.useState(0);

<>
  <CarouselComponent selectedIndex={index} />
  <button onClick={() => setIndex(2)}>Go to Slide 3</button>
</>
```

---

## Animation & Timing Properties

### animationEffect

Type of transition animation between slides.

**Type:** `'None' | 'Slide' | 'Fade' | 'Custom'`

**Default:** `'Slide'`

**Example:**
```tsx
// Fade animation
<CarouselComponent animationEffect="Fade">
  {/* Slides fade in/out */}
</CarouselComponent>

// Slide animation (default)
<CarouselComponent animationEffect="Slide">
  {/* Slides slide left/right */}
</CarouselComponent>

// No animation
<CarouselComponent animationEffect="None">
  {/* Instant transition */}
</CarouselComponent>

// Custom animation with CSS class
<CarouselComponent animationEffect="Custom" cssClass="parallax-carousel">
  {/* Apply custom CSS animations */}
</CarouselComponent>
```

### interval

Milliseconds each slide displays before auto-transitioning. Can be set globally or per-item.

**Type:** `number`

**Default:** `5000`

**Example:**
```tsx
// Global interval: all slides display for 3 seconds
<CarouselComponent interval={3000} autoPlay={true}>
  {/* All slides shown for 3000ms */}
</CarouselComponent>

// Per-item intervals (item binding only)
<CarouselComponent autoPlay={true}>
  <CarouselItemsDirective>
    <CarouselItemDirective template='<h3>Fast (1s)</h3>' interval={1000} />
    <CarouselItemDirective template='<h3>Normal (3s)</h3>' interval={3000} />
    <CarouselItemDirective template='<h3>Slow (5s)</h3>' interval={5000} />
  </CarouselItemsDirective>
</CarouselComponent>
```

### autoPlay

Enable automatic slide transitions at specified interval.

**Type:** `boolean`

**Default:** `false`

**Example:**
```tsx
// Enable auto-play: slides advance every 4 seconds
<CarouselComponent autoPlay={true} interval={4000}>
  {/* Automatic transitions */}
</CarouselComponent>

// Disable auto-play: manual navigation only
<CarouselComponent autoPlay={false}>
  {/* User must click buttons or swipe */}
</CarouselComponent>
```

### loop

Enable looping: return to first slide after last slide, or stop at end.

**Type:** `boolean`

**Default:** `true`

**Example:**
```tsx
// Loop enabled (default)
<CarouselComponent loop={true}>
  {/* Clicking next on last slide goes to first slide */}
</CarouselComponent>

// Loop disabled
<CarouselComponent loop={false}>
  {/* Clicking next on last slide does nothing */}
  {/* Next button disabled on last slide */}
</CarouselComponent>
```

### pauseOnHover

Pause automatic slide transitions when user hovers over carousel.

**Type:** `boolean`

**Default:** `true`

**Example:**
```tsx
// Pause on hover (default)
<CarouselComponent autoPlay={true} pauseOnHover={true}>
  {/* Auto-play stops when hovering over carousel */}
</CarouselComponent>

// Continue during hover
<CarouselComponent autoPlay={true} pauseOnHover={false}>
  {/* Auto-play continues even when hovering */}
</CarouselComponent>
```

---

## Navigation & Indicator Properties

### buttonsVisibility

Control when previous/next navigator buttons are displayed.

**Type:** `'Hidden' | 'Visible' | 'VisibleOnHover'`

**Default:** `'VisibleOnHover'`

**Example:**
```tsx
// Always hidden
<CarouselComponent buttonsVisibility="Hidden">
  {/* No navigation buttons visible */}
</CarouselComponent>

// Always visible
<CarouselComponent buttonsVisibility="Visible">
  {/* Navigation buttons always shown */}
</CarouselComponent>

// Only visible on hover
<CarouselComponent buttonsVisibility="VisibleOnHover">
  {/* Buttons appear on hover (or always on mobile) */}
</CarouselComponent>
```

### showIndicators

Display slide position indicators (dots/progress bar).

**Type:** `boolean`

**Default:** `true`

**Example:**
```tsx
// Show indicators
<CarouselComponent showIndicators={true}>
  {/* Indicators visible at bottom */}
</CarouselComponent>

// Hide indicators
<CarouselComponent showIndicators={false}>
  {/* No position indicators */}
</CarouselComponent>
```

### indicatorsType

Style and type of slide position indicators.

**Type:** `'Default' | 'Dynamic' | 'Fraction' | 'Progress'`

**Default:** `'Default'`

**Example:**
```tsx
// Default: Bullet style dots
<CarouselComponent indicatorsType="Default" showIndicators={true}>
  {/* Displays as filled/empty circles */}
</CarouselComponent>

// Dynamic: Animated indicators
<CarouselComponent indicatorsType="Dynamic" showIndicators={true}>
  {/* Indicators animate on slide change */}
</CarouselComponent>

// Fraction: Numeric display
<CarouselComponent indicatorsType="Fraction" showIndicators={true}>
  {/* Shows "2/5", "3/5" format */}
</CarouselComponent>

// Progress: Progress bar
<CarouselComponent indicatorsType="Progress" showIndicators={true}>
  {/* Shows progress bar at bottom */}
</CarouselComponent>
```

### showPlayButton

Display play/pause button for controlling auto-play.

**Type:** `boolean`

**Default:** `false`

**Example:**
```tsx
// Show play/pause button
<CarouselComponent showPlayButton={true} autoPlay={true} buttonsVisibility="Visible">
  {/* Play/pause button appears with navigation buttons */}
</CarouselComponent>

// Hide play button
<CarouselComponent showPlayButton={false}>
  {/* No play/pause button */}
</CarouselComponent>
```

---

## Template & Customization Properties

### previousButtonTemplate

Custom template for previous navigation button.

**Type:** `(props: any) => JSX.Element | string`

**Example:**
```tsx
const prevButtonTemplate = (props: any): JSX.Element => (
  <button className="custom-prev-btn">
    <span className="e-icons e-chevron-left"></span> Prev
  </button>
);

<CarouselComponent previousButtonTemplate={prevButtonTemplate} buttonsVisibility="Visible">
  {/* Custom previous button rendered */}
</CarouselComponent>
```

### nextButtonTemplate

Custom template for next navigation button.

**Type:** `(props: any) => JSX.Element | string`

**Example:**
```tsx
const nextButtonTemplate = (props: any): JSX.Element => (
  <button className="custom-next-btn">
    Next <span className="e-icons e-chevron-right"></span>
  </button>
);

<CarouselComponent nextButtonTemplate={nextButtonTemplate} buttonsVisibility="Visible">
  {/* Custom next button rendered */}
</CarouselComponent>
```

### playButtonTemplate

Custom template for play/pause button.

**Type:** `(props: any) => JSX.Element | string`

**Example:**
```tsx
const playButtonTemplate = (props: any): JSX.Element => (
  <button className="custom-play-btn">
    {props.isPlaying ? '⏸ Pause' : '▶ Play'}
  </button>
);

<CarouselComponent playButtonTemplate={playButtonTemplate} showPlayButton={true}>
  {/* Custom play/pause button rendered */}
</CarouselComponent>
```

### indicatorsTemplate

Custom template for slide position indicators.

**Type:** `(props: any) => JSX.Element | string`

**Example:**
```tsx
const indicatorTemplate = (props: any): JSX.Element => (
  <span 
    className={`custom-indicator ${props.isActive ? 'active' : ''}`}
    data-slide-index={props.index}
  >
    {props.index + 1}
  </span>
);

<CarouselComponent indicatorsTemplate={indicatorTemplate} showIndicators={true}>
  {/* Custom indicators rendered */}
</CarouselComponent>
```

### cssClass

Apply one or more custom CSS classes to the carousel element.

**Type:** `string`

**Example:**
```tsx
// Single class
<CarouselComponent cssClass="custom-carousel">
  {/* 'custom-carousel' class applied */}
</CarouselComponent>

// Multiple classes
<CarouselComponent cssClass="custom-carousel dark-theme wide-mode">
  {/* All three classes applied */}
</CarouselComponent>
```

### partialVisible

Display adjacent slides partially visible for context.

**Type:** `boolean`

**Default:** `false`

**Example:**
```tsx
// Partial visible disabled (default)
<CarouselComponent partialVisible={false}>
  {/* Only current slide shown */}
</CarouselComponent>

// Partial visible enabled
<CarouselComponent partialVisible={true}>
  {/* Current + partial prev + partial next shown */}
</CarouselComponent>

// With loop disabled
<CarouselComponent partialVisible={true} loop={false}>
  {/* No partial on edges (first/last slides) */}
</CarouselComponent>
```

---

## Interaction & Accessibility Properties

### enableTouchSwipe

Allow users to navigate with touch swipe gestures on touch devices.

**Type:** `boolean`

**Default:** `true`

**Example:**
```tsx
// Touch swipe enabled (default)
<CarouselComponent enableTouchSwipe={true}>
  {/* Users can swipe left/right on mobile */}
</CarouselComponent>

// Touch swipe disabled
<CarouselComponent enableTouchSwipe={false}>
  {/* Only buttons/keyboard navigation */}
</CarouselComponent>
```

### swipeMode

Configure which input types trigger slide transitions (touch, mouse).

**Type:** `CarouselSwipeMode` (bitwise flags: Touch | Mouse)

**Default:** `Touch | Mouse`

**Example:**
```tsx
import { CarouselSwipeMode } from "@syncfusion/ej2-react-navigations";

// Touch swipe only
<CarouselComponent swipeMode={CarouselSwipeMode.Touch} enableTouchSwipe={true}>
  {/* Touch swipe enabled, mouse drag disabled */}
</CarouselComponent>

// Mouse drag only
<CarouselComponent swipeMode={CarouselSwipeMode.Mouse} enableTouchSwipe={true}>
  {/* Mouse drag enabled, touch swipe disabled */}
</CarouselComponent>

// Both touch and mouse (default)
<CarouselComponent 
  swipeMode={CarouselSwipeMode.Touch | CarouselSwipeMode.Mouse} 
  enableTouchSwipe={true}
>
  {/* Both enabled */}
</CarouselComponent>
```

### allowKeyboardInteraction

Enable keyboard navigation (arrow keys, Home, End, Space, Enter).

**Type:** `boolean`

**Default:** `true`

**Example:**
```tsx
// Keyboard navigation enabled (default)
<CarouselComponent allowKeyboardInteraction={true}>
  {/* Arrow keys, Home, End work */}
</CarouselComponent>

// Keyboard navigation disabled
<CarouselComponent allowKeyboardInteraction={false}>
  {/* Keyboard navigation disabled (useful for forms inside carousel) */}
</CarouselComponent>
```

---

## Layout & Localization Properties

### height

Component height in pixels or percentage string.

**Type:** `number | string`

**Example:**
```tsx
// Fixed pixel height
<CarouselComponent height={400}>
  {/* 400px tall */}
</CarouselComponent>

// Percentage height
<CarouselComponent height="100%">
  {/* Full parent height */}
</CarouselComponent>

// String with unit
<CarouselComponent height="500px">
  {/* 500 pixels tall */}
</CarouselComponent>
```

### width

Component width in pixels or percentage string.

**Type:** `number | string`

**Example:**
```tsx
// Fixed pixel width
<CarouselComponent width={800}>
  {/* 800px wide */}
</CarouselComponent>

// Percentage width
<CarouselComponent width="100%">
  {/* Full parent width */}
</CarouselComponent>

// String with unit
<CarouselComponent width="1000px">
  {/* 1000 pixels wide */}
</CarouselComponent>
```

### enableRtl

Enable right-to-left (RTL) text direction and layout mirroring.

**Type:** `boolean`

**Default:** `false`

**Example:**
```tsx
// RTL disabled (default)
<CarouselComponent enableRtl={false}>
  {/* Left-to-right layout */}
</CarouselComponent>

// RTL enabled
<CarouselComponent enableRtl={true}>
  {/* Arrows reverse, buttons mirror, layout flips */}
</CarouselComponent>
```

### enablePersistence

Persist carousel state (selected slide) between page reloads using localStorage.

**Type:** `boolean`

**Default:** `false`

**Example:**
```tsx
// Persistence disabled (default)
<CarouselComponent enablePersistence={false}>
  {/* Resets to first slide on reload */}
</CarouselComponent>

// Persistence enabled
<CarouselComponent enablePersistence={true} id="carousel-1">
  {/* Current slide saved and restored on reload */}
</CarouselComponent>
```

### locale

Set language/culture for localization (e.g., 'fr-FR', 'de-DE', 'es-ES').

**Type:** `string`

**Default:** Global locale

**Example:**
```tsx
// Override global locale for this carousel
<CarouselComponent locale="fr-FR">
  {/* Uses French localization if available */}
</CarouselComponent>

// Default locale
<CarouselComponent locale="en-US">
  {/* Uses English localization */}
</CarouselComponent>
```

### htmlAttributes

Set custom HTML attributes on the carousel element.

**Type:** `{ [key: string]: any }`

**Example:**
```tsx
const customAttributes = {
  'data-carousel-id': 'product-gallery',
  'role': 'region',
  'aria-label': 'Product carousel',
  'data-theme': 'dark'
};

<CarouselComponent htmlAttributes={customAttributes}>
  {/* Custom attributes added to carousel element */}
</CarouselComponent>
```

---

## Properties Quick Reference Table

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| **dataSource** | `any[]` | - | External data array for carousel items |
| **itemTemplate** | `Function` | - | Render template for data-bound items |
| **items** | `CarouselItemModel[]` | - | Declarative collection of carousel items |
| **selectedIndex** | `number` | `0` | Current slide index (0-based) |
| **animationEffect** | `string` | `'Slide'` | Transition animation type |
| **interval** | `number` | `5000` | Milliseconds per slide |
| **autoPlay** | `boolean` | `false` | Enable auto-transitions |
| **loop** | `boolean` | `true` | Enable slide looping |
| **pauseOnHover** | `boolean` | `true` | Pause auto-play on hover |
| **buttonsVisibility** | `string` | `'VisibleOnHover'` | Navigation button visibility |
| **showIndicators** | `boolean` | `true` | Show position indicators |
| **indicatorsType** | `string` | `'Default'` | Indicator style (Default, Dynamic, Fraction, Progress) |
| **showPlayButton** | `boolean` | `false` | Show play/pause button |
| **previousButtonTemplate** | `Function` | - | Custom previous button UI |
| **nextButtonTemplate** | `Function` | - | Custom next button UI |
| **playButtonTemplate** | `Function` | - | Custom play button UI |
| **indicatorsTemplate** | `Function` | - | Custom indicators UI |
| **cssClass** | `string` | - | Custom CSS classes |
| **partialVisible** | `boolean` | `false` | Show adjacent slides partially |
| **enableTouchSwipe** | `boolean` | `true` | Allow touch swipe |
| **swipeMode** | `CarouselSwipeMode` | `Touch \| Mouse` | Swipe input types |
| **allowKeyboardInteraction** | `boolean` | `true` | Enable keyboard navigation |
| **height** | `number \| string` | - | Component height |
| **width** | `number \| string` | - | Component width |
| **enableRtl** | `boolean` | `false` | Right-to-left layout |
| **enablePersistence** | `boolean` | `false` | Persist state between reloads |
| **locale** | `string` | - | Language/culture setting |
| **htmlAttributes** | `object` | - | Custom HTML attributes |
