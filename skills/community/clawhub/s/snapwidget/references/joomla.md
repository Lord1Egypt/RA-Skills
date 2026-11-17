<!-- From https://snapwidget.com/docs/install/joomla. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to my Joomla website?

> Add your SnapWidget Instagram widget to a Joomla article with the CodeMirror editor, so the editor does not remove the code.

Paste your SnapWidget code into a Joomla article where you want the widget to show. The default TinyMCE editor removes `<iframe>` and `<script>` tags, so use the CodeMirror editor for this article. The same steps work for Facebook, X, TikTok and YouTube widgets.

> [!NOTE]
>
> You must be a Super User, or your user group must have **No Filtering** in **System** > **Global Configuration** > **Text Filters**. For all other groups, Joomla removes the code when you save.

### In SnapWidget

1. [Create your widget](https://snapwidget.com/docs/getting-started/create-an-instagram-widget.md), or open an existing widget from your [dashboard](https://snapwidget.com/dashboard).
2. Click **Install Widget**.
3. In the **Install Widget** window, click **Copy Code**.

### In Joomla

1. In the Joomla administrator, open the user menu in the top right and click **Edit Account**. On the **Basic Settings** tab, set **Editor** to **Editor - CodeMirror**. Click **Save & Close**.

2. Go to **Content** > **Articles** and open the article.

   ![The Articles item in the Content menu](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/joomla/6.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=3873f5035338729583d28473d0f9e9c2)

3. Paste your code where you want the widget to show.

4. Click **Save & Close**.

> [!WARNING]
>
> If someone later opens this article in TinyMCE and saves it, TinyMCE can remove the code. Always edit this article with CodeMirror.

### Check your widget

Open the article on your live site. The widget shows your latest Instagram posts.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
