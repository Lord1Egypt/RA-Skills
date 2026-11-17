# Мобильная интеграция SmartCaptcha: общий подход через WebView

Читайте этот файл перед любой мобильной интеграцией (Android, iOS, Flutter): он объясняет общую архитектуру — капча живет в HTML-странице внутри WebView, а токен передается в нативный код через мост. Платформенные детали — в [mobile-android.md](mobile-android.md), [mobile-ios.md](mobile-ios.md), [mobile-flutter.md](mobile-flutter.md).

## Архитектура

Нативного SDK у SmartCaptcha нет. Капча встраивается в приложения Android и iOS через **WebView** — компонент, отображающий веб-страницы внутри приложения (мини-браузер). Схема:

1. Приложение загружает в WebView URL HTML-страницы с кодом капчи, передавая `sitekey` (ключ клиента) query-параметром.
2. Страница отрисовывает виджет расширенным методом (`window.smartCaptcha.render`, см. [widget-advanced.md](widget-advanced.md)) и подписывается на события через `subscribe`.
3. Когда сервис обработал попытку пользователя (событие `success`), страница передает токен в нативный код через мост: JavaScript Interface на Android или `webkit.messageHandlers` на iOS.
4. Приложение отправляет токен на **свой бэкенд**, который проверяет его POST-запросом на `https://smartcaptcha.yandexcloud.net/validate` (см. [server-validation.md](server-validation.md)). Ключ сервера в приложение попадать не должен.

## HTML-страница: своя или готовая

**Своя страница.** Разместите HTML-страницу с кодом капчи на вашем сервере и загружайте ее URL в WebView. Готовый адаптированный шаблон — [../templates/webview-page.html](../templates/webview-page.html). Своя страница нужна, если вы хотите переименовать методы моста или добавить свою логику.

**Готовая страница Yandex Cloud.** Можно не хостить страницу самостоятельно, а использовать размещенную на сервере Yandex Cloud:

```
smartcaptcha.yandexcloud.net
```

Страница принимает query-параметры и передает их в `render()`:

| Параметр | Назначение |
|---|---|
| `sitekey` | Ключ клиента (обязателен) |
| `invisible=true` | Невидимый режим работы капчи |
| `test=true` | Тестовый режим — задание показывается всегда (только для отладки) |
| `hideShield=true` | Скрыть блок с уведомлением об обработке данных |

Параметры `test`, `invisible`, `hideShield` приводятся к `boolean`; параметр `webview` страница всегда выставляет в `true` сама. Пример URL для WebView:

```
https://smartcaptcha.yandexcloud.net/?sitekey=<ключ_клиента>&invisible=true
```

> **Важно.** Если вы скрываете блок с уведомлением об обработке данных (`hideShield`), вы обязаны сообщить пользователям иным способом, что SmartCaptcha обрабатывает их данные.

## Параметр webview

В параметрах `render()` есть флаг `webview: boolean` — запуск капчи в WebView. Он повышает точность оценки пользователей при добавлении капчи в мобильные приложения через WebView. На мобильной странице всегда выставляйте `webview: true` (шаблон и готовая страница делают это автоматически).

## JavaScript Interface: мост страница → нативный код

JavaScript Interface — объект, который ОС Android передает в WebView; фронтенд обращается к нему, чтобы отправлять сообщения в нативный код через функции обратного вызова. В туториалах объект регистрируется под именем **`NativeClient`**. Структура:

| Метод | Обязательность | Когда вызывается |
|---|---|---|
| `onGetToken(token: String)` | Обязательный | Сервис обработал попытку пользователя — страница передает токен прохождения капчи |
| `onChallengeVisible()` | Только для невидимой капчи | Капча показала пользователю задание — пора показать скрытый WebView |
| `onChallengeHidden()` | Только для невидимой капчи | Пользователь закрыл («смахнул») окно с заданием — восстановить его нельзя, верните пользователя на предыдущий экран |

При создании класса на Android методы помечаются аннотацией `@JavascriptInterface`. Если вы хостите собственную страницу, названия методов можно изменить — но синхронно на странице и в нативном классе.

На iOS та же страница отправляет сообщения через `window.webkit.messageHandlers.NativeClient.postMessage({method, data})` — шаблон проверяет наличие обоих мостов и работает на обеих платформах.

## Чеклист интеграции

1. Создайте капчу и на вкладке **Обзор** получите ключи (подробно — [keys.md](keys.md), [captcha-management.md](captcha-management.md)):
   * **Ключ клиента** — для загрузки страницы с капчей;
   * **Ключ сервера** — для проверки токена на бэкенде (в приложение не встраивать).
2. Разместите [шаблон страницы](../templates/webview-page.html) на своем сервере или используйте `smartcaptcha.yandexcloud.net`.
3. В приложении загрузите в WebView URL страницы с query-параметром `sitekey=<ключ_клиента>` (плюс `invisible=true` для невидимой капчи).
4. Зарегистрируйте мост `NativeClient` и получите токен в `onGetToken`.
5. Отправьте токен на бэкенд и проверьте через `/validate` — токен одноразовый, живет 5 минут, поэтому проверяйте сразу.

## См. также

* [mobile-android.md](mobile-android.md) — Android: настройка WebView, обычная и невидимая капча.
* [mobile-ios.md](mobile-ios.md) — iOS: WKWebView.
* [mobile-flutter.md](mobile-flutter.md) — Flutter: webview_flutter.
* [../templates/webview-page.html](../templates/webview-page.html) — готовая страница для WebView.
* [../workflows/integrate-mobile.md](../workflows/integrate-mobile.md) — пошаговый сценарий мобильной интеграции.
* [server-validation.md](server-validation.md) — проверка токена на бэкенде.
* [invisible-captcha.md](invisible-captcha.md) — как работает невидимая капча.
* Официальная документация: [HTML-страница для мобильных приложений](https://yandex.cloud/ru/docs/tutorials/security/mobile-app/website), [объект JavaScript Interface](https://yandex.cloud/ru/docs/smartcaptcha/concepts/js-interface), [методы виджета](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods).
