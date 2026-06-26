# Textual CSS (TCSS) Reference

## Table of Contents
- [Selectors](#selectors)
- [Layout Properties](#layout-properties)
- [Sizing Properties](#sizing-properties)
- [Positioning Properties](#positioning-properties)
- [Appearance Properties](#appearance-properties)
- [Text Properties](#text-properties)
- [Scrolling Properties](#scrolling-properties)
- [Animation Properties](#animation-properties)
- [Theme Variables](#theme-variables)
- [Pseudo-classes](#pseudo-classes)

## Selectors

```css
/* Type selector - matches Python class name */
Button { }

/* ID selector */
#sidebar { }

/* Class selector */
.error { }

/* Compound selectors */
Button.primary { }

/* Descendant combinator */
#dialog Button { }

/* Child combinator */
Container > Button { }

/* Multiple selectors */
#submit, #cancel { }
```

## Nested CSS

```css
#container {
    background: $surface;

    .item {
        padding: 1;

        &:hover {
            background: $primary;
        }

        &.-active {
            border: solid green;
        }
    }
}
```

## Layout Properties

```css
layout: vertical;          /* vertical, horizontal, grid */

/* Grid layout */
grid-size: 3 2;           /* columns rows */
grid-columns: 1fr 2fr 1fr;
grid-rows: auto 1fr;
grid-gutter: 1 2;         /* vertical horizontal */
column-span: 2;
row-span: 2;
```

## Sizing Properties

```css
width: 50%;               /* auto, %, fr, cells */
height: 100%;
min-width: 20;
max-width: 80;
min-height: 10;
max-height: 50;

margin: 1 2;              /* vertical horizontal */
margin: 1 2 1 2;          /* top right bottom left */
padding: 1 2;
padding: 1 2 1 2;
```

## Positioning Properties

```css
dock: top;                /* top, right, bottom, left */
offset: 5 10;             /* x y offset */
offset-x: -100%;
offset-y: 50%;
layer: overlay;           /* layer name */
```

### Layers
```css
Screen {
    layers: base overlay modal;
}

#background { layer: base; }
#popup { layer: overlay; }
#dialog { layer: modal; }
```

## Appearance Properties

```css
background: darkblue;
color: white;

/* Borders */
border: solid green;      /* none, solid, double, round, heavy, tall, wide */
border-top: double red;
border-right: solid blue;
border-bottom: heavy green;
border-left: round yellow;

outline: dashed red;
opacity: 0.5;
```

## Text Properties

```css
text-align: center;       /* left, center, right */
content-align: center middle;  /* horizontal vertical */
text-style: bold italic;  /* bold, italic, underline, reverse, strike */
```

## Scrolling Properties

```css
overflow: auto;           /* auto, hidden, scroll */
overflow-x: auto;
overflow-y: scroll;
scrollbar-gutter: stable;
```

## Animation Properties

```css
transition: background 500ms;
transition: offset 200ms ease-in-out;
transition: opacity 300ms linear;

/* Multiple transitions */
transition: background 200ms, offset 300ms;
```

### Easing Functions
- `linear`
- `ease-in`
- `ease-out`
- `ease-in-out`

## Theme Variables

### Core Colors
```css
$primary
$secondary
$success
$warning
$error
$text
$background
$surface
$panel
```

### Color Variants
```css
$primary-lighten-1
$primary-lighten-2
$primary-lighten-3
$primary-darken-1
$primary-darken-2
$primary-darken-3
```

### Custom Variables
```css
$my-color: dodgerblue;
$spacing: 2;

.widget {
    background: $my-color;
    padding: $spacing;
}
```

## Pseudo-classes

```css
Button:hover { background: lightblue; }
Button:focus { border: double green; }
Button:disabled { opacity: 0.5; }

/* Custom state classes (prefixed with -) */
.sidebar.-visible { offset-x: 0; }
.item.-selected { background: $primary; }
```

## Common Patterns

### Animated Sidebar
```css
Sidebar {
    width: 30;
    dock: left;
    offset-x: -100%;
    transition: offset 200ms;

    &.-visible {
        offset-x: 0;
    }
}
```

### Centered Modal
```css
#modal {
    layer: modal;
    width: 60;
    height: 20;
    background: $surface;
    border: thick $primary;
}

Screen {
    align: center middle;
    layers: base modal;
}
```

### Responsive Grid
```css
Grid {
    layout: grid;
    grid-size: 3;
    grid-gutter: 1;
}

@media (max-width: 60) {
    Grid {
        grid-size: 2;
    }
}
```
