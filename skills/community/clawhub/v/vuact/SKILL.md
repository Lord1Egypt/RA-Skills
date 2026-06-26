---
name: vuact
description: >
  Vuact best practices and integration guide. A React↔Vue bridge / interop library
  that lets you use React components in Vue or Vue components in React with full
  two-way interoperability — covering components, events, reactivity, Context, Ref,
  and more. Use this skill whenever the user mentions react-in-vue, vue-in-react,
  react-to-vue, vue-to-react, cross-framework component rendering, or any scenario
  involving mixing React and Vue in the same project.
---

# Vuact

Vuact is a React runtime compatibility layer for Vue 3. It enables seamless usage of the React component ecosystem inside Vue 3 projects, with two-way interoperability between Vue and React for components, events, reactivity, Context, Ref, and more.

**Key value**:
- Seamlessly use React components in Vue apps
- Support bidirectional migration: Vue ↔ React
- Use Vue and React in the same application
- Build cross-stack component libraries in a React-like way

## Quick Start

For the full configuration and initialization flow, see [setup-config.md](references/setup-config.md).

## Core Capabilities

### 1. Component Conversion

Vuact provides two core functions to convert components between Vue and React:

- **r2v (react-to-vue)**: Convert a React component into a Vue component
- **v2r (vue-to-react)**: Convert a Vue component into a React component

Examples:
- [r2v Basics](references/r2v-basic.md)
- [v2r Basics](references/v2r-basic.md)

### 2. Slots and Render Props

Vuact provides a flexible slots and render-props transformation mechanism:

- On the Vue side, you can pass children, element props, or render props to React components via slots
- On the React side, you can pass slots to Vue components via props prefixed with `slot:`

- [r2v Render Props and Slots](references/r2v-render-props.md)
- [v2r Slots](references/v2r-slots.md)

### 3. Events and Props Interop

Vuact automatically transforms props and events between Vue and React:

- Vue `class` → React `className`
- Vue `style` (string or object) → React `style` (object)
- React `className` → Vue `class`
- React `style` (object; auto-add `px` for unitless values) → Vue `style`
- Vue `v-model` update events → React `onUpdate:xxx`

Examples:
- [r2v Event Callbacks](references/r2v-event.md)
- [v2r Event Callbacks](references/v2r-event.md)

### 4. Context Interop

Vuact supports two-way Context passing between Vue and React:

- On the Vue side, you can provide React Context to React components via `provideContext`
- On the React side, you can provide Vue Context to Vue components via `VueContextProvider`
- Context can pass through both frameworks

Examples:
- [r2v React Context](references/r2v-react-context.md)
- [r2v Vue Context](references/r2v-vue-context.md)
- [v2r React Context](references/v2r-react-context.md)
- [v2r Vue Context](references/v2r-vue-context.md)

### 5. Ref Interop

Vuact supports passing refs between Vue and React components:

- On the Vue side, use `ref` to get a React component instance
- On the React side, use `ref` to get a Vue component instance
- For function components, expose methods via `useImperativeHandle`

Examples:
- [r2v Component Ref](references/r2v-ref.md)
- [v2r Component Ref](references/v2r-ref.md)

### 6. Use Vue Hooks in React Components

Vuact lets you use Vue reactivity directly inside React components:

- Create a Vue reactive scope via `useVueEffectScope`
- Use Vue hooks like `ref`, `watch`, `computed`, etc. within that scope
- Combine the reactivity systems from both frameworks

Examples:
- [r2v Vue Hooks](references/r2v-vue-hooks.md)
- [r2v Hybrid Components](references/r2v-hybrid.md)

## Compatibility and Limitations

### Version Compatibility

- **React**: mainly compatible with React 16–18; React 19 support is in progress
- **Vue**: requires Vue >= 3.5
- **Build tools**: ESM-only; requires a modern bundler

### Known Limitations

Because Vuact is essentially based on Vue, some behaviors cannot fully match React:

1. **Concurrent rendering**: Vue renders recursively, so React concurrent rendering cannot be replicated
2. **Commit phase**: Vue mutates the DOM during recursive rendering; there is no explicit commit phase like React
   - `useInsertionEffect` timing differs from React
   - `getSnapshotBeforeUpdate` timing differs from React
3. **Event system**: `@vue/runtime-dom` cannot fully match `react-dom`
   - `react-dom`'s `SyntheticEvent` differs from standard web events
   - `react-dom` applies special handling for some native DOM elements (e.g. `input`, `form`, etc.)

## Full Examples

Load the relevant reference docs to get complete example code and detailed explanations.

### Vue → React (r2v)

- [r2v Basics](references/r2v-basic.md) - The most basic way to use React components from Vue
- [r2v Event Callbacks](references/r2v-event.md) - Event passing between Vue and React components
- [r2v Hybrid Components](references/r2v-hybrid.md) - Mix Vue and React, using capabilities from both frameworks
- [r2v React Context](references/r2v-react-context.md) - Provide React Context to React components from Vue
- [r2v Component Ref](references/r2v-ref.md) - Get React component refs from Vue
- [r2v Render Props and Slots](references/r2v-render-props.md) - Render props and element props usage for React components
- [r2v Vue Context](references/r2v-vue-context.md) - Provide Vue Context to React components from Vue
- [r2v Vue Hooks](references/r2v-vue-hooks.md) - Use Vue hooks inside React components

### React → Vue (v2r)

- [v2r Basics](references/v2r-basic.md) - The most basic way to use Vue components from React
- [v2r Event Callbacks](references/v2r-event.md) - Event passing between React and Vue components
- [v2r React Context](references/v2r-react-context.md) - Provide React Context to Vue components from React
- [v2r Component Ref](references/v2r-ref.md) - Get Vue component refs from React
- [v2r Slots](references/v2r-slots.md) - Pass slots to Vue components from React
- [v2r Vue Context](references/v2r-vue-context.md) - Provide Vue Context to Vue components from React

### Configuration and Initialization

- [setup-config.md](references/setup-config.md) - Full configuration and initialization guide (more complete than the README)
