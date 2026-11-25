<!-- From https://snapwidget.com/docs/install/react. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to a React site?

> Add your SnapWidget Instagram widget to a React site with the @snapwidget/react package, or with one script tag and one div.

A `<script>` tag inside a React component does not run, so the SnapWidget code does not work when you paste it into a component. Use the `@snapwidget/react` package, which loads the script for you. The same steps work for Facebook, X, TikTok, YouTube and review widgets.

### In SnapWidget

1. [Create your widget](https://snapwidget.com/docs/getting-started/create-an-instagram-widget.md), or open an existing widget from your [dashboard](https://snapwidget.com/dashboard).
2. Click **Install Widget**.
3. In the **Install Widget** window, click **Copy Code**.

### Find your widget ID

Look at the code that you copied. Your widget ID is the value of `data-widget-id`. If your code has an `<iframe>`, your widget ID is the part of the address after `/embed/`.

For a review widget, your widget ID is the value of `data-reviews-id`, or the part of the address after `/embed/reviews/`.

> [!NOTE]
>
> These steps are for feed, grid and review widgets. They are not for popup and banner widgets.

### In your React project

1. Install the package:

   ```bash theme={null}
   npm install @snapwidget/react
   ```

2. Add the widget to the component where you want it to show:

   ```jsx theme={null}
   import { SnapWidget } from "@snapwidget/react"

   export default function InstagramFeed() {
     return <SnapWidget widgetId="YOUR_WIDGET_ID" />
   }
   ```

For a review widget, use `reviewsId` in place of `widgetId`:

```jsx theme={null}
<SnapWidget reviewsId="YOUR_WIDGET_ID" />
```

If your code has lines with `snapwidget-lightbox`, your posts open in a pop-up. Add `lightbox`:

```jsx theme={null}
<SnapWidget widgetId="YOUR_WIDGET_ID" lightbox />
```

The `<div>` in your code can have a `style`, for example `style="aspect-ratio:750/500"`. It gives the widget its size and keeps its space on the page while the widget loads. To keep it, pass the same values as a React style:

```jsx theme={null}
<SnapWidget widgetId="YOUR_WIDGET_ID" style={{ aspectRatio: "750/500" }} />
```

### Without the package

1. Add the script to the `<head>` of `index.html`:

   ```html theme={null}
   <script src="https://snapwidget.com/js/snapwidget-embed.js" async></script>
   ```

2. Add this element to the component where you want the widget to show:

   ```jsx theme={null}
   <div className="snapwidget-embed" data-widget-id="YOUR_WIDGET_ID" />
   ```

For a review widget, use `data-reviews-id` in place of `data-widget-id`.

If your code has lines with `snapwidget-lightbox`, your posts open in a pop-up. Add these lines to the `<head>` of `index.html` too:

```html theme={null}
<link rel="stylesheet" href="https://snapwidget.com/stylesheets/snapwidget-lightbox.css" />
<script src="https://snapwidget.com/js/snapwidget-lightbox.js"></script>
```

### Ask your AI coding tool

Paste this prompt into Claude Code, Cursor or another AI coding tool. Put your widget ID in it first.

```text wrap theme={null}
Add my SnapWidget Instagram feed to this React site.
Install the npm package @snapwidget/react.
Render <SnapWidget widgetId="YOUR_WIDGET_ID" /> (import { SnapWidget } from "@snapwidget/react") on the home page, in its own section with a full-width container.
Do not use an iframe and do not add a script tag.
```

### Check your widget

Open the page in your browser. The widget shows your latest Instagram posts.

If the widget is too narrow or too wide, give the element around the widget a width, for example `width: 100%`.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
