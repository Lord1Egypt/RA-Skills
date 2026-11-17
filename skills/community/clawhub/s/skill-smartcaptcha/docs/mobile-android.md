# SmartCaptcha в Android-приложении (WebView)

Читайте этот файл при встраивании SmartCaptcha в приложение на Android — обычной или невидимой. Общая архитектура (страница, мост, параметр `webview`) описана в [mobile-webview.md](mobile-webview.md); здесь — только Kotlin-код и порядок действий.

## Перед началом работы

1. Разместите [HTML-страницу](../templates/webview-page.html) на своем сервере или используйте готовую на сервере Yandex Cloud — `smartcaptcha.yandexcloud.net`.
2. Создайте капчу (см. [captcha-management.md](captcha-management.md)).
3. На вкладке **Обзор** капчи получите ключи ([keys.md](keys.md)):
   * **Ключ клиента** — для загрузки страницы с капчей;
   * **Ключ сервера** — для проверки токена на бэкенде.

## Шаг 1. Создайте JavaScript Interface

Класс принимает сообщения от веб-страницы с капчей через функции обратного вызова. Методы помечаются аннотацией `@JavascriptInterface`:

```kotlin
class WebJsInterface {

  @JavascriptInterface
  fun onGetToken(token: String) {
    // Токен прохождения капчи: отправьте его на свой бэкенд.
  }

  // Два метода ниже нужны только для невидимой капчи.
  @JavascriptInterface
  fun onChallengeVisible() {
    // Капча показала задание — покажите WebView.
  }

  @JavascriptInterface
  fun onChallengeHidden() {
    // Пользователь закрыл задание — скройте WebView.
  }
}
```

Для обычной капчи достаточно одного `onGetToken(token: String)` — он вызывается, когда веб-страница возвращает токен прохождения капчи.

## Шаг 2. Настройте WebView

1. Создайте **WebView** и добавьте его на экран.
2. Включите JavaScript и зарегистрируйте JavaScript Interface. Второй параметр `addJavascriptInterface` — имя `NativeClient`: на него страница отправляет сообщения:

   ```kotlin
   settings.javaScriptEnabled = true // Включает выполнение JavaScript.
   addJavascriptInterface(WebJsInterface(), "NativeClient")
   ```

3. Загрузите URL страницы с капчей, добавив query-параметр `sitekey`:

   ```kotlin
   val webView = findViewById<WebView>(R.id.webViewCaptcha)
   webView.loadUrl("URL_страницы_с_капчей?sitekey=<ключ_клиента>")
   ```

## Шаг 3. Получите и проверьте токен

1. Сохраните токен из `onGetToken(token: String)` и отправьте его на свой бэкенд.
2. Бэкенд проверяет токен POST-запросом на `https://smartcaptcha.yandexcloud.net/validate` с параметрами `secret` (ключ сервера), `token` и `ip` в формате `x-www-form-urlencoded`. Ответ — JSON с полями `status` (`ok` — человек, `failed` — робот) и `message`. Готовый код и разбор ошибок — в [server-validation.md](server-validation.md).

> **Важно.** Проверка токена выполняется только на бэкенде: секретный ключ `secret` в Android-приложение попасть не должен.

## Невидимая капча

Отличия от обычной:

1. В классе `WebJsInterface` определите все три метода (см. шаг 1).
2. В URL добавьте параметр `invisible=true` — капча перейдет в невидимый режим:

   ```kotlin
   webView.loadUrl("URL_страницы_с_капчей?sitekey=<ключ_клиента>&invisible=true")
   ```

   На странице после `render()` сразу вызывается `window.smartCaptcha.execute(widgetId)` — проверка запускается при загрузке страницы (так делают шаблон и готовая страница `smartcaptcha.yandexcloud.net`). Значит, момент проверки выбирайте моментом загрузки WebView — например, загружайте страницу по нажатию кнопки отправки формы.
3. Держите **WebView** изначально скрытым (`View.GONE`) — большинство пользователей задание не увидят, а токен придет в `onGetToken` без показа окна.
4. Покажите **WebView** в `onChallengeVisible()` — капча выдала пользователю задание:

   ```kotlin
   val webView = activity.findViewById<WebView>(R.id.webViewCaptcha)
   webView.visibility = View.VISIBLE
   ```

5. Скройте **WebView** в `onChallengeHidden()` — пользователь не прошел задание и свернул его; самостоятельно восстановить капчу не получится, верните пользователя на предыдущий экран:

   ```kotlin
   val webView = activity.findViewById<WebView>(R.id.webViewCaptcha)
   webView.visibility = View.GONE
   ```

**Почему невидимая.** Она требует меньше памяти — не загружает код отрисовки кнопки **Я не робот**. Но у пользователей, которым показано задание, время загрузки виджета может варьироваться — предупреждайте их о показе капчи, чтобы не вводить в замешательство во время ожидания.

## См. также

* [mobile-webview.md](mobile-webview.md) — общий подход, готовая страница, методы моста `NativeClient`.
* [../templates/webview-page.html](../templates/webview-page.html) — HTML-страница для WebView.
* [server-validation.md](server-validation.md) — проверка токена через `/validate`.
* [invisible-captcha.md](invisible-captcha.md) — принципы работы невидимой капчи.
* [../workflows/integrate-mobile.md](../workflows/integrate-mobile.md) — пошаговый сценарий интеграции.
* Официальная документация: [SmartCaptcha в приложении на Android](https://yandex.cloud/ru/docs/tutorials/security/mobile-app/android/quickstart-android), [невидимая SmartCaptcha на Android](https://yandex.cloud/ru/docs/tutorials/security/mobile-app/android/invisible-captcha-android).
