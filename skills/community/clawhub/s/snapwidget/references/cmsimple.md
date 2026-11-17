<!-- From https://snapwidget.com/docs/install/cmsimple. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to my CMSimple website?

> Add your SnapWidget Instagram widget to a CMSimple page with the Source code button of the TinyMCE editor.

Paste your SnapWidget code into a CMSimple page with the **Source code** view of the editor. The same steps work for Facebook, X, TikTok and YouTube widgets.

### In SnapWidget

1. [Create your widget](https://snapwidget.com/docs/getting-started/create-an-instagram-widget.md), or open an existing widget from your [dashboard](https://snapwidget.com/dashboard).
2. Click **Install Widget**.
3. In the **Install Widget** window, click **Copy Code**.

### In CMSimple

1. Log in to CMSimple and click **Pages**.

2. Click the **»** arrows next to the page where you want the widget.

   ![The page list with the arrows next to each page](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/cmsimple/7.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=6e152767a3a761d4f83a485f4f9cbbf6)

3. In the editor toolbar, click **Source code**.

   ![The Source code button](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/cmsimple/9.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=a6e89ed42a29ee5f4cc870c9e3477a51)

4. Paste your code where you want the widget to show, and click **Ok**.

   ![The Source code window with the widget code](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/cmsimple/11.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=3246308042a505cc3e4ea9ab6ab24647)

5. Click the save icon in the editor toolbar.

> [!TIP]
>
> The editor removes `<link>` lines. If your widget uses the **Lightbox** or **Shoppable (Lightbox)** photo link, add the lightbox stylesheet to your template. Go to **Settings** > **Template** and paste this line just before `</head>`, then click **Save**:
>
> ```html theme={null}
> <link rel="stylesheet" href="https://snapwidget.com/stylesheets/snapwidget-lightbox.css" />
> ```

### Check your widget

Click **View mode** to see the page as your visitors see it. The widget shows your latest Instagram posts.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
