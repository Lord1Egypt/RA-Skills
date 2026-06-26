# Getting Started with Breadcrumb Component

## Table of Contents
- [Dependencies](#dependencies)
- [Development Environment Setup](#development-environment-setup)
- [Adding Syncfusion Packages](#adding-syncfusion-packages)
- [Adding Stylesheets](#adding-stylesheets)
- [Creating Your First Breadcrumb](#creating-your-first-breadcrumb)
- [Adding Items](#adding-items)
- [Enabling and Disabling Navigation](#enabling-and-disabling-navigation)

## Dependencies

The Syncfusion Breadcrumb component requires the following dependencies:

```
@syncfusion/ej2-react-navigations
├── @syncfusion/ej2-react-base
├── @syncfusion/ej2-navigations
│   ├── @syncfusion/ej2-base
│   ├── @syncfusion/ej2-data
│   ├── @syncfusion/ej2-inputs
│   ├── @syncfusion/ej2-lists
│   └── @syncfusion/ej2-popups
│       └── @syncfusion/ej2-buttons
```

These are automatically installed when you install `@syncfusion/ej2-react-navigations`.

## Development Environment Setup

### Option 1: Using Vite (Recommended)

Vite provides faster development, smaller bundle sizes, and optimized production builds.

**Create a new React application with TypeScript:**

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

**Create a new React application with JavaScript:**

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

**Benefits of Vite:**
- Faster hot module replacement (HMR)
- Smaller production bundles
- Optimized build process
- Better development experience

### Option 2: Using Create React App

If you prefer Create React App instead of Vite, use:

```bash
npx create-react-app my-app
cd my-app
npm start
```

## Adding Syncfusion Packages

Install the Breadcrumb component package:

```bash
npm install @syncfusion/ej2-react-navigations --save
```

This command installs all required dependencies for the Breadcrumb component.

## Adding Stylesheets

Add the Breadcrumb component stylesheets to your `App.css` or `App.tsx` file:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
```

**Available Themes:**
- `tailwind3.css` - Tailwind CSS theme (modern, clean)
- `bootstrap5.css` - Bootstrap 5 theme (classic)
- `fluent2.css` - Microsoft Fluent 2 theme (professional)
- `material3.css` - Material Design 3 theme (material design)

Choose the theme that matches your application's design system.

## Creating Your First Breadcrumb

Create a basic Breadcrumb component with no items:

```tsx
import { BreadcrumbComponent } from '@syncfusion/ej2-react-navigations';
import './App.css';

export default function App() {
  return (
    <BreadcrumbComponent enableNavigation={false}>
    </BreadcrumbComponent>
  );
}
```

**Key Props:**
- `enableNavigation={false}` - Disables navigation, breadcrumb is display-only

## Adding Items

Add breadcrumb items using `BreadcrumbItemsDirective` and `BreadcrumbItemDirective`:

```tsx
import { 
  BreadcrumbComponent, 
  BreadcrumbItemDirective, 
  BreadcrumbItemsDirective 
} from '@syncfusion/ej2-react-navigations';
import './App.css';

export default function App() {
  return (
    <BreadcrumbComponent enableNavigation={false}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective iconCss="e-icons e-home" url="url" />
        <BreadcrumbItemDirective text="Components" url="url" />
        <BreadcrumbItemDirective text="Navigations" url="url" />
        <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Item Properties:**
- `text` - Display text for the breadcrumb item
- `url` - Navigation URL (relative or absolute)
- `iconCss` - CSS class for icon (e.g., "e-icons e-home")

## Enabling and Disabling Navigation

The Breadcrumb component supports navigation control through the `enableNavigation` property.

### Navigation Disabled (Display Only)

When `enableNavigation={false}`, breadcrumb items are not clickable:

```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="e-icons e-home" url="url" />
    <BreadcrumbItemDirective text="Components" url="url" />
    <BreadcrumbItemDirective text="Navigations" url="url" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

### Navigation Enabled (Clickable Items)

When `enableNavigation={true}`, breadcrumb items become clickable:

```tsx
<BreadcrumbComponent enableNavigation={true}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="e-icons e-home" url="url" />
    <BreadcrumbItemDirective text="Components" url="url" />
    <BreadcrumbItemDirective text="Navigations" url="url" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Note:** The last breadcrumb item (active/current page) is not clickable by default, even when `enableNavigation={true}`. To make it clickable, use `enableActiveItemNavigation={true}`.

## Running Your Application

After setup, run your development server:

```bash
npm run dev
```

Your Breadcrumb component will be available at `url` (Vite) or `url` (Create React App).

## TypeScript Support

Full TypeScript support is available. Import types for better IDE support:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbBeforeItemRenderEventArgs, BreadcrumbClickEventArgs } from '@syncfusion/ej2-navigations';
```

This enables type checking and autocomplete for all props and events.
