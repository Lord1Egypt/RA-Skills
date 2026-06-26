---
name: syncfusion-react-common
description: Common utilities and features for Syncfusion React components. Use this skill when the user needs to implement animations, drag-and-drop, state persistence, RTL support, localization, globalization, security, templates, and advanced features for Syncfusion React components.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Common Features"
---

# Common Features in Syncfusion React Components

Syncfusion React components include comprehensive common utilities and features that enhance user experience, ensure cross-cultural support, and provide foundational capabilities across all components. This skill covers installation setup, animations, globalization, state management, and security considerations for building robust React applications.

## Table of Contents

- [Navigation Guide](#navigation-guide)
- [Quick Start](#quick-start)
- [Common Features](#common-features)

## Navigation Guide

### Getting Started & Framework Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Framework integration (Next.js, Remix, Vite, Preact, SharePoint)
- Package installation and CSS imports
- Component initialization
- Quick start examples

### Globalization
📄 **Read:** [references/globalization.md](references/globalization.md)
- Right-to-left (RTL) support for Arabic, Hebrew, Persian languages
- Localization (l10n) for multi-language support
- Internationalization (i18n) with CLDR data
- Number and currency formatting
- Date and time formatting

### Advanced Features & Utilities
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Animation effects (FadeIn, ZoomOut, SlideUp, etc.)
- Animation timing (duration, delay, global settings)
- Drag-and-drop interactions (Draggable, Droppable)
- Template customization and optimization
- State persistence with enablePersistence
- Security best practices and HTML sanitization

## Quick Start

### Install Syncfusion React Package

```bash
npm install @syncfusion/ej2-react-grids@latest --save
```

> **Note:** The `@syncfusion/ej2-base` package is a dependency for all Syncfusion components and will be automatically installed when you install any Syncfusion React package. You don't need to explicitly add it to your `package.json` file.

### Import Styles

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-grids/styles/tailwind3.css";
```

### Register License Key

**Step 1:** Set the environment variable:

```bash
# Windows
setx SYNCFUSION_LICENSE "Your_License_Key_Here"

# Mac/Linux
export SYNCFUSION_LICENSE='Your_License_Key_Here'
```

**Step 2:** Activate the license using NPX command:

```bash
npx syncfusion-license activate
```

> **Note:** For alternative license registration methods, kindly refer to the [Syncfusion license key registration documentation](https://ej2.syncfusion.com/react/documentation/licensing/license-key-registration).

### Basic Component Setup

```typescript
import * as React from 'react';
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-grids';

function App() {
  const data = [
    { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
    { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 }
  ];

  return (
    <GridComponent dataSource={data} allowPaging={true}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' width='100' />
        <ColumnDirective field='CustomerID' width='100' />
        <ColumnDirective field='Freight' width='100' format="C2" />
      </ColumnsDirective>
      <Inject services={[Page]} />
    </GridComponent>
  );
}

export default App;
```

## Common Features

### Enable State Persistence

```typescript
<GridComponent dataSource={data} enablePersistence={true}>
  {/* Component content */}
</GridComponent>
```

### Enable RTL Support

```typescript
import { enableRtl } from '@syncfusion/ej2-base';

// Global RTL enablement
enableRtl(true);

// OR per-component
<ListViewComponent enableRtl={true} />
```

### Add Animation Effects

```typescript
import { Animation } from '@syncfusion/ej2-base';

useEffect(() => {
  const animation = new Animation({ duration: 5000, delay: 2000 });
  animation.animate(element, { name: 'FadeOut' });
}, []);
```

### Implement Drag-and-Drop

```typescript
import { Draggable, Droppable } from '@syncfusion/ej2-base';

useEffect(() => {
  const draggable = new Draggable(document.getElementById('draggable'), { clone: false });
  const droppable = new Droppable(document.getElementById('droppable'), {
    drop: (e) => {
      e.droppedElement.textContent = 'Dropped!';
    }
  });
}, []);
```
