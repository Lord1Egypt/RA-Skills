# SmartCaptcha в iOS-приложении (WKWebView)

Читайте этот файл, когда встраиваете SmartCaptcha в нативное iOS-приложение на Swift. Общий подход к мобильной интеграции (HTML-страница, обмен сообщениями между WebView и нативным кодом) описан в [mobile-webview.md](mobile-webview.md) — здесь только iOS-специфика.

## Схема интеграции

1. WKWebView загружает HTML-страницу с виджетом капчи — свою страницу (шаблон: [../templates/webview-page.html](../templates/webview-page.html)) или готовую `smartcaptcha.yandexcloud.net`. Для загрузки страницы нужен **ключ клиента** (см. [keys.md](keys.md)).
2. JS-код страницы подписывается на события виджета и пересылает их в нативную часть через `window.webkit.messageHandlers`.
3. Нативная часть регистрирует `WKScriptMessageHandler` в `WKUserContentController` и получает токен.
4. Токен отправляется на ваш бэкенд, который проверяет его POST-запросом на `https://smartcaptcha.yandexcloud.net/validate` с **ключом сервера** — см. [server-validation.md](server-validation.md). Не храните ключ сервера в приложении: его можно извлечь из бинарника.

## JS-часть страницы

Если используете готовую страницу `smartcaptcha.yandexcloud.net`, этот шаг не нужен. Для своей страницы добавьте виджет и метод пересылки сообщений в нативную часть:

```js
function sendIos(...args) {
  if (args.length == 0) {
    return;
  }
  const message = {
    method: args[0],
    data: args[1] !== undefined ? args[1] : ""
  };

  // Проверка на вызов из WKWebView.
  if (window.webkit) {
    window.webkit.messageHandlers.NativeClient.postMessage(message);
  }
}
```

Формат сообщения:

```js
{
  method: "captchaDidFinish" | "challengeDidAppear" | "challengeDidDisappear"
  data: "tokenName" | ""
}
```

Методы соответствуют событиям виджета (см. [../references/js-api.md](../references/js-api.md)):

| Метод | Событие виджета | Смысл |
|---|---|---|
| `captchaDidFinish` | `success` | успешная валидация пользователя, в `data` — токен |
| `challengeDidAppear` | `challenge-visible` | открытие всплывающего окна с заданием |
| `challengeDidDisappear` | `challenge-hidden` | закрытие всплывающего окна с заданием |

## Нативная часть: приём токена в Swift

Зарегистрируйте в `WKUserContentController` обработчик `WKScriptMessageHandler` для ключа `NativeClient` (имя должно совпадать с именем в JS: `messageHandlers.NativeClient`). Компактный рабочий вариант:

```swift
// Экран с капчей в WKWebView; подробности — в dist/docs/mobile-ios.md
import UIKit
import WebKit

final class CaptchaViewController: UIViewController, WKScriptMessageHandler {

    private var webView: WKWebView!

    override func viewDidLoad() {
        super.viewDidLoad()

        let userContentController = WKUserContentController()
        userContentController.add(self, name: "NativeClient") // ключ из JS-части

        let configuration = WKWebViewConfiguration()
        configuration.userContentController = userContentController

        webView = WKWebView(frame: view.bounds, configuration: configuration)
        view.addSubview(webView)

        // Страница с виджетом; ключ клиента передаётся в параметре sitekey
        let url = URL(string: "https://<домен_вашей_страницы>/captcha.html?sitekey=<ключ_клиента>")!
        webView.load(URLRequest(url: url))
    }

    // Сообщения от JS-части страницы
    func userContentController(_ userContentController: WKUserContentController,
                               didReceive message: WKScriptMessage) {
        guard let jsData = message.body as? [String: String],
              let methodName = jsData["method"] else { return }

        switch methodName {
        case "captchaDidFinish":
            let token = jsData["data"] ?? ""
            sendTokenToBackend(token) // отправьте токен на свой бэкенд для /validate
        case "challengeDidAppear":
            showWebView()             // актуально для невидимой капчи
        case "challengeDidDisappear":
            hideWebView()             // окно задания закрылось; webView.reload() нужен только
                                      // для невидимой капчи, если пользователь «смахнул» задание
                                      // без captchaDidFinish (см. раздел «Невидимая капча»)
        default:
            break
        }
    }
}
```

Если обработчиков несколько, удобнее вынести их в отдельные классы и регистрировать циклом: `handlers.forEach { userContentController.add($1, name: $0) }` — так сделано в официальном примере [Yandex SmartCaptcha for iOS](https://github.com/yandex-cloud-examples/yc-smartcaptcha-ios-example/tree/main).

## Проверка токена

После получения токена из `captchaDidFinish` отправьте POST-запрос на `https://smartcaptcha.yandexcloud.net/validate` в формате `x-www-form-urlencoded` с параметрами:

* `secret` — ключ сервера;
* `token` — одноразовый токен, полученный после прохождения проверки;
* `ip` — IP-адрес пользователя, с которого пришел запрос на проверку токена. Параметр не обязателен, но его передача помогает улучшить качество работы SmartCaptcha.

В тьюториале Yandex Cloud запрос к `/validate` выполняется прямо из приложения (класс `CaptchaValidator` на `URLSession`) — это годится для демо. В продакшене делайте запрос со своего бэкенда: токен одноразовый, а ключ сервера не должен попадать в клиентский код. Полный формат ответа `/validate` — в [../references/validate-api.md](../references/validate-api.md).

## Невидимая капча

Виджет с параметром `invisible` не отображается в HTML-коде страницы (см. [invisible-captcha.md](invisible-captcha.md)), поэтому:

* **`challengeDidAppear`.** WKWebView должен быть загружен, но недоступен пользователю до вызова этого метода. Один из способов показать его по событию:

  ```swift
  UIApplication.shared.windows.first?.addSubview(webControllerView)
  ```

  Если после проверки приходит `captchaDidFinish` — удалите `webControllerView` из иерархии. Если `captchaDidFinish` нет — переместите `webControllerView` в иерархию для показа пользователю.

* **`challengeDidDisappear`.** Если пользователь «смахнул» капчу с экрана, восстановить её самостоятельно не получится. Перезагрузите контент WKWebView по этому событию:

  ```swift
  webControllerView.reload()
  ```

## См. также

* [mobile-webview.md](mobile-webview.md) — общий подход: HTML-страница, JavaScript Interface, параметр `webview`.
* [../templates/webview-page.html](../templates/webview-page.html) — готовая HTML-страница для WebView.
* [server-validation.md](server-validation.md) — проверка токена на бэкенде (обязательный шаг).
* [invisible-captcha.md](invisible-captcha.md) — как работает невидимая капча.
* [mobile-android.md](mobile-android.md), [mobile-flutter.md](mobile-flutter.md) — интеграция на других мобильных платформах.
* [../workflows/integrate-mobile.md](../workflows/integrate-mobile.md) — пошаговый сценарий мобильной интеграции.
* Официальная документация: [SmartCaptcha в приложении на iOS](https://yandex.cloud/ru/docs/tutorials/security/mobile-app/ios/quickstart-ios), [объект JavaScript Interface](https://yandex.cloud/ru/docs/smartcaptcha/concepts/js-interface).
