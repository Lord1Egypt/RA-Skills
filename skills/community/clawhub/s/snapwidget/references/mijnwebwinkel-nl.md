<!-- From https://snapwidget.com/docs/install/mijnwebwinkel-nl. To change it, change the docs and run npm run references. -->

Get the code with `snapwidget embed <widget_id> --format html` (the MCP tool get_embed_code). It is the same code as **Copy Code** in the steps below, so skip the steps in SnapWidget.

# Hoe voeg ik een Instagram feed toe aan mijn Mijnwebwinkel webshop?

> Plaats je SnapWidget Instagram-widget in je Mijnwebwinkel webshop met Google Tag Manager. Je hebt Mijnwebwinkel PRO of hoger nodig.

Mijnwebwinkel laat je geen HTML-code op een pagina plakken. Je plaatst de widget daarom met Google Tag Manager. Een tag in Google Tag Manager vervangt een korte tekst op je pagina, `[instagram-feed]`, door je widget. Dezelfde stappen werken voor Facebook-, X-, TikTok- en YouTube-widgets.

> [!NOTE]
>
> Google Tag Manager is beschikbaar vanaf het Mijnwebwinkel PRO-abonnement. De support van Mijnwebwinkel helpt niet bij het maken van eigen tags.

### In SnapWidget

1. [Maak je widget](https://snapwidget.com/docs/getting-started/create-an-instagram-widget.md), of open een bestaande widget op je [dashboard](https://snapwidget.com/dashboard).
2. Klik op **Install Widget**.
3. Klik in het venster **Install Widget** op **Copy Code**.

### Koppel Google Tag Manager aan je webshop

1. Ga naar Google Tag Manager en log in met je Google-account. Maak een account en een container aan. Kies als doelplatform **Web**. De code die Google toont, hoef je niet te plaatsen. Mijnwebwinkel doet dat voor je.
2. Ga in je beheeromgeving naar **Marketing** > **Google-services** en open het tabblad **Google Tag Manager**.
3. Klik op **Maak verbinding met Google** en kies je Google-account.
4. Zet **Gebruik Google Tag Manager** aan, kies je container en klik op **Opslaan**.

   ![Het tabblad Google Tag Manager bij Google-services](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/mijnwebwinkel-nl/8.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=c51d6474e6137f9fa1f77057e2d3f03f)

### Maak de tag in Google Tag Manager

1. Open in Google Tag Manager de container die je aan je webshop hebt gekoppeld. Klik op **Tags** en daarna op **Nieuw**.

2. Geef de tag een naam, bijvoorbeeld "SnapWidget". Klik op **Tagconfiguratie** en kies **Aangepaste HTML**.

   ![Het tagtype Aangepaste HTML](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/mijnwebwinkel-nl/13.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=06a7f03f14f2fe14e53619f31670f767)

3. Plak deze code in het HTML-veld:

   ```html theme={null}
   <script src="https://snapwidget.com/js/snapwidget.js"></script>
   <script>
     var iframe = 'PLAK-HIER-JE-IFRAME';
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

4. Zoek in de SnapWidget-code die je hebt gekopieerd de regel die begint met `<iframe` en eindigt met `</iframe>`. Kopieer alleen die regel. Vervang in het HTML-veld `PLAK-HIER-JE-IFRAME` door die regel. Laat de enkele aanhalingstekens eromheen staan. De iframe-code moet op één regel blijven en mag geen enkel aanhalingsteken (`'`) bevatten.

5. Gebruikt je widget **Lightbox** of **Shoppable (Lightbox)** als **Photo Link**? Dan heeft je SnapWidget-code twee extra regels: één met `snapwidget-lightbox.css` en één met `snapwidget-lightbox.js`. Kopieer beide regels en plak ze bovenaan in het HTML-veld.

6. Klik op **Opslaan**. Google Tag Manager meldt dat de tag geen trigger heeft. Klik op **Trigger toevoegen** en kies **Alle pagina's**.

   ![De trigger Alle pagina's](https://mintcdn.com/snapwidget/QJTE73Rcy1kqujES/images/install/mijnwebwinkel-nl/20.png?fit=max\&auto=format\&n=QJTE73Rcy1kqujES\&q=85\&s=114033b95695c3f50a379c58142f4622)

7. Klik op **Opslaan**. Klik daarna op **Verzenden** en **Publiceren**.

### Plaats de widget op je webshoppagina

1. Ga in je beheeromgeving naar **Inhoud** > **Pagina's** en open de pagina waar de widget moet komen.
2. Typ in de tekst van de pagina `[instagram-feed]` op een eigen regel. Maak de tekst niet dikgedrukt. Sluit de regel af met **Enter**, niet met **Shift**+**Enter**.
3. Klik op **Opslaan**.

Wil je een tweede widget plaatsen? Maak dan een tweede tag met een eigen tekst, bijvoorbeeld `[instagram-grid]`. Gebruik die tekst in de `if`-regel van de tag en op je pagina.

### Controleer je widget

Open de pagina in je webshop. De widget staat op de plek van `[instagram-feed]`. Zie je nog de oude pagina? Open de pagina dan in een privévenster of leeg de cache van je browser.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
