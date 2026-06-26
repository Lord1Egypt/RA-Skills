# Getting Started with React Carousel

## Table of Contents

- [Installation and Dependencies](#installation-and-dependencies)
  - [Package Dependencies](#package-dependencies)
  - [Install via npm](#install-via-npm)
- [Development Environment Setup](#development-environment-setup)
  - [Option 1: Create React App with Vite (Recommended)](#option-1-create-react-app-with-vite-recommended)
  - [Option 2: Create React App (Traditional)](#option-2-create-react-app-traditional)
- [CSS Imports and Theme Configuration](#css-imports-and-theme-configuration)
  - [Tailwind 3 Theme](#tailwind-3-theme)
  - [Bootstrap 5.3 Theme](#bootstrap-53-theme)
  - [Material 3 Theme](#material-3-theme)
  - [Fluent 2 Theme](#fluent-2-theme)
- [Basic Carousel Component Setup](#basic-carousel-component-setup)
  - [Component Import](#component-import)
  - [Minimal Component Structure](#minimal-component-structure)
- [First Working Example: Image Gallery](#first-working-example-image-gallery)
- [Common Setup Issues](#common-setup-issues)
- [Running the Application](#running-the-application)
- [Video Tutorial](#video-tutorial)

## Installation and Dependencies

### Package Dependencies

The Carousel component requires the following packages:

```
|-- @syncfusion/ej2-react-navigations
    |-- @syncfusion/ej2-react-base
    |-- @syncfusion/ej2-navigations
        |-- @syncfusion/ej2-base
        |-- @syncfusion/ej2-buttons
```

### Install via npm

```bash
npm install @syncfusion/ej2-react-navigations --save
```

This command installs all required dependencies including base and button components.

## Development Environment Setup

### Option 1: Create React App with Vite (Recommended)

Vite provides faster development and smaller bundle sizes:

```bash
npm create vite@latest my-carousel-app -- --template react-ts
cd my-carousel-app
npm run dev
```

For JavaScript (without TypeScript):

```bash
npm create vite@latest my-carousel-app -- --template react
cd my-carousel-app
npm run dev
```

### Option 2: Create React App (Traditional)

```bash
npx create-react-app my-carousel-app
cd my-carousel-app
npm start
```

## CSS Imports and Theme Configuration

Add Carousel styles to `App.css` or your main stylesheet. Choose your preferred theme:

### Tailwind 3 Theme
```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
```

### Bootstrap 5.3 Theme
```css
@import "../node_modules/@syncfusion/ej2-base/styles/bootstrap5.3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/bootstrap5.3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/bootstrap5.3.css";
```

### Material 3 Theme
```css
@import "../node_modules/@syncfusion/ej2-base/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/material3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material3.css";
```

### Fluent 2 Theme
```css
@import "../node_modules/@syncfusion/ej2-base/styles/fluent2.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/fluent2.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/fluent2.css";
```

## Basic Carousel Component Setup

### Component Import

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";
```

### Minimal Component Structure

```tsx
const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent>
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

## First Working Example: Image Gallery

This complete example displays a carousel with five images:

```tsx
import { CarouselComponent, CarouselItemsDirective, CarouselItemDirective } from "@syncfusion/ej2-react-navigations";
import * as React from "react";
import * as ReactDOM from "react-dom";

const App = () => {
  return (
    <div className='control-container'>
      <CarouselComponent>
        <CarouselItemsDirective>
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="cardinal" style="height:100%;width:100%;" /><figcaption class="img-caption">Cardinal</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="kingfisher" style="height:100%;width:100%;" /><figcaption class="img-caption">Kingfisher</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="keel-billed-toucan" style="height:100%;width:100%;" /><figcaption class="img-caption">Keel-billed-toucan</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="yellow-warbler" style="height:100%;width:100%;" /><figcaption class="img-caption">Yellow-warbler</figcaption></figure>' />
          <CarouselItemDirective template='<figure class="img-container"><img src="url" alt="bee-eater" style="height:100%;width:100%;" /><figcaption class="img-caption">Bee-eater</figcaption></figure>' />
        </CarouselItemsDirective>
      </CarouselComponent>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('element'));
root.render(<App />);
```

## Common Setup Issues

### Issue: Styles not applying
- **Cause:** CSS import paths incorrect or missing theme file
- **Solution:** Verify CSS import statements match your `node_modules` structure. Run `npm list @syncfusion/ej2-base` to verify installation.

### Issue: Components not found
- **Cause:** Package not installed or import path wrong
- **Solution:** Run `npm install @syncfusion/ej2-react-navigations` and verify import paths use exact component names.

### Issue: Carousel not displaying
- **Cause:** Missing items or container styling
- **Solution:** Ensure container has explicit height: `<div style="height:400px;">` and carousel has at least one CarouselItemDirective child.

## Running the Application

After setup, start your development server:

**With Vite:**
```bash
npm run dev
```

**With Create React App:**
```bash
npm start
```

The carousel will render in your browser, typically at `http://localhost:5173` (Vite) or `http://localhost:3000` (CRA).

## Video Tutorial

For a visual walkthrough of setup and configuration, refer to the official Syncfusion React Carousel getting started video.
