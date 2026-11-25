# SnapWidget code in a JavaScript framework

The HTML code from `snapwidget embed <widget_id> --format html` (the MCP tool `get_embed_code`) has two parts:

- one or more `<script src="https://snapwidget.com/js/...">` tags (a popup or banner widget has a small inline script that loads one), and sometimes a `<link rel="stylesheet">`;
- the widget itself: a `<div class="snapwidget-embed">` (an older code has an `<iframe class="snapwidget-widget">`), or a `<div>` for a popup or banner widget.

A framework that renders the page with JavaScript does not run a `<script>` tag inside a component. Load each script once per page as shown here, and render the div or iframe as it is.

## React

`snapwidget embed <widget_id> --format react` gives a component that loads the scripts in `useEffect`. Save it and render it.

Or install the package `@snapwidget/react` and render `<SnapWidget widgetId="<widget_id>" />`. A review widget takes `reviewsId` in place of `widgetId`. When the HTML code has `snapwidget-lightbox` lines, add the `lightbox` prop. The package is for feed, grid and review widgets, not for popup and banner widgets.

On a page that the server renders (Next.js, Base44), load the script in `useEffect`, or with `next/script` in the same component as the div. A script tag in the `<head>`, or `next/script` in the root layout, runs before React is ready: React reports a hydration error, and the widget can start twice. In a site that renders in the browser only (a Vite app), a script tag in the `<head>` of `index.html` is also correct.

With only the MCP tools, make the same component from the HTML code:

```jsx
'use client';

import { useEffect } from 'react';

const SCRIPTS = ['https://snapwidget.com/js/snapwidget-embed.js']; // each src from the HTML code

export default function SnapWidget() {
  useEffect(() => {
    for (const src of SCRIPTS) {
      if (document.querySelector(`script[src="${src}"]`)) continue;
      const script = document.createElement('script');
      script.src = src;
      document.body.appendChild(script);
    }
  }, []);

  return (
    <>
      {/* the div from the HTML code, as JSX */}
    </>
  );
}
```

## Next.js

`snapwidget embed <widget_id> --format next` gives a component that loads the scripts with `next/script`. It works in the App Router and the Pages Router. The package `@snapwidget/react` works in Next.js too.

With only the MCP tools, make the same component from the HTML code:

```jsx
import Script from 'next/script';

export default function SnapWidget() {
  return (
    <>
      <Script src="https://snapwidget.com/js/snapwidget-embed.js" strategy="afterInteractive" />
      {/* the div from the HTML code, as JSX */}
    </>
  );
}
```

## The div as JSX

In React and Next.js, change the div's attributes: `class` becomes `className`, and `style` becomes an object, such as `style={{ aspectRatio: '765/510' }}`. On an older code with an iframe, `frameborder` becomes `frameBorder` too, and leave out `allowtransparency`.

The small inline script of a popup or banner widget has a `src` and an `id`. Load that `src`, and give the script that `id`: `script.id = id` in React, `<Script id="..." src="..." strategy="afterInteractive" />` in Next.js.

## Vue

Vue templates drop `<script>` tags. Put the div in the template and load each script once, in `onMounted`:

```vue
<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  const src = 'https://snapwidget.com/js/snapwidget-embed.js' // each src from the HTML code
  if (!document.querySelector(`script[src="${src}"]`)) {
    const script = document.createElement('script')
    script.src = src
    document.body.appendChild(script)
  }
})
</script>

<template>
  <!-- the div from the HTML code -->
</template>
```

Or add the `<script>` tags to `index.html` and keep only the div in the component.

## Nuxt

Load the scripts with `useHead` and put the div in the template:

```vue
<script setup>
useHead({ script: [{ src: 'https://snapwidget.com/js/snapwidget-embed.js' }] })
</script>
```

## Svelte and SvelteKit

Put the scripts in `<svelte:head>` and the div in the markup:

```svelte
<svelte:head>
  <script src="https://snapwidget.com/js/snapwidget-embed.js"></script>
</svelte:head>

<!-- the div from the HTML code -->
```

## Astro

Astro bundles `<script>` tags unless they have `is:inline`. Add `is:inline` to each script tag of the HTML code:

```astro
<script is:inline src="https://snapwidget.com/js/snapwidget-embed.js"></script>
<!-- the div from the HTML code -->
```

## Popup and banner widgets

A popup or banner widget starts once, when the page loads. In a React, Next.js, Vue, Nuxt, Svelte or Astro site, put its code in the root layout (in Next.js, `app/layout.tsx`), so it starts when the site loads, as on any other site. In a page component, it does not start again when the visitor leaves the page and comes back.

## Size

The `style` of the div has the size of the widget and keeps its space on the page while the widget loads. Keep the div's `style` and `class` as they are. The widget takes the width of the element around it: give that element a width, and to make the widget narrower, give it a `max-width`.
