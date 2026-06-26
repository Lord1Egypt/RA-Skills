# Animations and Transitions

## Table of Contents
- [Animation Effects](#animation-effects)
- [Setting Intervals Between Slides](#setting-intervals-between-slides)
- [Auto Play Configuration](#auto-play-configuration)
- [Pause on Hover](#pause-on-hover)
- [Looping Slides](#looping-slides)
- [Slide Changing Events](#slide-changing-events)
- [Touch Swipe Control](#touch-swipe-control)
- [Swipe Modes](#swipe-modes)

## Animation Effects

The `animationEffect` property controls the visual transition between slides.

### Fade Animation

Slides fade out and fade in for a smooth transition:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent animationEffect="Fade">
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

### Slide Animation (Default)

Slides move horizontally across the carousel area (default behavior):

```tsx
<CarouselComponent animationEffect="Slide">
  {/* items */}
</CarouselComponent>
```

Or omit the prop entirely since "Slide" is the default.

### Custom Animation

Define custom CSS animations using the `Custom` effect with CSS class:

```tsx
<CarouselComponent animationEffect="Custom" cssClass="parallax">
  <CarouselItemsDirective>
    <CarouselItemDirective template='<h3>Slide 1</h3>' />
    <CarouselItemDirective template='<h3>Slide 2</h3>' />
    <CarouselItemDirective template='<h3>Slide 3</h3>' />
  </CarouselItemsDirective>
</CarouselComponent>
```

Define your CSS animations in your stylesheet:

```css
.e-carousel.parallax .e-carousel-item {
  animation: parallaxMove 0.5s ease-in-out;
}

@keyframes parallaxMove {
  0% {
    transform: translateX(100%) rotateY(30deg);
    opacity: 0;
  }
  100% {
    transform: translateX(0) rotateY(0);
    opacity: 1;
  }
}
```

## Setting Intervals Between Slides

Control how long each slide displays before transitioning. Intervals are specified in milliseconds.

### Different Intervals Per Item

When using CarouselItem binding, each item can have its own interval:

```tsx
<CarouselComponent>
  <CarouselItemsDirective>
    <CarouselItemDirective template='<h3>Slide 1 - 3 seconds</h3>' interval={3000} />
    <CarouselItemDirective template='<h3>Slide 2 - 1 second</h3>' interval={1000} />
    <CarouselItemDirective template='<h3>Slide 3 - 2 seconds</h3>' interval={2000} />
    <CarouselItemDirective template='<h3>Slide 4 - 5 seconds</h3>' interval={5000} />
    <CarouselItemDirective template='<h3>Slide 5 - 6 seconds</h3>' interval={6000} />
  </CarouselItemsDirective>
</CarouselComponent>
```

**Default interval:** 5000 ms (5 seconds)

## Auto Play Configuration

### Enable Auto Play

Slides transition automatically using the `autoPlay` property:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent autoPlay={true}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

**Default:** `autoPlay={false}`

### Disable Auto Play

```tsx
<CarouselComponent autoPlay={false}>
  {/* Manual navigation only */}
</CarouselComponent>
```

## Pause on Hover

By default, auto-play pauses when the user hovers over the carousel. Control this with `pauseOnHover`:

### Enable Pause on Hover (Default)

```tsx
<CarouselComponent autoPlay={true} pauseOnHover={true}>
  {/* Auto-play stops on hover, resumes when mouse leaves */}
</CarouselComponent>
```

### Disable Pause on Hover

Keep auto-play running even when hovering:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent pauseOnHover={false}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

## Looping Slides

Control whether slides repeat infinitely or stop at the end.

### Enable Loop (Default)

```tsx
<CarouselComponent loop={true}>
  {/* After last slide, returns to first slide */}
</CarouselComponent>
```

### Disable Loop

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent loop={false}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

**Behavior:**
- With `loop={true}`: Next button on last slide goes to first slide
- With `loop={false}`: Next button disabled on last slide; auto-play stops

## Slide Changing Events

Listen to slide transitions using `slideChanging` and `slideChanged` events:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective, SlideChangingEventArgs, SlideChangedEventArgs } from '@syncfusion/ej2-react-navigations';
import * as React from 'react';

const App = () => {
  const onSlideChanging = (args: SlideChangingEventArgs): void => {
    console.log('About to change to slide:', args.nextSlide);
    // Perform actions before slide change (preload images, etc.)
  }

  const onSlideChanged = (args: SlideChangedEventArgs): void => {
    console.log('Changed to slide:', args.currentSlide);
    // Perform actions after slide change (update UI, log analytics, etc.)
  }

  return (
    <div className='control-container'>
      <CarouselComponent slideChanging={onSlideChanging} slideChanged={onSlideChanged}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

**Event Properties:**
- `args.currentSlide` - Current slide index
- `args.nextSlide` - Next slide index (in slideChanging)

## Touch Swipe Control

Enable or disable touch swipe gestures using the `enableTouchSwipe` property:

### Enable Touch Swipe (Default)

```tsx
<CarouselComponent enableTouchSwipe={true}>
  {/* Users can swipe left/right to navigate */}
</CarouselComponent>
```

### Disable Touch Swipe

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent enableTouchSwipe={false}>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<h3>Slide 1</h3>' />
          <CarouselItemDirective template='<h3>Slide 2</h3>' />
          <CarouselItemDirective template='<h3>Slide 3</h3>' />
          <CarouselItemDirective template='<h3>Slide 4</h3>' />
          <CarouselItemDirective template='<h3>Slide 5</h3>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

## Swipe Modes

The `swipeMode` property defines which input types trigger slide transitions using bitwise operators:

### Touch Only

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective, CarouselSwipeMode } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent swipeMode={CarouselSwipeMode.Touch}>
        {/* Touch gestures work, mouse drag does not */}
      </CarouselComponent>
    </div>
  );
}

export default App;
```

### Mouse Only

```tsx
<CarouselComponent swipeMode={CarouselSwipeMode.Mouse}>
  {/* Mouse drag works, touch gestures do not */}
</CarouselComponent>
```

### Touch and Mouse

```tsx
<CarouselComponent swipeMode={CarouselSwipeMode.Touch & CarouselSwipeMode.Mouse}>
  {/* Both touch and mouse drag work */}
</CarouselComponent>
```

### Disable Both

```tsx
<CarouselComponent swipeMode={~CarouselSwipeMode.Touch & ~CarouselSwipeMode.Mouse}>
  {/* No swipe/drag navigation */}
</CarouselComponent>
```

**Note:** Swipe mode is separate from button navigation. Disabling swipe modes doesn't affect prev/next buttons or keyboard navigation.

## Best Practices

- **Auto-play:** Use 5-10 seconds per slide for readability
- **Animations:** Fade for clean transitions, Slide for directional clarity
- **Mobile:** Enable touch swipe with "Touch" or "Touch & Mouse" mode
- **Events:** Use slideChanged for analytics, slideChanging for validation
- **Loop:** Disable for ordered content; enable for decorative galleries
