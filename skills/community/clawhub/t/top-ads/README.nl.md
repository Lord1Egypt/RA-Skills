# Denote Top Ads

Vind populaire, snel stijgende en pas ontdekte advertenties voor games en hulpprogramma’s en kies ideeën voor je volgende campagne om gebruikers te werven.

[EN](README.md) · [ZH](README.zh.md) · [JA](README.ja.md) · [KO](README.ko.md) · [ES](README.es.md) · NL · [DE](README.de.md) · [FR](README.fr.md)

Denote verzamelt en ververst dagelijks advertentiegegevens voor games en hulpprogramma’s. Elke verzamelronde omvat meer dan 60 miljoen advertentierecords. De ranglijsten worden één keer per week samengesteld. Met een gratis account krijg je drie ranglijsten voor games of apps over de afgelopen volledige week, met maximaal tien advertenties per lijst. [Bekijk Denote Top Ads](https://denote.net/top-ads).

| Gratis ranglijst | Wat je ontdekt |
| --- | --- |
| Populaire advertenties | Welke advertenties vorige week de meeste aandacht trokken. |
| Snelste stijgers | Welke advertenties het meest aan populariteit wonnen ten opzichte van de week ervoor. |
| Nieuwe advertenties | Welke advertenties voor het eerst opdoken, gerangschikt naar hun vroege populariteit. |

## Je eerste weekoverzicht ophalen

Voer deze opdracht uit in je OpenClaw-werkruimte. Je hebt Python 3 nodig.

```sh
git clone https://github.com/denote-developer/denote-top-ads.git skills/denote-top-ads
```

1. Open een nieuwe sessie en vraag: ‘Welke advertenties kan ik met Denote ontdekken?’
2. [Maak een gratis Denote-account aan](https://denote.net/user/register). Heb je al een account? Log dan in. Maak een Denote-API-sleutel aan met de machtiging `top_ads:read` of voeg die toe aan een bestaande sleutel.
3. Sla de sleutel in de beveiligde instellingen van je agent op als `DENOTE_API_KEY`. Vraag daarna: ‘Laat me de populairste appadvertenties van vorige week zien.’ Je krijgt alle drie de lijsten. Zonder categorie zie je advertenties voor games.

De chat toont de eerste drie advertenties per lijst, één per regel, met een medialink en looptijd. Populaire en nieuwe advertenties tonen de totale weekscore. Snelle stijgers tonen de scoretoename en het groeipercentage. Het lokale rapport onderaan het antwoord bevat alle resultaten. Open een kaart voor de video, het overzicht, de trend, gerelateerde advertenties en de doelgroep. De detailknop opent de juiste ranglijst in Denote, ook als gegevens ontbreken.

## Een advertentie nader bekijken

Vraag bijvoorbeeld: ‘Open nummer twee van de snelste stijgers.’ Met Top Ads Pro of Business kun je beschikbare gegevens over de prestaties en het publiek bekijken. De drie wekelijkse ranglijsten zijn gratis.

## Schermafbeeldingen

[![Open de drie weekranglijsten via het menu aan de linkerkant.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/top-ads-navigation.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/top-ads-navigation.jpg)

*Open de drie weekranglijsten via het menu aan de linkerkant.*

[![Populaire gameadvertenties van 9 tot en met 15 november 2026, gerangschikt op weekpopulariteit.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/trending-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/trending-ads.jpg)

*Populaire gameadvertenties van 9 tot en met 15 november 2026, gerangschikt op weekpopulariteit.*

[![Gameadvertenties die het meest aan populariteit wonnen ten opzichte van de week ervoor.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/rising-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/rising-ads.jpg)

*Gameadvertenties die het meest aan populariteit wonnen ten opzichte van de week ervoor.*

[![Nieuw ontdekte gameadvertenties, gerangschikt naar hun vroege populariteit.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/new-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/new-ads.jpg)

*Nieuw ontdekte gameadvertenties, gerangschikt naar hun vroege populariteit.*

[![Overzicht van de Vita Mahjong-advertentie, met het advertentieformaat en het geschatte aantal vertoningen.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/overview.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/overview.jpg)

*Overzicht van de Vita Mahjong-advertentie, met het advertentieformaat en het geschatte aantal vertoningen.*

[![De dagelijkse score van de Vita Mahjong-advertentie vergeleken met de referentielijnen.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/data-trend.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/data-trend.jpg)

*De dagelijkse score van de Vita Mahjong-advertentie vergeleken met de referentielijnen.*

[![Advertenties met hetzelfde materiaal, met de adverteerders en de looptijd.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/related-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/related-ads.jpg)

*Advertenties met hetzelfde materiaal, met de adverteerders en de looptijd.*

[![Het bereik van Vita Mahjong uitgesplitst naar land, leeftijd en geslacht.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/audience.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/audience.jpg)

*Het bereik van Vita Mahjong uitgesplitst naar land, leeftijd en geslacht.*
