# Styling and Appearance

Customize the Carousel component's visual appearance using CSS classes and the Theme Studio. The Carousel uses a predictable CSS class hierarchy for targeted styling.

## Table of Contents

- [CSS Structure in React Carousel](#css-structure-in-react-carousel)
- [Customizing Indicators](#customizing-indicators)
  - [Spacing Between Indicators](#spacing-between-indicators)
  - [Indicator Size and Shape](#indicator-size-and-shape)
  - [Indicator Position](#indicator-position)
- [Customizing Navigators](#customizing-navigators)
  - [Navigator Icon Size and Color](#navigator-icon-size-and-color)
  - [Navigator Button Background](#navigator-button-background)
  - [Navigator Position](#navigator-position)
- [Customizing Partial Slides Size](#customizing-partial-slides-size)
  - [Example: Responsive Partial Slides](#example-responsive-partial-slides)
- [Carousel Item Styling](#carousel-item-styling)
  - [Style Active Slide](#style-active-slide)
  - [Slide Transitions](#slide-transitions)
  - [Carousel Container Styling](#carousel-container-styling)
- [Theme Studio Integration](#theme-studio-integration)
  - [Import Custom Theme](#import-custom-theme)
- [Dark Mode Implementation](#dark-mode-implementation)
- [Full Customization Example](#full-customization-example)
- [Best Practices](#best-practices)

## CSS Structure in React Carousel

The following table lists CSS classes used by the Carousel component:

| CSS Class | Purpose |
|-----------|---------|
| `.e-carousel` | Root carousel container |
| `.e-carousel-item` | Individual carousel slide |
| `.e-carousel-item.e-active` | Currently active/visible slide |
| `.e-carousel-indicators` | Indicators container |
| `.e-carousel-indicators .e-indicator-bars` | Indicator bars wrapper |
| `.e-carousel-indicators .e-indicator-bars .e-indicator-bar` | Individual indicator bar |
| `.e-carousel-indicators .e-indicator-bars .e-indicator-bar .e-indicator` | Indicator dot/element |
| `.e-carousel-navigators` | Navigator buttons container |
| `.e-carousel-navigators .e-previous` | Previous button wrapper |
| `.e-carousel-navigators .e-next` | Next button wrapper |
| `.e-carousel-navigators .e-play-pause` | Play/pause button wrapper |
| `.e-carousel.e-partial .e-carousel-slide-container` | Partial visible slides container |

## Customizing Indicators

### Spacing Between Indicators

Increase or decrease space between indicator dots:

```css
.e-carousel .e-carousel-indicators .e-indicator-bars .e-indicator-bar {
    padding: 8px;
}
```

Adjust padding value (in pixels) to control spacing. Default is typically 4-6px.

### Indicator Size and Shape

Customize individual indicator appearance:

```css
.e-carousel .e-carousel-indicators .e-indicator-bars .e-indicator-bar .e-indicator {
    width: 20px;
    height: 20px;
    border-radius: 100%;
    background-color: rgba(255, 255, 255, 0.5);
    transition: all 0.3s ease;
}

.e-carousel .e-carousel-indicators .e-indicator-bars .e-indicator-bar .e-indicator.e-active {
    background-color: white;
    width: 30px;
    border-radius: 10px;
}
```

### Indicator Position

By default, indicators appear at the bottom center. Move them outside the carousel:

```css
.e-carousel .e-carousel-indicators {
    bottom: auto;
    top: -50px;  /* Place above carousel */
}
```

Or position at top inside:

```css
.e-carousel .e-carousel-indicators {
    top: 20px;
    bottom: auto;
}
```

## Customizing Navigators

### Navigator Icon Size and Color

Change the previous/next button icon appearance:

```css
.e-carousel .e-carousel-navigators .e-next .e-btn:not(:disabled) .e-btn-icon,
.e-carousel .e-carousel-navigators .e-previous .e-btn:not(:disabled) .e-btn-icon
{
    color: greenyellow;
    font-size: 25px;
}
```

### Navigator Button Background

Style the navigator button backgrounds:

```css
.e-carousel .e-carousel-navigators .e-previous,
.e-carousel .e-carousel-navigators .e-next
{
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    padding: 10px;
}
```

### Navigator Position

Move navigators from center to bottom or custom position:

```css
.e-carousel .e-carousel-navigators {
    top: auto;
    bottom: 20px;
}
```

Or position outside the carousel:

```css
.e-carousel .e-carousel-navigators .e-previous,
.e-carousel .e-carousel-navigators .e-next
{
    margin: -60px;  /* Pull outside carousel boundary */
    background: black;
}
```

## Customizing Partial Slides Size

When `partialVisible={true}`, customize the visible area of adjacent slides:

```css
.e-carousel.e-partial .e-carousel-slide-container {
    padding: 0 150px;  /* Show 150px of adjacent slides */
}
```

Increase padding value to show more of partial slides; decrease to show less.

### Example: Responsive Partial Slides

```css
/* Desktop */
.e-carousel.e-partial .e-carousel-slide-container {
    padding: 0 150px;
}

/* Tablet */
@media (max-width: 768px) {
    .e-carousel.e-partial .e-carousel-slide-container {
        padding: 0 100px;
    }
}

/* Mobile */
@media (max-width: 480px) {
    .e-carousel.e-partial .e-carousel-slide-container {
        padding: 0 50px;
    }
}
```

## Carousel Item Styling

### Style Active Slide

Apply styles only to the currently displayed slide:

```css
.e-carousel-item.e-active {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transform: scale(1.02);
}
```

### Slide Transitions

Add smooth transitions between slides:

```css
.e-carousel-item {
    transition: all 0.3s ease-in-out;
}
```

### Carousel Container Styling

Style the main carousel container:

```css
.e-carousel {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
```

## Theme Studio Integration

Use Syncfusion Theme Studio to generate custom themes:

1. Visit [Theme Studio]
2. Select "Carousel" component
3. Customize colors, spacing, and typography
4. Export the custom CSS
5. Import in your application

### Import Custom Theme

```css
@import "./custom-carousel-theme.css";
```

## Dark Mode Implementation

Create a dark theme variant:

```css
/* Light mode (default) */
.e-carousel {
    background-color: white;
    color: #333;
}

.e-carousel .e-carousel-indicators .e-indicator-bar .e-indicator {
    background-color: rgba(0, 0, 0, 0.3);
}

/* Dark mode */
.dark-theme .e-carousel {
    background-color: #1e1e1e;
    color: #fff;
}

.dark-theme .e-carousel .e-carousel-indicators .e-indicator-bar .e-indicator {
    background-color: rgba(255, 255, 255, 0.3);
}
```

## Full Customization Example

```css
/* Carousel container */
.e-carousel {
    background-color: #f5f5f5;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Items */
.e-carousel-item {
    border-radius: 12px;
    overflow: hidden;
}

.e-carousel-item.e-active {
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1);
}

/* Indicators - fancy design */
.e-carousel .e-carousel-indicators {
    background: linear-gradient(to top, rgba(0, 0, 0, 0.3), transparent);
    padding-bottom: 15px;
}

.e-carousel .e-carousel-indicators .e-indicator-bar .e-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.5);
    margin: 0 6px;
    transition: all 0.3s ease;
}

.e-carousel .e-carousel-indicators .e-indicator-bar .e-indicator.e-active {
    background-color: white;
    width: 32px;
    border-radius: 6px;
}

/* Navigators - subtle design */
.e-carousel .e-carousel-navigators .e-previous,
.e-carousel .e-carousel-navigators .e-next {
    background-color: rgba(0, 0, 0, 0.4);
    border-radius: 4px;
    transition: background-color 0.3s ease;
}

.e-carousel .e-carousel-navigators .e-previous:hover,
.e-carousel .e-carousel-navigators .e-next:hover {
    background-color: rgba(0, 0, 0, 0.6);
}

.e-carousel .e-carousel-navigators .e-previous .e-btn-icon,
.e-carousel .e-carousel-navigators .e-next .e-btn-icon {
    color: white;
    font-size: 18px;
}
```

## Best Practices

- Use CSS classes for static styles
- Use Theme Studio for consistent branding
- Test dark mode with `prefers-color-scheme` media query
- Ensure sufficient color contrast for accessibility
- Keep custom CSS organized and maintainable
