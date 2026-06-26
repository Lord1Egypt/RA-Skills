---
name: syncfusion-react-carousel
description: Complete guide to implementing the Syncfusion React Carousel component for rotating image galleries, product carousels, slideshow presentations, testimonials, and sequential content display. Use this skill when working with slide transitions, navigation controls, animations, styling, and accessibility features. Covers installation, item population, and all API properties, methods, and events.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing the Syncfusion React Carousel Component

## Table of Contents

- [Overview](#component-overview)
- [Getting Started](#getting-started)
- [Populating Items and Selection](#populating-items-and-selection)
- [Navigation and Indicators](#navigation-and-indicators)
- [Animations and Transitions](#animations-and-transitions)
- [API Properties](#api-properties)
- [API Methods](#api-methods)
- [API Events](#api-events)
- [Styling and Appearance](#styling-and-appearance)
- [Accessibility](#accessibility)
- [Image Optimization](#image-optimization)
- [Common Patterns](#common-patterns)
- [Use Cases](#use-cases)

The Syncfusion React Carousel component is a powerful, fully-featured carousel for displaying images, content, or any sequential items with automatic or manual transitions. It supports multiple animation effects, customizable indicators and navigators, keyboard navigation, and comprehensive accessibility features.

## When to Use This Skill

**Implement the Carousel component when you need to:**
- Create rotating image galleries with smooth transitions
- Build slideshow presentations with navigation controls
- Display product carousels for e-commerce sites
- Implement testimonial sliders with indicators
- Build content carousels with auto-play functionality
- Support touch/swipe navigation on mobile devices
- Display items with accessibility compliance (WCAG 2.2, Section 508)

## Component Overview

The Carousel component manages:
- **Visual Display:** Renders one active slide with customizable templates
- **Navigation:** Previous/next buttons with multiple visibility modes
- **Indicators:** Show current position with multiple indicator types (dots, fractions, progress bars)
- **Animations:** Smooth slide transitions with fade, slide, or custom effects
- **Interaction:** Auto-play, manual swipe, keyboard navigation
- **Accessibility:** Full ARIA support, keyboard shortcuts, screen reader compatibility

**Core imports:**
```ts
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
```

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package dependencies
- Development environment setup with Vite or Create React App
- CSS imports and theme configuration (Tailwind, Bootstrap, Fluent, Material)
- Basic carousel component setup
- First working example with items
- Common setup issues and solutions

**When to read:** First time setting up Carousel or troubleshooting initial setup problems.

### Populating Items and Selection
📄 **Read:** [references/populating-items.md](references/populating-items.md)
- Populating slides using CarouselItem directives
- Data source binding with itemTemplate
- Setting initial slide with selectedIndex
- Navigation with prev() and next() methods
- Partial visible slides (showing adjacent slides)
- Programmatic vs. declarative slide rendering

**When to read:** Building slide content, handling dynamic data, or implementing navigation controls.

### Navigators and Indicators
📄 **Read:** [references/navigators-and-indicators.md](references/navigators-and-indicators.md)
- Previous/next navigator button visibility modes
- Custom navigator button templates
- Showing/hiding indicators (progress dots)
- Four indicator types: Default, Dynamic, Fraction, Progress
- Indicator templates with preview images
- Play/pause button control and templates

**When to read:** Customizing navigation UI, changing indicator style, or implementing play controls.

### Animations and Transitions
📄 **Read:** [references/animations-and-transitions.md](references/animations-and-transitions.md)
- Animation effects (Fade, Slide, Custom CSS)
- Setting slide transition intervals per item
- Auto-play configuration and timing
- Pause on hover behavior
- Looping and non-looping behavior
- Touch swipe modes and disabled interactions
- Slide changing events (slideChanging, slideChanged)

**When to read:** Implementing smooth transitions, configuring auto-play, or adding custom animations.

### Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- CSS class structure for customization
- Customizing indicator appearance and spacing
- Navigator button positioning and styling
- Partial slide area customization
- Theme Studio integration for visual theming
- Dark mode and custom color schemes

**When to read:** Styling indicators/navigators, positioning elements, or creating custom themes.

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- ARIA attributes and roles
- Keyboard interaction shortcuts (arrows, Home, End, Space, Enter)
- Screen reader support
- Focus management and mobile accessibility

**When to read:** Building accessible carousels or implementing keyboard navigation.

### Image Optimization
📄 **Read:** [references/image-optimization.md](references/image-optimization.md)
- Loading carousel images in WebP format
- Performance benefits and file size reduction
- Image format conversion techniques
- Implementation with carousel items

**When to read:** Optimizing carousel performance or implementing modern image formats.

## Quick Start Example

**Minimal working carousel with 5 images:**

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="cardinal" style="height:100%;width:100%;" /><figcaption class="img-caption">Cardinal</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="kingfisher" style="height:100%;width:100%;" /><figcaption class="img-caption">Kingfisher</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="toucan" style="height:100%;width:100%;" /><figcaption class="img-caption">Toucan</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="warbler" style="height:100%;width:100%;" /><figcaption class="img-caption">Warbler</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="bee-eater" style="height:100%;width:100%;" /><figcaption class="img-caption">Bee-eater</figcaption></figure>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

export default App;
```

## Common Patterns

### Pattern 1: Auto-Play Gallery with Indicators and Navigators
```tsx
<CarouselComponent autoPlay={true} showIndicators={true} buttonsVisibility="Visible">
  <CarouselItemsDirective>
    {/* items */}
  </CarouselItemsDirective>
</CarouselComponent>
```

### Pattern 2: Data-Driven Carousel with Dynamic Content
```tsx
const itemTemplate = (props: any): JSX.Element => {
  return <img src={props.imageUrl} alt={props.title} />;
}

<CarouselComponent dataSource={carouselData} itemTemplate={itemTemplate} />
```

### Pattern 3: Carousel with Custom Navigation Buttons
```tsx
const nextButtonTemplate = (props: any): JSX.Element => {
  return <ButtonComponent iconCss="e-icons e-chevron-right" />;
}

<CarouselComponent nextButtonTemplate={nextButtonTemplate} />
```

### Pattern 4: Touch-Enabled Mobile Carousel
```tsx
<CarouselComponent 
  enableTouchSwipe={true} 
  swipeMode={CarouselSwipeMode.Touch & CarouselSwipeMode.Mouse}
  pauseOnHover={true}
>
  {/* items */}
</CarouselComponent>
```

## API Properties Overview

**Core Display Properties:**
- `dataSource` - Bind carousel to external data
- `itemTemplate` - Template for data-bound items
- `items` - Collection of CarouselItemModel
- `selectedIndex` - Current slide index

**Animation & Behavior:**
- `animationEffect` - Animation type (None, Slide, Fade, Custom)
- `interval` - Transition delay in milliseconds (default: 5000)
- `autoPlay` - Enable auto-play (default: false)
- `loop` - Loop slides infinitely (default: true)
- `pauseOnHover` - Pause on hover (default: true)
- `enableTouchSwipe` - Enable touch swiping (default: true)
- `swipeMode` - Touch/mouse swipe modes (Touch, Mouse)

**UI Controls:**
- `buttonsVisibility` - Navigator buttons (Hidden, Visible, VisibleOnHover)
- `showIndicators` - Show indicators (default: true)
- `showPlayButton` - Show play/pause button (default: false)
- `indicatorsType` - Indicator style (Default, Dynamic, Fraction, Progress)

**Customization:**
- `previousButtonTemplate` - Previous button UI
- `nextButtonTemplate` - Next button UI
- `playButtonTemplate` - Play/pause button UI
- `indicatorsTemplate` - Indicators UI
- `cssClass` - Custom CSS classes
- `partialVisible` - Show adjacent slides (default: false)
- `allowKeyboardInteraction` - Keyboard navigation (default: true)

**Layout & Localization:**
- `height` - Component height (pixels/percentage)
- `width` - Component width (pixels/percentage)
- `enableRtl` - Right-to-left support
- `enablePersistence` - Persist state between reloads
- `locale` - Culture/localization setting
- `htmlAttributes` - Custom HTML attributes

## Common Use Cases

**1. Product Gallery (E-Commerce)**
- Display product images with fade animation
- Show indicators to indicate available images
- Enable swipe for mobile users
- See: [populating-items.md](references/populating-items.md) + [animations-and-transitions.md](references/animations-and-transitions.md)

**2. Testimonial/Review Carousel**
- Auto-play testimonials with 10-second intervals
- Custom testimonial template
- Pause on hover to allow reading
- See: [populating-items.md](references/populating-items.md) + [animations-and-transitions.md](references/animations-and-transitions.md)

**3. Accessible Banner Carousel**
- Keyboard navigation with Home/End/Arrow keys
- WCAG 2.2 compliant structure
- Screen reader friendly labels
- See: [accessibility.md](references/accessibility.md)

**4. Styled Hero Carousel**
- Custom navigator and indicator styling
- Partial visible slides for context
- Theme Studio customization
- See: [styling-and-appearance.md](references/styling-and-appearance.md) + [navigators-and-indicators.md](references/navigators-and-indicators.md)

**5. Data-Bound Carousel**
- Bind carousel to REST API data
- Dynamic templates based on item properties
- Real-time updates
- See: [populating-items.md](references/populating-items.md)

## Complete API Reference

### API Properties Reference
📄 **Read:** [references/api-properties.md](references/api-properties.md)

Comprehensive documentation for all 28+ carousel properties organized by functionality:
- **Core Data & Selection:** dataSource, itemTemplate, items, selectedIndex
- **Animation & Timing:** animationEffect, interval, autoPlay, loop, pauseOnHover
- **Navigation & Indicators:** buttonsVisibility, showIndicators, indicatorsType, showPlayButton
- **Template & Customization:** Button/indicator templates, cssClass, partialVisible
- **Interaction & Accessibility:** enableTouchSwipe, swipeMode, allowKeyboardInteraction
- **Layout & Localization:** height, width, enableRtl, enablePersistence, locale, htmlAttributes

Each property includes type information, default values, and practical code examples.

### API Methods Reference
📄 **Read:** [references/api-methods.md](references/api-methods.md)

Complete documentation for all carousel control methods:
- **`next()`** - Navigate to next slide with loop support
- **`prev()`** - Navigate to previous slide with loop support
- **`getHostElement()`** - Access underlying carousel DOM element

Includes method signatures, use cases, practical examples, and advanced patterns like skip multiple slides, go to specific slide, and scroll-to-carousel functionality.

### API Events Reference
📄 **Read:** [references/api-events.md](references/api-events.md)

Comprehensive event documentation with complete event arguments:
- **`slideChanging`** - Fires BEFORE transition (cancelable)
  - Arguments: cancel, currentIndex, currentSlide, nextIndex, nextSlide, isSwiped, name, slideDirection
  - Use cases: Validation, confirmation dialogs, preventing access to specific slides

- **`slideChanged`** - Fires AFTER transition (not cancelable)
  - Arguments: currentIndex, currentSlide, previousIndex, previousSlide, isSwiped, name, slideDirection
  - Use cases: Analytics tracking, updating UI counters, loading content, triggering animations

Includes practical examples for rate limiting, history tracking, analytics integration, and event pattern library.

## Next Steps

1. **Start here:** Read [getting-started.md](references/getting-started.md) to install and configure
2. **Add content:** Follow [populating-items.md](references/populating-items.md) for your data
3. **Customize UI:** Use [navigators-and-indicators.md](references/navigators-and-indicators.md) for controls
4. **Enhance behavior:** Reference [animations-and-transitions.md](references/animations-and-transitions.md) for effects
5. **Polish design:** Apply [styling-and-appearance.md](references/styling-and-appearance.md) for styling
6. **Ensure access:** Implement [accessibility.md](references/accessibility.md) for compliance
7. **Optimize images:** Use [image-optimization.md](references/image-optimization.md) for performance
