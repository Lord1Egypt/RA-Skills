# Accessibility

The Carousel component is built with accessibility standards in mind, following WAI-ARIA specifications and providing comprehensive keyboard navigation support.

## Table of Contents

- [Accessibility Compliance](#accessibility-compliance)
- [ARIA Attributes](#aria-attributes)
- [Keyboard Interaction](#keyboard-interaction)
- [Keyboard Shortcuts Reference](#keyboard-shortcuts-reference)
- [Screen Reader Support](#screen-reader-support)
- [Setting Up Application-Level Keyboard Focus](#setting-up-application-level-keyboard-focus)
- [Right-to-Left (RTL) Support](#right-to-left-rtl-support)
- [Color Contrast](#color-contrast)
- [Mobile Device Accessibility](#mobile-device-accessibility)
- [Example: Fully Accessible Carousel](#example-fully-accessible-carousel)
- [Testing for Accessibility](#testing-for-accessibility)
- [Common Accessibility Issues and Solutions](#common-accessibility-issues-and-solutions)

## Accessibility Compliance

| Accessibility Criteria | Support |
|------------------------|---------:|
| WCAG 2.2 | ✓ Full |
| Section 508 | ✓ Full |
| Screen Reader Support | ✓ Full |
| Right-To-Left (RTL) Support | ✓ Full |
| Color Contrast | ✓ Full |
| Mobile Device Support | ✓ Full |
| Keyboard Navigation | ✓ Full |
| Accessibility Checker Validation | ✓ Full |
| Axe-core Accessibility Validation | ✓ Full |

## ARIA Attributes

The Carousel component automatically includes the following ARIA attributes for assistive technology support:

| Attribute | Usage |
|-----------|-------|
| `aria-roledescription` | Describes the Carousel role and each slide as "slide" |
| `aria-label` | Labels for previous, next, and play/pause buttons |
| `aria-current` | Set to `true` for the active slide indicator |
| `aria-hidden` | Set to `true` for non-visible slides |
| `aria-live` | Set to `off` when autoPlay is enabled; `polite` when disabled |
| `aria-role` | Set to "group" for Carousel slide items |

These attributes are automatically applied—no additional configuration needed.

## Keyboard Interaction

All Carousel actions are fully controllable via keyboard. Enable or disable keyboard interaction with the `allowKeyboardInteraction` property:

```tsx
// Enable keyboard navigation (default)
<CarouselComponent allowKeyboardInteraction={true}>
  {/* items */}
</CarouselComponent>

// Disable if carousel contains form inputs
<CarouselComponent allowKeyboardInteraction={false}>
  {/* items */}
</CarouselComponent>
```

**Disable keyboard interaction when:** Your carousel contains text inputs or form controls, as arrow keys might trigger unwanted navigation.

## Keyboard Shortcuts Reference

Once the Carousel element has focus, use these keyboard shortcuts:

| Key | Action |
|-----|--------|
| <kbd>Alt + J</kbd> | Focus the Carousel component (set up at application level) |
| <kbd>←</kbd> Arrow Left | Navigate to previous slide |
| <kbd>→</kbd> Arrow Right | Navigate to next slide |
| <kbd>Home</kbd> | Jump to first slide |
| <kbd>End</kbd> | Jump to last slide |
| <kbd>Space</kbd> | Toggle play/pause auto-play |
| <kbd>Enter</kbd> | Perform action on focused element |
| <kbd>Tab</kbd> | Move focus to next interactive element |
| <kbd>Shift + Tab</kbd> | Move focus to previous interactive element |

## Screen Reader Support

The Carousel announces:
- Slide position when auto-play is disabled
- Current slide changes
- Navigator and indicator button purposes
- All interactive elements with appropriate labels

**Best practices for screen reader users:**
- Always include descriptive alt text in slide images
- Use semantic HTML in slide templates
- Provide meaningful button labels
- Test with NVDA (Windows), JAWS, or VoiceOver (Mac)

## Setting Up Application-Level Keyboard Focus

Configure Alt + J to focus the Carousel at the application level:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import { useRef } from "react";
import * as React from "react";

const App = () => {
  const carouselRef = useRef<CarouselComponent>(null);

  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.altKey && e.key === 'j') {
        // Focus carousel on Alt + J
        const carouselElement = carouselRef.current?.getHostElement();
        carouselElement?.focus();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div>
      <CarouselComponent ref={carouselRef} tabIndex={0}>
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

## Right-to-Left (RTL) Support

The Carousel automatically adapts to RTL languages. Enable RTL at the component or application level:

### Component-Level RTL

```tsx
<CarouselComponent enableRtl={true}>
  {/* items */}
</CarouselComponent>
```

### Application-Level RTL

```tsx
document.documentElement.dir = 'rtl';
```

**RTL Behavior:**
- Arrow keys reverse (← moves right, → moves left)
- Previous button appears on right, next on left
- Indicators remain centered but flow right-to-left
- Text direction reverses within slide templates

## Color Contrast

The Carousel uses sufficient color contrast (4.5:1 or higher) for all text and interactive elements by default. When customizing colors, ensure:

```css
/* ✓ Good contrast (4.5:1) */
.e-carousel-indicators .e-indicator {
    background-color: rgba(0, 0, 0, 0.5);  /* Dark background */
    color: white;  /* Light text */
}

/* ✗ Poor contrast (2:1) */
.e-carousel-indicators .e-indicator {
    background-color: #999;  /* Medium gray */
    color: #bbb;  /* Light gray - insufficient contrast */
}
```

Use tools like WebAIM Contrast Checker to verify custom colors.

## Mobile Device Accessibility

The Carousel supports touch-based navigation for mobile users:

```tsx
<CarouselComponent 
  enableTouchSwipe={true}  // Allow swipe gestures
  buttonsVisibility="Visible"  // Large buttons for touch
  swipeMode={CarouselSwipeMode.Touch & CarouselSwipeMode.Mouse}
>
  {/* items */}
</CarouselComponent>
```

**Mobile considerations:**
- Use larger touch targets (min 44×44 pixels)
- Provide visible navigation buttons (VisibleOnHover doesn't work on touch)
- Test with mobile screen readers (VoiceOver on iOS, TalkBack on Android)

## Example: Fully Accessible Carousel

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import { useRef } from "react";
import * as React from "react";

const AccessibleCarousel = () => {
  const carouselRef = useRef<CarouselComponent>(null);

  return (
    <div>
      <h2>Image Gallery</h2>
      <CarouselComponent 
        ref={carouselRef}
        tabIndex={0}
        allowKeyboardInteraction={true}
        enableRtl={false}
        enableTouchSwipe={true}
        buttonsVisibility="Visible"
        showIndicators={true}
        showPlayButton={false}  // Simplifies for screen readers
      >
        <CarouselItemsDirective>
          <CarouselItemDirective 
            template='<figure><img src="image1.jpg" alt="Mountain landscape at sunset" style="width:100%;height:100%;" /><figcaption>Mountain Landscape</figcaption></figure>' 
          />
          <CarouselItemDirective 
            template='<figure><img src="image2.jpg" alt="Ocean waves with seagulls" style="width:100%;height:100%;" /><figcaption>Ocean Waves</figcaption></figure>' 
          />
          <CarouselItemDirective 
            template='<figure><img src="image3.jpg" alt="Forest path with tall trees" style="width:100%;height:100%;" /><figcaption>Forest Path</figcaption></figure>' 
          />
        </CarouselItemsDirective>
      </CarouselComponent>
      <p>Use arrow keys or tab to navigate. Press Enter to interact.</p>
    </div>
  );
}

export default AccessibleCarousel;
```

## Testing for Accessibility

### Manual Testing Checklist
- [ ] Tab through all interactive elements (buttons, indicators)
- [ ] Keyboard navigation works (arrows, Home, End, Space)
- [ ] Focus indicator clearly visible
- [ ] Screen reader announces slide changes
- [ ] Color contrast passes WCAG AA (4.5:1)
- [ ] Touch targets min 44×44 pixels on mobile

### Automated Testing Tools
- **axe-core:** Browser extension for accessibility scanning
- **Accessibility Checker:** Chrome extension
- **WAVE:** Web accessibility evaluation tool
- **Lighthouse:** Chrome DevTools built-in audit

## Common Accessibility Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Keyboard focus lost | Focus not managed | Use `tabIndex={0}` on Carousel |
| Screen reader silent | ARIA attributes missing | Use component defaults; don't override |
| Low contrast buttons | Custom CSS override | Verify 4.5:1 ratio with WCAG tool |
| Touch targets too small | CSS sizing | Min 44×44 pixels on mobile |
| Auto-play too fast | `autoPlay` with short interval | Use 5+ second intervals |
