<!-- From https://snapwidget.com/docs/install/mijnwebwinkel. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# How do I add an Instagram feed to my Mijnwebwinkel webshop?

> Add your SnapWidget Instagram widget to a Mijnwebwinkel webshop with Google Tag Manager. You need Mijnwebwinkel PRO or higher.

Mijnwebwinkel does not let you paste HTML code into a page. You add the widget with Google Tag Manager instead. A tag in Google Tag Manager replaces a short text on your page, `[instagram-feed]`, with your widget. The same steps work for Facebook, X, TikTok and YouTube widgets.

> [!NOTE]
>
> Google Tag Manager is available from the Mijnwebwinkel PRO plan. Mijnwebwinkel support does not help with custom tags.

### In SnapWidget

1. [Create your widget](https://snapwidget.com/docs/getting-started/create-an-instagram-widget.md), or open an existing widget from your [dashboard](https://snapwidget.com/dashboard).
2. Click **Install Widget**.
3. In the **Install Widget** window, click **Copy Code**.

### Connect Google Tag Manager to your webshop

1. Go to Google Tag Manager and sign in with your Google account. Create an account and a container. For the target platform, choose **Web**. You do not have to add the code that Google shows. Mijnwebwinkel adds it for you.
2. In your Mijnwebwinkel admin, go to **Marketing** > **Google services** and open the **Google Tag Manager** tab.
3. Click **Connect with Google** and choose your Google account.
4. Turn on **Use Google Tag Manager**, select your container and click **Save**.

   ![The Google Tag Manager tab in Google services](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/mijnwebwinkel/8.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=95162291633c378f4efcfada95f11c47)

### Create the tag in Google Tag Manager

1. In Google Tag Manager, open the container that you connected to your webshop. Click **Tags**, then **New**.

2. Type a name for the tag, for example "SnapWidget". Click **Tag Configuration** and choose **Custom HTML**.

   ![The Custom HTML tag type](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/mijnwebwinkel/13.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=8f118443817131acf9e9e61e3229ecc5)

3. Paste this code into the **HTML** field:

   ```html theme={null}
   <script src="https://snapwidget.com/js/snapwidget.js"></script>
   <script>
     var iframe = 'PASTE-YOUR-IFRAME-HERE';
     var elements = document.getElementsByTagName("p");
     [].forEach.call(elements, function (element) {
       if (element.textContent === "[instagram-feed]") {
         var iframeDiv = document.createElement("div");
         iframeDiv.innerHTML = iframe;
         element.parentNode.replaceChild(iframeDiv, element);
       }
     });
   </script>
   ```

4. In the SnapWidget code that you copied, find the line that starts with `<iframe` and ends with `</iframe>`. Copy only that line. In the HTML field, replace `PASTE-YOUR-IFRAME-HERE` with it. Keep the single quotes around it. The iframe code must stay on one line and must not contain a single quote (`'`).

5. If your widget uses **Lightbox** or **Shoppable (Lightbox)** as **Photo Link**, your SnapWidget code has two more lines: one with `snapwidget-lightbox.css` and one with `snapwidget-lightbox.js`. Copy both lines and paste them at the top of the HTML field.

6. Click **Save**. Google Tag Manager tells you that the tag has no trigger. Click **Add Trigger** and choose **All Pages**.

   ![The All Pages trigger](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/mijnwebwinkel/20.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=2e954b3d68c7cb9eb6fe5f4e4ab99c62)

7. Click **Save**. Then click **Submit** and **Publish**.

### Place the widget on your webshop page

1. In your Mijnwebwinkel admin, go to **Content** > **Pages** and open the page where you want the widget.
2. In the text of the page, type `[instagram-feed]` on a line of its own. Do not make the text bold. Press **Enter** to end the line, not **Shift**+**Enter**.
3. Click **Save**.

To add a second widget, create a second tag with its own text, for example `[instagram-grid]`. Use that text in the `if` line of the tag and on your page.

### Check your widget

Open the page on your webshop. The widget shows in place of `[instagram-feed]`. If you still see the old page, open it in a private browser window or clear your browser cache.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
