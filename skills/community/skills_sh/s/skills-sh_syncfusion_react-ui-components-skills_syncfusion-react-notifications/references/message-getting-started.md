# Getting Started with Syncfusion React Message

This guide walks through installing, configuring, and rendering your first `MessageComponent` in a React application.

## Prerequisites

- React 16.8+ (hooks support required)
- Node.js 14+
- A Vite or Create React App project

## Installation

Install the Syncfusion notifications package, which includes the Message component:

```bash
npm install @syncfusion/ej2-react-notifications --save
```

## Adding CSS

Import the required stylesheets in `src/App.css`. The `ej2-base` styles provide foundational theme tokens; the notifications styles provide component-specific styling:

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-notifications/styles/tailwind3.css';
```

Then import `App.css` in your entry file:

```tsx
// src/App.tsx
import './App.css';
```

## Basic Usage

Import `MessageComponent` from the notifications package and render it in JSX:

```tsx
import { MessageComponent } from '@syncfusion/ej2-react-notifications';
import './App.css';

function App() {
  return (
    <MessageComponent content="Please read the comments carefully" />
  );
}
export default App;
```

## Content: Prop vs Children

The `content` prop and JSX children are both supported for message text:

```tsx
{/* Using the content prop (string) */}
<MessageComponent content="Your message has been sent successfully" />

{/* Using JSX children (string) */}
<MessageComponent>Your message has been sent successfully</MessageComponent>
```

For rich/templated content, pass a function or JSX element to `content` — see `customization.md` for details.

## Running the Application

Start the Vite development server:

```bash
npm run dev
```

The browser will open with your message displayed immediately. No additional initialization is needed beyond the CSS import and the component tag.

## Setup for TypeScript

To scaffold a TypeScript-enabled React app with Vite:

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @syncfusion/ej2-react-notifications --save
npm run dev
```

## Setup for JavaScript

To scaffold a JavaScript React app with Vite:

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install @syncfusion/ej2-react-notifications --save
npm run dev
```

## Gotchas

- **Missing styles**: If the message appears unstyled, ensure both `ej2-base` and `ej2-react-notifications` CSS files are imported before the component renders.
- **SSR environments**: The component requires a DOM — ensure it only renders client-side in SSR frameworks (Next.js, Remix).
