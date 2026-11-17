<!-- From https://snapwidget.com/docs/install/grav. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to my Grav website?

> Add your SnapWidget Instagram widget to a Grav page. First turn off the GFM Tag Filter, which blocks iframes and scripts.

Paste your SnapWidget code into the content of a Grav page. In Grav 2, the **GFM Tag Filter** setting shows `<iframe>` and `<script>` tags as plain text, so turn it off first. The same steps work for Facebook, X, TikTok and YouTube widgets.

### In SnapWidget

1. [Create your widget](https://snapwidget.com/docs/getting-started/create-an-instagram-widget.md), or open an existing widget from your [dashboard](https://snapwidget.com/dashboard).
2. Click **Install Widget**.
3. In the **Install Widget** window, click **Copy Code**.

### In Grav

1. In the Grav admin, go to **Configuration** > **System**. On the **Markdown** tab, turn off **GFM Tag Filter** and click **Save**.
2. Click **Pages** and open the page where you want the widget.
3. On the **Content** tab, paste your code where you want the widget to show.
4. Click **Save**. Grav can show a warning about possible XSS issues in the content. The warning is about the `<script>` and `<iframe>` tags in the code, and it does not stop the save.

### Check your widget

Open the page on your live site. The widget shows your latest Instagram posts. If you see the code as text, check that **GFM Tag Filter** is off.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
