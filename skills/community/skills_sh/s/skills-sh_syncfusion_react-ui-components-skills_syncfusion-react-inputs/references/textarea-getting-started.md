# Getting Started with React TextArea Component

## Table of Contents
- [Installation](#installation)
- [Setup](#setup)
- [Basic Implementation](#basic-implementation)
- [CSS Configuration](#css-configuration)
- [Getting and Setting Values](#getting-and-setting-values)
- [First Render](#first-render)

## Installation

### Install the TextArea Package

The Syncfusion TextArea component is part of the `@syncfusion/ej2-react-inputs` package published on npmjs.com.

```bash
npm install @syncfusion/ej2-react-inputs --save
```

The `--save` flag adds the package to your `package.json` dependencies section.

## Setup

### Vite Project Setup (Recommended)

Vite provides faster development and optimized builds compared to traditional tools. To create a new React application with Vite:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

For JavaScript environment (without TypeScript):

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

For detailed steps, refer to the [Vite installation guide](https://vitejs.dev/guide).

### Create React App (Alternative)

For traditional React setup:

```bash
npx create-react-app my-app
cd my-app
npm start
```

## CSS Configuration

### Add Syncfusion Styles

The TextArea component requires CSS files from the Syncfusion package. Add these imports to your **src/App.css** file:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-inputs/styles/tailwind3.css";
```

Then import `App.css` in your **src/App.tsx** (or App.jsx) file:

```typescript
import './App.css';
```

## Basic Implementation

### Simple TextArea

Add the TextArea component to **src/App.tsx**:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <TextAreaComponent id='default' />
  );
}

export default App;
```

### TextArea with Placeholder

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default' 
        placeholder='Enter your comments' 
      />
    </div>
  );
}

export default App;
```

### TextArea with Floating Label

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default' 
        placeholder='Enter your comments'
        floatLabelType='Auto'
      />
    </div>
  );
}

export default App;
```

## First Render

### Running the Application

Execute the development server:

```bash
npm run dev
```

The application will:
1. Compile your code
2. Start a local development server
3. Open in your default browser

The TextArea component will render as an empty multiline text input field.

### Output Structure

```html
<div class='wrap'>
  <textarea 
    id='default' 
    class='e-field e-input'
    placeholder='Enter your comments'
  ></textarea>
</div>
```

## Getting and Setting Values

### Set Initial Value with Property

Use the `value` property to set the initial content:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default' 
        value='This is initial content'
      />
    </div>
  );
}

export default App;
```

### Set Value with State Variable

Manage the textarea value with React state for dynamic updates:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [textValue, setTextValue] = useState('Default comment text');

  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default' 
        value={textValue}
      />
    </div>
  );
}

export default App;
```

### Get Value Programmatically

Retrieve the textarea value when needed (e.g., on button click):

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [textValue, setTextValue] = useState('Default comment');

  const onButtonClick = () => {
    console.log('TextArea value:', textValue);
    // Use the value for form submission, API call, etc.
  };

  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default' 
        value={textValue}
      />
      <button onClick={onButtonClick}>Get Value</button>
    </div>
  );
}

export default App;
```

### Detect Value Changes

Use the `input` event for real-time value change detection or the `change` event for when focus is lost:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { InputEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';
import './App.css';

function App() {
  const handleInput = (args: InputEventArgs) => {
    console.log('Current value (real-time):', args.value);
  };

  const handleChange = (args) => {
    console.log('Value changed (on blur):', args.value);
  };

  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default'
        input={handleInput}
        change={handleChange}
      />
    </div>
  );
}

export default App;
```

### State Update on Change

Automatically update state when the textarea value changes:

```typescript
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import type { ChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import * as React from 'react';
import './App.css';

function App() {
  const [textValue, setTextValue] = useState('');

  const handleChange = (args: ChangedEventArgs) => {
    setTextValue(args.value || '');
  };

  return (
    <div className='wrap'>
      <TextAreaComponent 
        id='default'
        value={textValue}
        change={handleChange}
      />
      <p>Current length: {textValue.length}</p>
    </div>
  );
}

export default App;
```

## Next Steps

- Configure floating labels for better UX
- Add form validation with FormValidator
- Set maximum character limits
- Customize styling and appearance
- Implement resize behavior
- Add adornments for additional functionality
