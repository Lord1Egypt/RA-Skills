<!-- From https://snapwidget.com/docs/install/vue. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to a Vue site?

> Add your SnapWidget Instagram widget to a Vue site with one script tag in index.html and one div in your component.

Vue removes `<script>` tags from a component's template, so the SnapWidget code does not work when you paste it into a component. Load the script in `index.html` and keep only the widget's element in the component. The same steps work for Facebook, X, TikTok, YouTube and review widgets.

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

### In your Vue project

1. Add the script to the `<head>` of `index.html`:

   ```html theme={null}
   <script src="https://snapwidget.com/js/snapwidget-embed.js" async></script>
   ```

2. Add this element to the template of the component where you want the widget to show:

   ```vue theme={null}
   <template>
     <div class="snapwidget-embed" data-widget-id="YOUR_WIDGET_ID"></div>
   </template>
   ```

If your code has a line that starts with `<div class="snapwidget-embed"`, use that line in place of the `<div>` above. It has the size of your widget.

For a review widget, use `data-reviews-id` in place of `data-widget-id`.

If your code has lines with `snapwidget-lightbox`, your posts open in a pop-up. Add these lines to the `<head>` of `index.html` too:

```html theme={null}
<link rel="stylesheet" href="https://snapwidget.com/stylesheets/snapwidget-lightbox.css" />
<script src="https://snapwidget.com/js/snapwidget-lightbox.js"></script>
```

### Check your widget

Open the page in your browser. The widget shows your latest Instagram posts.

If the widget is too narrow or too wide, give the element around the widget a width, for example `width: 100%`.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
