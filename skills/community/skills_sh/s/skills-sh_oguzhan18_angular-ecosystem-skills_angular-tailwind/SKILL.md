---
name: angular-tailwind
description: "ALWAYS use when working with Angular and Tailwind CSS, Tailwind configuration, utility-first CSS, or styling Angular applications with Tailwind."
metadata:
  version: 4.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular + Tailwind CSS

**Version:** Tailwind CSS 4.x (2025)
**Tags:** Tailwind CSS, Styling, Utility-first, CSS

**References:** [Tailwind CSS](https://tailwindcss.com/docs) • [Angular Tailwind](https://tailwindcss.com/docs/guides/angular)

## API Changes

This section documents recent version-specific API changes.

- NEW: Tailwind CSS v4 — New engine with improved performance [source](https://tailwindcss.com/blog/tailwindcss-v4)

- NEW: @tailwindcss/vite — Native Vite support

- NEW: CSS-first configuration — Configure Tailwind with CSS instead of config file

- NEW: Angular 17+ support — Full compatibility with standalone components

## Best Practices

- Install Tailwind CSS

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

- Configure tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

- Add directives to styles

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- Use Tailwind v4 with Angular

```bash
npm install tailwindcss @tailwindcss/vite
```

```ts
// vite.config.ts
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [tailwindcss()],
});
```

```css
@import "tailwindcss";
```

- Use utility classes in templates

```ts
@Component({
  template: `
    <div class="flex items-center justify-between p-4 bg-white shadow rounded-lg">
      <h1 class="text-2xl font-bold text-gray-800">Title</h1>
      <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        Click
      </button>
    </div>
  `
})
export class CardComponent {}
```

- Use ngClass for conditional classes

```ts
@Component({
  template: `
    <div [ngClass]="isActive ? 'bg-blue-500' : 'bg-gray-200'">
      Content
    </div>
  `
})
export class MyComponent {}
```

- Use class binding

```ts
@Component({
  template: `
    <div [class]="containerClasses">
      Content
    </div>
  `
})
export class MyComponent {
  containerClasses = 'p-4 bg-white rounded-lg shadow';
}
```

- Create custom components with Tailwind

```ts
@Component({
  selector: 'app-button',
  template: `
    <button [class]="buttonClasses">
      <ng-content></ng-content>
    </button>
  `
})
export class ButtonComponent {
  @Input() variant: 'primary' | 'secondary' = 'primary';
  
  get buttonClasses() {
    const base = 'px-4 py-2 rounded font-medium transition';
    const variants = {
      primary: 'bg-blue-500 text-white hover:bg-blue-600',
      secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300'
    };
    return `${base} ${this.variants[this.variant]}`;
  }
}
```

- Use @apply for reusable styles

```css
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600;
  }
  
  .card {
    @apply bg-white rounded-lg shadow p-4;
  }
}
```

- Use theme customization

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          900: '#0c4a6e',
        }
      }
    }
  }
}
```

- Use Dark mode

```js
// tailwind.config.js
module.exports = {
  darkMode: 'class',
}
```

```ts
@Component({
  template: `
    <div class="dark:bg-gray-900 dark:text-white">
      Content
    </div>
  `
})
export class DarkComponent {}
```
