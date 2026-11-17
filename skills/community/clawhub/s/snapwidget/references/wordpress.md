<!-- From https://snapwidget.com/docs/install/wordpress. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to my WordPress website?

> Add your SnapWidget Instagram widget to a WordPress page, post, sidebar or footer with the Custom HTML block.

Paste your SnapWidget code into a **Custom HTML** block where you want the widget to show. The same steps work for Facebook, X, TikTok and YouTube widgets.

> [!NOTE]
>
> On a self-hosted WordPress site, you need the Administrator or Editor role. On a WordPress multisite network, only a Super Admin can add the code. On WordPress.com, you need a paid plan with [hosting features activated](https://wordpress.com/support/code/). On other plans, WordPress.com removes the code when you save.

### In SnapWidget

1. [Create your widget](https://snapwidget.com/docs/getting-started/create-an-instagram-widget.md), or open an existing widget from your [dashboard](https://snapwidget.com/dashboard).
2. Click **Install Widget**.
3. In the **Install Widget** window, click **Copy Code**.

### In WordPress

1. In your WordPress dashboard, click **Pages** or **Posts**. Open the page or post where you want the widget.
2. Click the **Block Inserter** (**+**) at the place where you want the widget. Search for "Custom HTML" and select **Custom HTML**. You can also type `/html` in an empty line.
3. Click **Edit HTML**. Paste your code and click **Update**. In WordPress versions before 7.0, paste the code straight into the block.
4. Save or publish the page.

### Add the widget to a sidebar or footer

* **Classic theme:** go to **Appearance** > **Widgets**. Open the widget area, click **+** and add a **Custom HTML** block. Paste your code and click **Update**.
* **Block theme:** go to **Appearance** > **Editor** > **Patterns**. Under **Template Parts**, open the part you want, for example **Footer**, and click the pencil icon. Add a **Custom HTML** block, paste your code and click **Save**.

### Check your widget

Open the page on your live site. The widget shows your latest Instagram posts. If you see a link or an empty space where the widget should be, see [Why does WordPress display a link instead of the widget?](https://snapwidget.com/docs/troubleshooting/wordpress-shows-a-link.md)


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
