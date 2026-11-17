<!-- From https://snapwidget.com/docs/install/membervault. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram widget to my MemberVault website?

> Add your SnapWidget Instagram widget to a MemberVault page or lesson with the source code editor.

Paste your SnapWidget code into the source code of a MemberVault page or lesson. The same steps work for Facebook, X, TikTok and YouTube widgets.

### In SnapWidget

1. [Create your widget](https://snapwidget.com/docs/getting-started/create-an-instagram-widget.md), or open an existing widget from your [dashboard](https://snapwidget.com/dashboard).
2. Click **Install Widget**.
3. In the **Install Widget** window, click **Copy Code**.

### In MemberVault

1. Open the page or lesson where you want the widget. For a page, go to **Content** > **Pages** and click the edit icon next to the page.
2. In the toolbar of the text editor, click the **Source code** button (**\<>**).
3. Paste your code and click **Save**.
4. Click **Save** to save the page or lesson.

> [!TIP]
>
> If your widget uses **Lightbox** as **Photo Link** and the lightbox does not open, the editor may have removed the lightbox stylesheet from your code. Go to **Settings** > **General** > **Advanced Settings**. Add this line to **Custom CSS** and click **Save**:
>
> ```css theme={null}
> @import url('https://snapwidget.com/stylesheets/snapwidget-lightbox.css');
> ```

### Check your widget

Open the page or lesson in preview mode, or as a member. The widget shows your latest Instagram posts.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
