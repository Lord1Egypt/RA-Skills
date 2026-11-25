<!-- From https://snapwidget.com/docs/install/lovable. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to my Lovable site?

> Add your SnapWidget Instagram widget to a site made with Lovable: paste one prompt into the chat.

Lovable writes the code of your site for you. Give it your widget ID and one prompt, and it adds the widget. The same steps work for Facebook, X, TikTok, YouTube and review widgets.

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

### In Lovable

1. Open your project in Lovable.

2. Paste this prompt into the Lovable chat. Put your widget ID in it first.

   ```text wrap theme={null}
   Add my SnapWidget Instagram feed to the home page, in its own section with a full-width container.
   At the place of the feed, render this element, with no children:
   <div class="snapwidget-embed" data-widget-id="YOUR_WIDGET_ID"></div>
   In the same component, add the script https://snapwidget.com/js/snapwidget-embed.js to document.head inside a useEffect, one time only: skip it if a script with that src is already on the page.
   Do not add the script tag to the <head> of the page. Do not use an iframe.
   ```

3. For a review widget, change two things in the prompt: `data-widget-id` to `data-reviews-id`, and "Instagram feed" to "reviews".

4. If the `<div>` in your code has a `style`, add the same `style` to the `<div>` in the prompt. It has the size of your widget.

5. If your code has lines with `snapwidget-lightbox`, your posts open in a pop-up. Add this line to the end of the prompt:

   ```text wrap theme={null}
   Also add this stylesheet and this script to document.head in the same useEffect, one time only: https://snapwidget.com/stylesheets/snapwidget-lightbox.css and https://snapwidget.com/js/snapwidget-lightbox.js
   ```

6. Publish your site.

### Check your widget

Open the page in your browser. The widget shows your latest Instagram posts.

If the widget is too narrow or too wide, give the element around the widget a width, for example `width: 100%`.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
