# Denote Top Ads

Encuentra anuncios populares, en ascenso y recién detectados de juegos y aplicaciones de utilidades para elegir creatividades para tu próxima campaña de captación.

[EN](README.md) · [ZH](README.zh.md) · [JA](README.ja.md) · [KO](README.ko.md) · ES · [NL](README.nl.md) · [DE](README.de.md) · [FR](README.fr.md)

Denote recopila y actualiza a diario datos de anuncios de juegos y aplicaciones de utilidades. Cada rastreo abarca más de 60 millones de registros publicitarios. Las clasificaciones se elaboran una vez por semana. Con una cuenta gratuita puedes consultar tres listas de juegos o aplicaciones de la última semana completa, con hasta diez anuncios por lista. [Explorar Denote Top Ads](https://denote.net/top-ads).

| Lista gratuita | Qué te permite descubrir |
| --- | --- |
| Anuncios populares | Los anuncios que más atención recibieron la semana pasada. |
| Anuncios en ascenso | Los que más ganaron en popularidad respecto a la semana anterior. |
| Anuncios nuevos | Los detectados por primera vez durante esa semana, ordenados por su popularidad inicial. |

## Obtén tus primeras tres listas

Ejecuta este comando en tu espacio de trabajo de OpenClaw. Necesitas Python 3.

```sh
git clone https://github.com/denote-developer/denote-top-ads.git skills/denote-top-ads
```

1. Abre una sesión nueva y pregunta «¿Qué anuncios puedo descubrir con Denote?».
2. [Crea una cuenta gratuita de Denote](https://denote.net/user/register). Si ya tienes cuenta, inicia sesión. Crea una clave de API de Denote con el permiso `top_ads:read` o añádelo a una clave existente.
3. Guarda la clave como `DENOTE_API_KEY` en la configuración de secretos de tu agente y pídele «Muéstrame los mejores anuncios de aplicaciones de la semana pasada». Recibirás las tres listas. Si omites la categoría, verás anuncios de juegos.

El chat muestra los tres primeros anuncios de cada lista, uno por fila, con enlace al material y duración. Las listas de populares y nuevos muestran la puntuación semanal total; la de anuncios en ascenso muestra el incremento y la tasa de crecimiento. El informe local al final de la respuesta incluye todos los resultados. Abre una tarjeta para reproducir el vídeo y consultar el resumen, la tendencia, los anuncios relacionados y la audiencia. El botón de detalles abre la lista correspondiente en Denote incluso si faltan datos.

## Consulta un anuncio en detalle

Prueba con «Abre el segundo anuncio en ascenso». Con Top Ads Pro o Business puedes consultar los datos disponibles de rendimiento y audiencia. Las tres listas semanales son gratuitas.

## Capturas de pantalla

[![Accede a las tres clasificaciones semanales desde el menú lateral.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/top-ads-navigation.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/top-ads-navigation.jpg)

*Accede a las tres clasificaciones semanales desde el menú lateral.*

[![Anuncios populares de juegos del 9 al 15 de noviembre de 2026, por popularidad semanal.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/trending-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/trending-ads.jpg)

*Anuncios populares de juegos del 9 al 15 de noviembre de 2026, por popularidad semanal.*

[![Anuncios de juegos que más ganaron en popularidad respecto a la semana anterior.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/rising-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/rising-ads.jpg)

*Anuncios de juegos que más ganaron en popularidad respecto a la semana anterior.*

[![Anuncios de juegos recién detectados, ordenados por su popularidad inicial.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/new-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/new-ads.jpg)

*Anuncios de juegos recién detectados, ordenados por su popularidad inicial.*

[![Resumen de la creatividad de Vita Mahjong, con su formato e impresiones estimadas.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/overview.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/overview.jpg)

*Resumen de la creatividad de Vita Mahjong, con su formato e impresiones estimadas.*

[![Evolución de la puntuación diaria de Vita Mahjong frente a las líneas de referencia.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/data-trend.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/data-trend.jpg)

*Evolución de la puntuación diaria de Vita Mahjong frente a las líneas de referencia.*

[![Anuncios que utilizan la misma creatividad, con sus anunciantes y fechas de difusión.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/related-ads.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/related-ads.jpg)

*Anuncios que utilizan la misma creatividad, con sus anunciantes y fechas de difusión.*

[![Alcance de Vita Mahjong por país, edad y género.](https://raw.githubusercontent.com/denote-developer/denote-top-ads/7836381e21c51723656393ed99380a26215ee954/assets/screenshots/audience.jpg)](https://cdn.denote.net/denote/static/source/denote-top-ads/assets/screenshots/audience.jpg)

*Alcance de Vita Mahjong por país, edad y género.*
