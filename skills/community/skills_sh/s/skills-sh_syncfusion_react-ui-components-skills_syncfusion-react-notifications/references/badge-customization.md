# Badge Customization

## Table of Contents
- [Color Customization](#color-customization)
- [Size Customization](#size-customization)
- [Custom Positioning](#custom-positioning)

---

## Color Customization

The Badge provides eight built-in color variants. When those don't match your design requirements, apply a custom CSS class to override the badge's background and text colors.

The pattern is to keep a built-in color class for the base styles and add your own class to override color properties:

```tsx
import * as React from "react";
import * as ReactDOM from "react-dom";

function App() {
    return (
        <div>
            <h1>Color Customization <span className="e-badge e-badge-primary e-badge-pill green">New</span></h1>
            <h1>Color Customization <span className="e-badge e-badge-primary e-badge-pill bue">New</span></h1>
            <h1>Color Customization <span className="e-badge e-badge-primary e-badge-pill purple">New</span></h1>
            <h1>Color Customization <span className="e-badge e-badge-primary e-badge-pill gradient">New</span></h1>
        </div>
    );
}
export default App;
ReactDOM.render(<App />, document.getElementById("element"));
```

Define the custom classes in your CSS file:

```css
/* Example custom color overrides */
.e-badge.green {
  background-color: #4CAF50;
  color: #fff;
}

.e-badge.purple {
  background-color: #9C27B0;
  color: #fff;
}

.e-badge.gradient {
  background: linear-gradient(45deg, #f06, #48f);
  color: #fff;
}
```

> Use specific selectors (e.g., `.e-badge.green`) to avoid conflicts with other elements.

---

## Size Customization

The Badge automatically scales with its text content. To explicitly control the badge size, change the `font-size` CSS property — the badge dimensions respond proportionally.

```tsx
import * as React from "react";
import * as ReactDOM from "react-dom";

function App() {
    return (
        <div>
            <h1>Badge Component <span className="e-badge e-badge-primary size_1">New</span></h1>
            <h1>Badge Component <span className="e-badge e-badge-primary size_2">New</span></h1>
            <h1>Badge Component <span className="e-badge e-badge-primary size_3">New</span></h1>
        </div>
    );
}
export default App;
ReactDOM.render(<App />, document.getElementById("element"));
```

Define size classes in your CSS:

```css
.e-badge.size_1 {
  font-size: 10px;
}

.e-badge.size_2 {
  font-size: 14px;
}

.e-badge.size_3 {
  font-size: 18px;
}
```

> Changing `font-size` is the recommended way to resize badges — the padding, border-radius, and line-height all scale relative to the font size.

---

## Custom Positioning

The built-in `.e-badge-bottom` class only supports top and bottom placement. For left-side or other arbitrary positions, apply a custom CSS class that overrides the badge's `top`, `right`, `bottom`, and `left` properties.

```tsx
import * as React from "react";
import * as ReactDOM from "react-dom";

function App() {
    return (
        <div>
            <div className="block">
                {/* Left-top custom position */}
                <div className="badge-block">
                    <div className="firefox svg_icons"></div>
                    <span className="e-badge e-badge-warning e-badge-notification e-badge-overlap leftTop">99+</span>
                </div>
                <div className="badge-block">
                    <div className="facebook svg_icons"></div>
                    <span className="e-badge e-badge-danger e-badge-notification e-badge-overlap leftTop">99+</span>
                </div>
                <div className="badge-block">
                    <div className="skype svg_icons"></div>
                    <span className="e-badge e-badge-secondary e-badge-notification e-badge-overlap leftTop">18</span>
                </div>
            </div>
            <div className="badge-block">
                {/* Left-bottom custom position */}
                <div className="badge-block">
                    <div className="firefox svg_icons"></div>
                    <span className="e-badge e-badge-warning e-badge-notification e-badge-overlap leftBottom">99+</span>
                </div>
                <div className="badge-block">
                    <div className="facebook svg_icons"></div>
                    <span className="e-badge e-badge-danger e-badge-notification e-badge-overlap leftBottom">99+</span>
                </div>
                <div className="badge-block">
                    <div className="skype svg_icons"></div>
                    <span className="e-badge e-badge-secondary e-badge-notification e-badge-overlap leftBottom">18</span>
                </div>
            </div>
        </div>
    );
}
export default App;
ReactDOM.render(<App />, document.getElementById("element"));
```

Define the custom position classes in CSS:

```css
/* Left-top position */
.e-badge.leftTop {
  right: auto;
  left: -10px;
  top: -10px;
}

/* Left-bottom position */
.e-badge.leftBottom {
  right: auto;
  left: -10px;
  top: auto;
  bottom: -10px;
}
```

> Always keep `.e-badge-overlap` when using custom positions — it sets the `position: absolute` needed for CSS coordinate overrides to work.
