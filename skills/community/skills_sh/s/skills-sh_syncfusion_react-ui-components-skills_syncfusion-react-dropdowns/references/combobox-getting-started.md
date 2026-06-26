# Getting Started with ComboBox

## Table of Contents
- [Installation](#installation)
- [Basic Setup](#basic-setup)
- [CSS Imports](#css-imports)
- [Component Implementation](#component-implementation)
- [Custom Values](#custom-values)
- [Popup Configuration](#popup-configuration)

---

## Installation

### Step 1: Install Package

```bash
npm install @syncfusion/ej2-react-dropdowns --save
```

This installs the Syncfusion dropdown components package, which includes ComboBox, DropdownList, MultiSelect, and Mention components.

### Step 2: Verify Installation

```bash
npm list @syncfusion/ej2-react-dropdowns
```

Should show: `@syncfusion/ej2-react-dropdowns@<version>`

---

## Basic Setup

### Create a React Application

If you don't have a React project, create one using Vite (recommended for faster builds):

```bash
npm create vite@latest my-combobox-app -- --template react
cd my-combobox-app
npm install
npm run dev
```

Or with TypeScript:

```bash
npm create vite@latest my-combobox-app -- --template react-ts
cd my-combobox-app
npm install
npm run dev
```

---

## CSS Imports

### Add Syncfusion Styles

Edit `src/App.css` and add the following imports **before** your custom CSS:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";
```

**Available Themes:**
- `tailwind3.css` - Tailwind CSS (recommended, modern)
- `bootstrap5.css` - Bootstrap 5 style
- `fluent.css` - Microsoft Fluent Design
- `fabric.css` - Microsoft Fabric

Choose ONE theme based on your design system.

### Import in App.tsx

```tsx
import './App.css';  // Your CSS with Syncfusion imports
```

---

## Component Implementation

### Functional Component (Recommended)

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

export default function App() {
  const sportsList = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  return (
    <div className="app-container">
      <h2>Select a Sport</h2>
      <ComboBoxComponent 
        id="sports-combo"
        dataSource={sportsList}
        placeholder="Choose a sport..."
      />
    </div>
  );
}
```

### Class Component

```tsx
import { ComboBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';
import './App.css';

export default class App extends React.Component<{}, {}> {
  private sportsList: string[] = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  public render() {
    return (
      <div className="app-container">
        <h2>Select a Sport</h2>
        <ComboBoxComponent 
          id="sports-combo"
          dataSource={this.sportsList}
          placeholder="Choose a sport..."
        />
      </div>
    );
  }
}
```

---

## Custom Values

### Enable User-Defined Values

By default, `allowCustom={true}` lets users enter values not in the dropdown list.

```tsx
const gamesList = ['Chess', 'Carrom', 'Badminton'];

<ComboBoxComponent 
  id="games-combo"
  dataSource={gamesList}
  allowCustom={true}  // User can type custom value
  placeholder="Select or type a game..."
  change={(e) => console.log('Selected value:', e.value)}
/>
```

**Behavior:**
- ✅ User can select from list
- ✅ User can type and create a new value
- ✅ Custom value is submitted with form

**Example Workflow:**
1. User types "Scrabble" (not in list)
2. Presses Enter or leaves field
3. "Scrabble" becomes the selected value
4. Form submission includes "Scrabble"

---

## Popup Configuration

### Customize Dropdown Appearance

Control the popup list size and behavior:

```tsx
<ComboBoxComponent 
  id="combobox"
  dataSource={largeDataset}
  placeholder="Select an item..."
  popupHeight="250px"          // Dropdown list height
  popupWidth="300px"            // Dropdown list width
  allowFiltering={true}         // Show search box in dropdown
/>
```

### Responsive Popup

For mobile-friendly design, use percentage-based widths:

```tsx
<ComboBoxComponent 
  id="combobox"
  dataSource={sportsList}
  popupHeight="auto"            // Auto-fit to content
  popupWidth="100%"             // Full width (for mobile)
/>
```

### Default Popup Behavior

| Property | Default | Purpose |
|----------|---------|---------|
| `popupHeight` | 300px | Dropdown height with scrollbar |
| `popupWidth` | 100% | Dropdown width (matches input width) |
| `showClearButton` | true | Show X button to clear selection |

---

## First Implementation Checklist

- [ ] Package installed: `npm install @syncfusion/ej2-react-dropdowns`
- [ ] CSS imports added to `App.css`
- [ ] ComboBoxComponent imported in component file
- [ ] dataSource prop populated with data
- [ ] placeholder text added for UX
- [ ] change handler (optional) for selection events
- [ ] If using `enableVirtualization={true}`: import `Inject` and `VirtualScroll` from `@syncfusion/ej2-react-dropdowns` and add `<Inject services={[VirtualScroll]} />` inside `<ComboBoxComponent>`
- [ ] Application runs: `npm run dev`
- [ ] ComboBox appears and is clickable

---

## Next Steps

- **Binding complex data?** → Go to [data-binding.md](data-binding.md)
- **Want search capability?** → See [filtering-and-search.md](filtering-and-search.md)
- **Need grouping?** → Check [grouping-and-sorting.md](grouping-and-sorting.md)
- **Want custom UI?** → Explore [templates-and-customization.md](templates-and-customization.md)
