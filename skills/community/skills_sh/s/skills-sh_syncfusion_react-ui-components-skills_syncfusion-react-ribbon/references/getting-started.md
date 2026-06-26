# Getting Started with Syncfusion React Ribbon

## Table of Contents
- [Installation](#installation)
- [Setup Project](#setup-project)
- [Add Styles](#add-styles)
- [Create Basic Ribbon](#create-basic-ribbon)
- [Module Injection](#module-injection)
- [Run Application](#run-application)

## Installation

Install the Ribbon component package via npm:

```bash
npm install @syncfusion/ej2-react-ribbon --save
```

### Project Setup

For a new React TypeScript project, use Vite (recommended for faster development):

```bash
npm create vite@latest my-ribbon-app -- --template react-ts
cd my-ribbon-app
npm run dev
```

For JavaScript only:

```bash
npm create vite@latest my-ribbon-app -- --template react
cd my-ribbon-app
npm run dev
```

## Add Styles

Import the Ribbon styles into your application. Open `src/App.css` and add the following imports:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-ribbon/styles/tailwind3.css";
```

**Available Theme Files:**
- `material.css` - Material Design theme
- `bootstrap.css` - Bootstrap theme
- `bootstrap4.css` - Bootstrap 4 theme
- `fluent.css` - Fluent Design theme
- `tailwind3.css` - Tailwind CSS theme (recommended)

Choose the theme file that matches your application's design system.

## Create Basic Ribbon

Open `src/App.tsx` and create a basic Ribbon component:

```tsx
import { RibbonComponent } from "@syncfusion/ej2-react-ribbon";
import "./App.css";

function App() {
  return (
    <RibbonComponent id="ribbon"></RibbonComponent>
  );
}

export default App;
```

This creates an empty Ribbon. To add functionality, you need to define tabs and groups (see ribbon-structure.md).

## Module Injection

Some Ribbon features require module injection. Use the `Inject` component to register services:

```tsx
import { RibbonComponent, RibbonFileMenu, RibbonColorPicker, Inject } from "@syncfusion/ej2-react-ribbon";

function App() {
  return (
    <RibbonComponent id="ribbon">
      <Inject services={[RibbonFileMenu, RibbonColorPicker]} />
    </RibbonComponent>
  );
}

export default App;
```

**Available services for injection:**
- `RibbonFileMenu` - File menu feature
- `RibbonColorPicker` - Color picker item
- `RibbonContextualTab` - Contextual tab feature
- `RibbonGallery` - Gallery item type
- `RibbonBackstage` - Backstage view (if using file menu with backstage)

## Complete Minimal Example

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";
import "./App.css";

function App() {
  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-paste", content: "Paste" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

## Run Application

Start the development server:

```bash
npm run dev
```

The Ribbon component is now running. Navigate to the provided local URL (typically http://localhost:5173).

## TypeScript Configuration

Syncfusion components have full TypeScript support. For a React TypeScript project, type definitions are automatically included. Ensure your `tsconfig.json` has proper React settings:

```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"]
  }
}
```

## Troubleshooting

**Styles not applying:**
- Verify all CSS imports are correct in `App.css`
- Check that the theme file path matches your node_modules structure
- Ensure CSS is imported before creating components

**Components not rendering:**
- Verify all required imports are included
- Check that Ribbon ID is unique
- Ensure parent HTML element with id="element" or similar exists

**Module not found errors:**
- Run `npm install` to ensure
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
