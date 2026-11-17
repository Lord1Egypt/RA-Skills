# Workflow: интеграция SmartCaptcha в мобильное приложение

Читай этот файл, когда капчу нужно встроить в приложение для Android, iOS или Flutter. Нативного SDK у SmartCaptcha нет: капча живёт в HTML-странице внутри WebView, токен передаётся в нативный код через мост, а проверяется на твоём бэкенде.

## Шаги

1. **Пойми архитектуру и получи ключи.**
   Обязательно к прочтению: [../docs/mobile-webview.md](../docs/mobile-webview.md) — схема «страница в WebView → мост → бэкенд», параметр `webview: true`, структура JavaScript Interface. Ключи — [../docs/keys.md](../docs/keys.md); если капчи нет — сначала [setup-captcha.md](setup-captcha.md).

   > **Важно.** Ключ сервера в приложение попадать не должен — из бинарника его можно извлечь. В приложении используется только ключ клиента.

   *Готово:* есть ключ клиента (`ysc1_...`); ключ сервера (`ysc2_...`) — в секретах бэкенда.

2. **Выбери платформу и вариант капчи.**
   - **Android** — [../docs/mobile-android.md](../docs/mobile-android.md): `WebView`, класс с аннотациями `@JavascriptInterface`, мост `NativeClient`.
   - **iOS** — [../docs/mobile-ios.md](../docs/mobile-ios.md): `WKWebView`, `WKScriptMessageHandler` в `WKUserContentController`, сообщения через `window.webkit.messageHandlers.NativeClient`.
   - **Flutter** — [../docs/mobile-flutter.md](../docs/mobile-flutter.md): пакет `webview_flutter`, `JavaScriptChannel` с именем `jsBridge`.

   Вариант капчи: **обычная** (WebView с кнопкой **Я не робот** виден сразу) или **невидимая** ([../docs/invisible-captcha.md](../docs/invisible-captcha.md)) — WebView скрыт и показывается только при событии `onChallengeVisible`; требует уведомления пользователей об обработке данных.
   *Готово:* платформа и вариант выбраны.

3. **Подготовь HTML-страницу для WebView.**
   Справка: [../docs/mobile-webview.md](../docs/mobile-webview.md). Два пути:
   - **Своя страница** — размести шаблон [../templates/webview-page.html](../templates/webview-page.html) на своём сервере. Нужна, если хочешь переименовать методы моста или добавить свою логику.
   - **Готовая страница Yandex Cloud** — `smartcaptcha.yandexcloud.net`, хостить ничего не нужно. Параметры передаются в query-строке: `sitekey` (обязателен), `invisible=true`, `test=true`, `hideShield=true`; `webview: true` страница выставляет сама.
   *Готово:* известен URL страницы.
   *Проверка:* URL вида `https://smartcaptcha.yandexcloud.net/?sitekey=<ключ_клиента>` (или URL своей страницы с `?sitekey=...`) открывается в обычном браузере и показывает виджет.

4. **Реализуй нативную часть по платформе.**
   Пошаговый код — в платформенном файле из шага 2. Общее для всех платформ:
   - включи JavaScript в WebView и зарегистрируй мост: `NativeClient` (Android/iOS) или канал `jsBridge` (Flutter) — имя должно совпадать с именем на странице;
   - загрузи URL страницы с query-параметром `sitekey=<ключ_клиента>` (плюс `invisible=true` для невидимой);
   - прими токен (механизм зависит от платформы): Android — метод `onGetToken(token)` в JavaScript Interface (обязательный); iOS — сообщение `{method: "captchaDidFinish", data: <токен>}` в обработчике `NativeClient`; Flutter — токен приходит строкой в `onMessageReceived` канала `jsBridge`; для невидимой капчи дополнительно `onChallengeVisible` (показать WebView) и `onChallengeHidden` (пользователь закрыл задание — восстановить окно нельзя, верни его на предыдущий экран).
   *Готово:* токен приходит в нативный код.
   *Проверка:* залогируй токен в обработчике моста — после прохождения капчи в логе непустая строка.

5. **Отправь токен на бэкенд и реализуй проверку.**
   Справка: [../docs/server-validation.md](../docs/server-validation.md), формат запроса/ответов — [../references/validate-api.md](../references/validate-api.md). Шаблоны под стек: [../templates/validate.py](../templates/validate.py), [../templates/validate.js](../templates/validate.js), [../templates/validate.php](../templates/validate.php).
   Приложение отправляет токен на твой API; бэкенд делает POST `https://smartcaptcha.yandexcloud.net/validate` (`x-www-form-urlencoded`: `secret`, `token`, `ip`) и решает по полю `status` (`ok`/`failed`).

   > **Важно.** Токен одноразовый и живёт 5 минут — проверяй его сразу после получения. При HTTP-коде не 200 рекомендуется fail-open — пропустить пользователя.

   *Готово:* защищаемый эндпоинт валидирует токен до бизнес-логики.
   *Проверка:* свежий токен из лога приложения проходит `python scripts/check_token.py --token <токен>` ([../scripts/check_token.py](../scripts/check_token.py)); повторная проверка того же токена возвращает `failed` с `Invalid or expired Token` — это норма.

6. **Протестируй полный цикл.**
   Типичные проблемы: [../docs/troubleshooting.md](../docs/troubleshooting.md).
   - Для гарантированного показа задания добавь `test=true` в URL страницы — только на время отладки, убери перед релизом.
   - Для невидимой капчи проверь оба сценария: задание появилось (WebView показался) и пользователь «смахнул» задание (`onChallengeHidden` — возврат на предыдущий экран).
   - Проверь повторную отправку: второй запрос с тем же токеном должен отклоняться бэкендом.
   *Готово:* цикл «WebView → мост → API → `/validate` → решение» работает на устройстве/эмуляторе.

7. **Пройди чеклист безопасности.**
   - Ключ сервера отсутствует в коде и ресурсах приложения: поиск `ysc2_` по проекту приложения пуст ([../docs/keys.md](../docs/keys.md)).
   - Проверка токена — только на бэкенде; факт получения токена в приложении ничего не гарантирует.
   - Решение принимается по `status`, `message` — только для диагностики.
   - Если блок с уведомлением скрыт (`hideShield=true`) — пользователи уведомлены об обработке данных SmartCaptcha другим способом.
   *Готово:* все пункты подтверждены.

## См. также

- [setup-captcha.md](setup-captcha.md) — создание капчи и получение ключей
- [../docs/mobile-webview.md](../docs/mobile-webview.md) — общая архитектура мобильной интеграции
- [../docs/mobile-android.md](../docs/mobile-android.md), [../docs/mobile-ios.md](../docs/mobile-ios.md), [../docs/mobile-flutter.md](../docs/mobile-flutter.md) — платформенные инструкции
- [../templates/webview-page.html](../templates/webview-page.html) — готовая страница для WebView
- [../docs/server-validation.md](../docs/server-validation.md), [../references/validate-api.md](../references/validate-api.md) — проверка токена
- Официальная документация: [страница для мобильного приложения](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/website), [Android](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/android/quickstart-android), [невидимая капча на Android](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/android/invisible-captcha-android), [Flutter](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/android/quickstart-android-flutter), [iOS](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/ios/quickstart-ios)
