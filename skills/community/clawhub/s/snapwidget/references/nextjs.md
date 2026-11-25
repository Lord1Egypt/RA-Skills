<!-- From https://snapwidget.com/docs/install/nextjs. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to a Next.js site?

> Add your SnapWidget Instagram widget to a Next.js site with the @snapwidget/react package. It works in the App Router and the Pages Router.

A `<script>` tag inside a React component does not run, so the SnapWidget code does not work when you paste it into a page. Use the `@snapwidget/react` package, which loads the script for you. You can use it in a Server Component. The same steps work for Facebook, X, TikTok, YouTube and review widgets.

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

### In your Next.js project

1. Install the package:

   ```bash theme={null}
   npm install @snapwidget/react
   ```

2. Add the widget to the page where you want it to show, for example `app/page.js`:

   ```jsx theme={null}
   import { SnapWidget } from "@snapwidget/react"

   export default function Home() {
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

Load the script with `next/script` and add the widget's element:

```jsx theme={null}
import Script from "next/script"

export default function Home() {
  return (
    <>
      <div className="snapwidget-embed" data-widget-id="YOUR_WIDGET_ID" />
      <Script src="https://snapwidget.com/js/snapwidget-embed.js" />
    </>
  )
}
```

For a review widget, use `data-reviews-id` in place of `data-widget-id`.

If your code has lines with `snapwidget-lightbox`, your posts open in a pop-up. Use the package for that widget: it loads the pop-up files for you.

### Ask your AI coding tool

Paste this prompt into Claude Code, Cursor or another AI coding tool. Put your widget ID in it first.

```text wrap theme={null}
Add my SnapWidget Instagram feed to this Next.js site.
Install the npm package @snapwidget/react.
Render <SnapWidget widgetId="YOUR_WIDGET_ID" /> (import { SnapWidget } from "@snapwidget/react") on the home page, in its own section with a full-width container.
Do not use an iframe and do not add a script tag.
```

### Check your widget

Open the page in your browser. The widget shows your latest Instagram posts.

If the widget is too narrow or too wide, give the element around the widget a width, for example `width: 100%`.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
