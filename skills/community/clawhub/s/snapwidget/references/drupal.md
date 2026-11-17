<!-- From https://snapwidget.com/docs/install/drupal. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to my Drupal website?

> Add your SnapWidget Instagram widget to a Drupal page with the Full HTML text format and the CKEditor 5 Source button.

Paste your SnapWidget code into the body of a Drupal page where you want the widget to show. The same steps work for Facebook, X, TikTok and YouTube widgets.

> [!NOTE]
>
> You need the **Full HTML** text format. On a standard Drupal site, only administrators can use it. The **Basic HTML** format removes the `<iframe>` tag when you save.

### In SnapWidget

1. [Create your widget](https://snapwidget.com/docs/getting-started/create-an-instagram-widget.md), or open an existing widget from your [dashboard](https://snapwidget.com/dashboard).
2. Click **Install Widget**.
3. In the **Install Widget** window, click **Copy Code**.

### In Drupal

1. In the admin toolbar, click **Content**. Find the page and click **Edit**.

   ![The content list with the Edit button](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/drupal/12.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=6e236cc47ab369fd7485a498b3ba838a)

2. Under the body field, set **Text format** to **Full HTML**.

3. In the editor toolbar, click **Source**.

4. Paste your code where you want the widget to show.

   ![The body field in Source mode with the Full HTML text format](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/drupal/14.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=15c8a1ac543ae56aa0e6149d9e48887b)

5. Click **Save** while the editor is still in Source mode. If you click **Source** again before you save, the editor can remove the `<script>` line.

### Check your widget

Open the page on your live site. The widget shows your latest Instagram posts.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
