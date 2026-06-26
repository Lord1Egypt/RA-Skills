# Styling & Customization

## Table of Contents
- [Theme Application](#theme-application)
- [CSS Class Customization](#css-class-customization)
- [Animation Variations](#animation-variations)
- [Responsive Breakpoints](#responsive-breakpoints)
- [RTL Support](#rtl-support)
- [Custom Animations](#custom-animations)

---

## Theme Application

### Available Themes

Syncfusion provides four built-in themes:

```jsx
// 1. Material Theme (Default, Modern)
import '@syncfusion/ej2-navigations/styles/material.css';
import '@syncfusion/ej2-base/styles/material.css';

// 2. Bootstrap Theme (Bootstrap design)
import '@syncfusion/ej2-navigations/styles/bootstrap5.css';
import '@syncfusion/ej2-base/styles/bootstrap5.css';

// 3. Fluent Theme (Microsoft Fluent)
import '@syncfusion/ej2-navigations/styles/fluent.css';
import '@syncfusion/ej2-base/styles/fluent.css';

// 4. Tailwind Theme (Tailwind CSS)
import '@syncfusion/ej2-navigations/styles/tailwind.css';
import '@syncfusion/ej2-base/styles/tailwind.css';
```

### Dynamic Theme Switching

```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [theme, setTheme] = useState('material');

  const switchTheme = (newTheme) => {
    setTheme(newTheme);
    // Remove old theme
    document.querySelectorAll('link[data-theme]').forEach(link => {
      link.remove();
    });
    // Add new theme
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `url`;
    link.setAttribute('data-theme', newTheme);
    document.head.appendChild(link);
  };

  return (
    <div>
      <div className="theme-switcher">
        <button onClick={() => switchTheme('material')}>Material</button>
        <button onClick={() => switchTheme('bootstrap5')}>Bootstrap</button>
        <button onClick={() => switchTheme('fluent')}>Fluent</button>
      </div>
      <SidebarComponent type="Over" width="250px">
        Themed Sidebar
      </SidebarComponent>
    </div>
  );
}

export default App;
```

---

## CSS Class Customization

### Component Classes

Key Syncfusion sidebar CSS classes:

```css
/* Sidebar container */
.e-sidebar { }

/* When sidebar is open */
.e-sidebar.e-open { }

/* When sidebar is closed */
.e-sidebar:not(.e-open) { }

/* Backdrop overlay */
.e-sidebar-overlay { }

/* Content within sidebar */
.e-sidebar-content { }
```

### Custom Styling Example

```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import './CustomSidebar.css';

function App() {
  const sidebarRef = useRef(null);

  return (
    <SidebarComponent
      ref={sidebarRef}
      type="Over"
      width="280px"
      cssClass="custom-sidebar"
    >
      <h3>Custom Styled Sidebar</h3>
      <ul>
        <li><a href="#home">Home</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </SidebarComponent>
  );
}

export default App;
```

### CustomSidebar.css

```css
/* Custom sidebar styling */
.custom-sidebar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.custom-sidebar h3 {
  color: white;
  padding: 20px;
  margin: 0;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
}

.custom-sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.custom-sidebar ul li {
  margin: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.custom-sidebar ul li a {
  display: block;
  padding: 15px 20px;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  transition: all 0.3s ease;
}

.custom-sidebar ul li a:hover {
  background-color: rgba(255, 255, 255, 0.1);
  padding-left: 25px;
}

.custom-sidebar ul li a:active {
  background-color: rgba(255, 255, 255, 0.2);
}

/* Overlay styling */
.custom-sidebar + .e-sidebar-overlay {
  background-color: rgba(0, 0, 0, 0.7);
}
```

---

## Animation Variations

### Animation Speed Control

```css
/* Slow animation (700ms) */
.slow-animation.e-sidebar {
  transition: transform 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Fast animation (200ms) */
.fast-animation.e-sidebar {
  transition: transform 0.2s ease-out;
}

/* Standard animation (300ms) */
.standard-animation.e-sidebar {
  transition: transform 0.3s ease-in-out;
}
```

### Easing Functions

```css
/* Ease-in (slow start) */
.ease-in.e-sidebar {
  transition: transform 0.4s ease-in;
}

/* Ease-out (slow end) */
.ease-out.e-sidebar {
  transition: transform 0.4s ease-out;
}

/* Custom cubic-bezier (bouncy) */
.bouncy.e-sidebar {
  transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

/* Custom cubic-bezier (smooth) */
.smooth.e-sidebar {
  transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

### Animation Presets

```jsx
import React, { useState, useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function AnimatedSidebar() {
  const [animationType, setAnimationType] = useState('standard');
  const sidebarRef = useRef(null);

  return (
    <div>
      <select onChange={(e) => setAnimationType(e.target.value)}>
        <option value="standard">Standard</option>
        <option value="slow">Slow</option>
        <option value="fast">Fast</option>
        <option value="bouncy">Bouncy</option>
      </select>

      <SidebarComponent
        ref={sidebarRef}
        type="Over"
        width="250px"
        cssClass={`${animationType}-animation`}
        animate={true}
      >
        Animated Sidebar
      </SidebarComponent>
    </div>
  );
}

export default AnimatedSidebar;
```

---

## Responsive Breakpoints

### Mobile-First Responsive Design

```jsx
import React, { useState, useEffect } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function ResponsiveSidebar() {
  const [config, setConfig] = useState({
    type: 'Over',
    width: '80vw',
    breakpoint: 'mobile'
  });

  useEffect(() => {
    const updateLayout = () => {
      const width = window.innerWidth;
      
      if (width < 576) {
        // Small mobile
        setConfig({
          type: 'Over',
          width: '85vw',
          breakpoint: 'xs'
        });
      } else if (width < 768) {
        // Large mobile
        setConfig({
          type: 'Over',
          width: '75vw',
          breakpoint: 'sm'
        });
      } else if (width < 992) {
        // Tablet
        setConfig({
          type: 'Push',
          width: '280px',
          breakpoint: 'md'
        });
      } else if (width < 1200) {
        // Small desktop
        setConfig({
          type: 'Push',
          width: '300px',
          breakpoint: 'lg'
        });
      } else {
        // Large desktop
        setConfig({
          type: 'Push',
          width: '320px',
          breakpoint: 'xl'
        });
      }
    };

    updateLayout();
    window.addEventListener('resize', updateLayout);
    return () => window.removeEventListener('resize', updateLayout);
  }, []);

  return (
    <SidebarComponent
      type={config.type}
      width={config.width}
    >
      Responsive: {config.breakpoint}
    </SidebarComponent>
  );
}

export default ResponsiveSidebar;
```

### Responsive CSS Media Queries

```css
/* Extra small (< 576px) */
@media (max-width: 575px) {
  .e-sidebar {
    width: 85vw !important;
  }
  .sidebar-header h3 {
    font-size: 18px;
  }
}

/* Small (576px - 768px) */
@media (min-width: 576px) and (max-width: 767px) {
  .e-sidebar {
    width: 75vw !important;
  }
}

/* Medium (768px - 992px) */
@media (min-width: 768px) and (max-width: 991px) {
  .e-sidebar {
    width: 280px !important;
  }
  .sidebar-header h3 {
    font-size: 20px;
  }
}

/* Large (992px - 1200px) */
@media (min-width: 992px) and (max-width: 1199px) {
  .e-sidebar {
    width: 300px !important;
  }
}

/* Extra large (>= 1200px) */
@media (min-width: 1200px) {
  .e-sidebar {
    width: 320px !important;
  }
  .sidebar-content {
    padding: 25px;
  }
}
```

---

## RTL Support

### Enable RTL Mode

```jsx
<SidebarComponent
  enableRtl={true}
  position="Right"
  type="Push"
>
  محتوى الشريط الجانبي
</SidebarComponent>
```

### RTL CSS Adjustments

```css
/* RTL specific styles */
body[dir="rtl"] .e-sidebar {
  border-right: none;
  border-left: 1px solid #ddd;
}

body[dir="rtl"] .e-sidebar h3 {
  text-align: right;
}

body[dir="rtl"] .e-sidebar ul li a {
  text-align: right;
  padding-right: 20px;
  padding-left: 0;
}

body[dir="rtl"] .e-sidebar ul li a:hover {
  padding-right: 25px;
  padding-left: 0;
}

body[dir="rtl"] .sidebar-content {
  direction: rtl;
}
```

### Complete RTL Example

```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function RTLSidebar() {
  const [isRTL, setIsRTL] = useState(false);

  React.useEffect(() => {
    if (isRTL) {
      document.documentElement.dir = 'rtl';
      document.documentElement.lang = 'ar';
    } else {
      document.documentElement.dir = ltr';
      document.documentElement.lang = 'en';
    }
  }, [isRTL]);

  return (
    <div>
      <button onClick={() => setIsRTL(!isRTL)}>
        {isRTL ? 'Switch to LTR' : 'Switch to RTL'}
      </button>

      <SidebarComponent
        enableRtl={isRTL}
        position={isRTL ? 'Right' : 'Left'}
        type="Push"
        width="280px"
      >
        <h3>{isRTL ? 'المحتوى' : 'Content'}</h3>
        <ul>
          <li><a href="#home">{isRTL ? 'الرئيسية' : 'Home'}</a></li>
          <li><a href="#about">{isRTL ? 'حول' : 'About'}</a></li>
          <li><a href="#contact">{isRTL ? 'اتصل' : 'Contact'}</a></li>
        </ul>
      </SidebarComponent>
    </div>
  );
}

export default RTLSidebar;
```

---

## Custom Animations

### Slide In from Top

```css
@keyframes slideFromTop {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.slide-top.e-sidebar.e-open {
  animation: slideFromTop 0.4s ease-out;
}
```

### Fade and Zoom

```css
@keyframes fadeZoom {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.fade-zoom.e-sidebar.e-open {
  animation: fadeZoom 0.3s ease-out;
}
```

### Rotate Entrance

```css
@keyframes rotateEnter {
  from {
    transform: rotateY(90deg);
    opacity: 0;
  }
  to {
    transform: rotateY(0);
    opacity: 1;
  }
}

.rotate-enter.e-sidebar.e-open {
  animation: rotateEnter 0.5s ease-out;
  perspective: 1000px;
}
```

### Custom Animation Implementation

```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import './CustomAnimations.css';

function AnimatedSidebarDemo() {
  const sidebarRef = useRef(null);
  const [animation, setAnimation] = React.useState('slide-left');

  const animations = [
    'slide-left',
    'fade-slide',
    'fade-zoom',
    'rotate-enter',
    'bounce-in'
  ];

  return (
    <div>
      <div className="animation-selector">
        {animations.map(anim => (
          <button
            key={anim}
            onClick={() => setAnimation(anim)}
            className={animation === anim ? 'active' : ''}
          >
            {anim}
          </button>
        ))}
      </div>

      <SidebarComponent
        ref={sidebarRef}
        type="Over"
        width="280px"
        cssClass={animation}
        animate={true}
      >
        Animated Sidebar
      </SidebarComponent>
    </div>
  );
}

export default AnimatedSidebarDemo;
```

### CustomAnimations.css

```css
/* Bounce In */
@keyframes bounceIn {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); opacity: 1; }
}

.bounce-in.e-sidebar.e-open {
  animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

/* Fade and Slide */
@keyframes fadeSlide {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.fade-slide.e-sidebar.e-open {
  animation: fadeSlide 0.4s ease-out;
}
```

---
