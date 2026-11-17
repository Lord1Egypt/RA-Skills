# SmartCaptcha во Flutter-приложении

Читайте этот файл, когда встраиваете SmartCaptcha в мобильное приложение на Flutter (тьюториал Yandex Cloud проверен на Android). Общий подход к мобильной интеграции описан в [mobile-webview.md](mobile-webview.md) — здесь только Flutter-специфика: пакет `webview_flutter`, `JavaScriptChannel` и получение токена в Dart.

## Схема интеграции

Проект из тьюториала состоит из двух частей:

* **Серверное приложение** (в тьюториале — Flask) отдаёт HTML-страницу с капчей по эндпоинту `/captcha` и проверяет токен по эндпоинту `/validate-captcha`, вызывая `https://smartcaptcha.yandexcloud.net/validate` — см. [server-validation.md](server-validation.md).
* **Мобильное приложение** показывает страницу в `WebViewWidget`, получает токен через JS-канал и отправляет его серверу на проверку.

Ключи капчи: **ключ клиента** — для загрузки страницы с капчей, **ключ сервера** — для получения результата прохождения капчи (см. [keys.md](keys.md)). Ключ сервера живёт только на бэкенде.

## Зависимости

В `pubspec.yaml` добавьте в секцию `dependencies` пакеты `webview_flutter` и `http`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  webview_flutter: ^4.0.0
  http: ^0.13.5
```

## HTML-страница с капчей

Ключевой для Flutter фрагмент — из страницы `captcha.html` тьюториала: при событии `success` страница отправляет токен в приложение через объект `window.jsBridge`, который создаст `JavaScriptChannel`:

```js
function handleSuccess(token) {
  if (window.jsBridge) {
    window.jsBridge.postMessage(token);
  }
}
```

Готовый шаблон [../templates/webview-page.html](../templates/webview-page.html) использует другой мост — `NativeClient` (нативные Android и iOS), поэтому для Flutter его нужно адаптировать: добавьте в функцию `sendToNative` первой ветку `if (window.jsBridge) { window.jsBridge.postMessage(data); return; }` (либо замените мост на `jsBridge`).

Страница из тьюториала читает параметры виджета (`sitekey`, `test`, `invisible`, `hideShield`) из query-строки URL и всегда выставляет `webview: true` — этот параметр обязателен для корректной работы виджета в WebView (подробнее в [mobile-webview.md](mobile-webview.md)).

## Настройка контроллера и получение токена в Dart

Настройте `WebViewController`: разрешите JavaScript, откройте канал `jsBridge` (имя должно совпадать с `window.jsBridge` на странице) и загрузите страницу капчи:

```dart
// Экран с капчей в WebView; подробности — в dist/docs/mobile-flutter.md
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MaterialApp(
    home: Scaffold(
      appBar: AppBar(title: Text('SmartCaptcha Example')),
      body: WebViewExample(),
    ),
  ));
}

class WebViewExample extends StatefulWidget {
  @override
  _WebViewExampleState createState() => _WebViewExampleState();
}

class _WebViewExampleState extends State<WebViewExample> {
  late final WebViewController _controller;
  String result = "";

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted) // разрешить выполнение скриптов
      ..addJavaScriptChannel(                          // канал для сообщений от страницы
        'jsBridge',
        onMessageReceived: (message) {
          if (message.message == 'pageReloaded') {
            setState(() { result = "Not Done"; });
          } else {
            String token = message.message;   // получение токена от капчи
            _sendTokenToServer(token);        // отправка токена на валидацию
          }
        },
      );
    setState(() { result = "Not Done"; });
    // Загрузка страницы с капчей; sitekey — ключ клиента
    _controller.loadRequest(
      Uri.parse('<URL_серверного_приложения>:5000/captcha?sitekey=<ключ_клиента>'),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(child: WebViewWidget(controller: _controller)),
        SizedBox(height: 20),
        if (result.isNotEmpty)
          Text(result,
              style: TextStyle(
                  fontSize: 20,
                  color: result == "Passed" ? Colors.green : Colors.red)),
      ],
    );
  }

  Future<void> _sendTokenToServer(String token) async {
    const String serverValidationUrl =
        '<URL_серверного_приложения>:5000/validate-captcha';
    try {
      setState(() { result = "Checking"; });
      final response = await http.post(
        Uri.parse(serverValidationUrl),
        body: jsonEncode({'token': token}),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        var jsonResponse = jsonDecode(response.body);
        setState(() {
          result = jsonResponse['status'] == 'ok' ? 'Passed' : 'Robot';
        });
      } else {
        setState(() { result = 'Error'; });
      }
    } catch (e) {
      setState(() { result = 'Error'; });
    }
  }
}
```

Почему токен уходит на сервер, а не на `/validate` напрямую: проверка требует ключа сервера, который нельзя хранить в приложении, а токен одноразовый — результат проверки должен фиксировать ваш бэкенд. Формат серверной проверки — в [server-validation.md](server-validation.md) и [../references/validate-api.md](../references/validate-api.md).

## Особенности запуска в эмуляторе Android

> **Важно.** Если серверное приложение запущено на том же компьютере, что и Flutter с Android Studio, не используйте адрес `http://localhost` в качестве URL сервера — эмулятор его не увидит. Используйте IP-адрес внутренней подсети, например `http://10.0.2.2`.

Чтобы в тестовых целях использовать незащищённый HTTP-протокол, в `\android\app\src\main\AndroidManifest.xml` добавьте в секцию `application` опцию:

```xml
android:usesCleartextTraffic="true"
```

Для проверки: запустите `main.dart` на устройстве из **Tools → Device Manager**, выполните задание капчи и наблюдайте смену статуса `Not Done` → `Checking` → `Passed`. Кнопка **Reload** на странице из тьюториала перезапускает тест (страница шлёт в канал сообщение `pageReloaded`); в шаблоне webview-page.html этой кнопки нет.

## См. также

* [mobile-webview.md](mobile-webview.md) — общий подход: HTML-страница, JavaScript Interface, параметр `webview`.
* [../templates/webview-page.html](../templates/webview-page.html) — готовая HTML-страница для WebView.
* [server-validation.md](server-validation.md) — проверка токена на бэкенде (обязательный шаг).
* [mobile-android.md](mobile-android.md), [mobile-ios.md](mobile-ios.md) — нативная интеграция на Android и iOS.
* [../workflows/integrate-mobile.md](../workflows/integrate-mobile.md) — пошаговый сценарий мобильной интеграции.
* Официальная документация: [SmartCaptcha в приложении Android на Flutter](https://yandex.cloud/ru/docs/tutorials/security/mobile-app/android/quickstart-android-flutter), [объект JavaScript Interface](https://yandex.cloud/ru/docs/smartcaptcha/concepts/js-interface).
