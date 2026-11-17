# Карта соответствия официальной документации

Читай этот файл, когда нужно проверить факт по первоисточнику или обновить скилл после изменений в официальной документации Yandex SmartCaptcha. Для каждого файла скилла здесь указаны страницы документации, из которых взято его содержимое.

Правило построения URL: все страницы лежат под `https://yandex.cloud/ru/docs/smartcaptcha/`. Путь страницы в снимке документации равен пути URL без расширения `.md`; файлы `index.md` соответствуют URL каталога (например, `api-ref/index.md` → `.../api-ref/`).

## docs/

| Файл скилла | Тема | Официальные страницы |
|---|---|---|
| docs/overview.md | Как работает SmartCaptcha, жизненный цикл токена, выбор способа интеграции | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart), [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation), [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods) |
| docs/keys.md | Ключ клиента и ключ сервера: получение, безопасность | [concepts/keys](https://yandex.cloud/ru/docs/smartcaptcha/concepts/keys), [operations/get-keys](https://yandex.cloud/ru/docs/smartcaptcha/operations/get-keys) |
| docs/widget-auto.md | Автоматическое подключение виджета (`div.smart-captcha`) | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart), [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [operations/advanced-method](https://yandex.cloud/ru/docs/smartcaptcha/operations/advanced-method) |
| docs/widget-advanced.md | Расширенный метод: `window.smartCaptcha.render`, колбэки | [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [operations/advanced-method](https://yandex.cloud/ru/docs/smartcaptcha/operations/advanced-method) |
| docs/invisible-captcha.md | Невидимая капча | [concepts/invisible-captcha](https://yandex.cloud/ru/docs/smartcaptcha/concepts/invisible-captcha), [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods) |
| docs/server-validation.md | Серверная проверка токена через `/validate` | [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation), [concepts/metadata-scheme](https://yandex.cloud/ru/docs/smartcaptcha/concepts/metadata-scheme), [operations/validate-captcha](https://yandex.cloud/ru/docs/smartcaptcha/operations/validate-captcha), [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) |
| docs/react.md | React-интеграция (`@yandex/smart-captcha`) | [concepts/react](https://yandex.cloud/ru/docs/smartcaptcha/concepts/react) |
| docs/vue.md | Vue 3: composable на расширенном методе; community-пакеты | [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [concepts/invisible-captcha](https://yandex.cloud/ru/docs/smartcaptcha/concepts/invisible-captcha); community: [vue3-smart-captcha](https://github.com/czernika/vue3-smart-captcha), [@gladesinger/vue3-yandex-smartcaptcha](https://www.npmjs.com/package/@gladesinger/vue3-yandex-smartcaptcha) (неофициальные, состояние на июль 2026) |
| docs/mobile-webview.md | Мобильная интеграция: HTML-страница, JavaScript Interface | [tutorials/mobile-app/website](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/website), [concepts/js-interface](https://yandex.cloud/ru/docs/smartcaptcha/concepts/js-interface) |
| docs/mobile-android.md | Android: WebView, обычная и невидимая капча | [tutorials/mobile-app/android/quickstart-android](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/android/quickstart-android), [tutorials/mobile-app/android/invisible-captcha-android](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/android/invisible-captcha-android) |
| docs/mobile-ios.md | iOS: WKWebView | [tutorials/mobile-app/ios/quickstart-ios](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/ios/quickstart-ios) |
| docs/mobile-flutter.md | Flutter: webview_flutter | [tutorials/mobile-app/android/quickstart-android-flutter](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/android/quickstart-android-flutter) |
| docs/captcha-management.md | Создание и управление капчей, роли, мониторинг, аудит | [operations/](https://yandex.cloud/ru/docs/smartcaptcha/operations/), [operations/create-captcha](https://yandex.cloud/ru/docs/smartcaptcha/operations/create-captcha), [operations/get-list](https://yandex.cloud/ru/docs/smartcaptcha/operations/get-list), [operations/get-info](https://yandex.cloud/ru/docs/smartcaptcha/operations/get-info), [operations/delete-captcha](https://yandex.cloud/ru/docs/smartcaptcha/operations/delete-captcha), [operations/operation-logs](https://yandex.cloud/ru/docs/smartcaptcha/operations/operation-logs), [security/](https://yandex.cloud/ru/docs/smartcaptcha/security/), [metrics](https://yandex.cloud/ru/docs/smartcaptcha/metrics), [at-ref](https://yandex.cloud/ru/docs/smartcaptcha/at-ref) |
| docs/captcha-settings.md | Типы заданий, сложность, варианты заданий, правила показа, домены | [concepts/tasks](https://yandex.cloud/ru/docs/smartcaptcha/concepts/tasks), [concepts/captcha-variants](https://yandex.cloud/ru/docs/smartcaptcha/concepts/captcha-variants), [concepts/domain-validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/domain-validation) |
| docs/troubleshooting.md | Типичные проблемы и решения, доступность | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) (раздел «Частые вопросы»), [concepts/accessibility](https://yandex.cloud/ru/docs/smartcaptcha/concepts/accessibility), [concepts/domain-validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/domain-validation), [concepts/restricted-mode](https://yandex.cloud/ru/docs/smartcaptcha/concepts/restricted-mode) |
| docs/pricing-limits.md | Тарификация, квоты и лимиты, публичные IP | [pricing](https://yandex.cloud/ru/docs/smartcaptcha/pricing), [concepts/limits](https://yandex.cloud/ru/docs/smartcaptcha/concepts/limits), [concepts/ips](https://yandex.cloud/ru/docs/smartcaptcha/concepts/ips), [concepts/restricted-mode](https://yandex.cloud/ru/docs/smartcaptcha/concepts/restricted-mode) |

## references/

| Файл скилла | Тема | Официальные страницы |
|---|---|---|
| references/widget-params.md | Параметры виджета: `render()` и data-атрибуты | [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [operations/advanced-method](https://yandex.cloud/ru/docs/smartcaptcha/operations/advanced-method) |
| references/js-api.md | Методы и события `window.smartCaptcha` | [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [concepts/js-interface](https://yandex.cloud/ru/docs/smartcaptcha/concepts/js-interface) |
| references/validate-api.md | `/validate`: параметры запроса, варианты ответов | [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation), [concepts/metadata-scheme](https://yandex.cloud/ru/docs/smartcaptcha/concepts/metadata-scheme) |
| references/management-api.md | REST/gRPC endpoint'ы, CLI-команды, Terraform-ресурс | [api-ref/](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/), [api-ref/authentication](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/authentication), [api-ref/Captcha/](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/Captcha/), [api-ref/grpc/](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/grpc/), [cli-ref/](https://yandex.cloud/ru/docs/smartcaptcha/cli-ref/), [cli-ref/captcha/](https://yandex.cloud/ru/docs/smartcaptcha/cli-ref/captcha/), [tf-ref](https://yandex.cloud/ru/docs/smartcaptcha/tf-ref), [operations/api-migration](https://yandex.cloud/ru/docs/smartcaptcha/operations/api-migration) |
| references/source-map.md | Карта соответствия (этот файл) | [Корень раздела SmartCaptcha](https://yandex.cloud/ru/docs/smartcaptcha/) |

Методы `Captcha` в REST API (аналогично для gRPC — путь с `grpc/`): [create](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/Captcha/create), [get](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/Captcha/get), [getSecretKey](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/Captcha/getSecretKey), [list](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/Captcha/list), [update](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/Captcha/update), [delete](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/Captcha/delete). Команды CLI: [create](https://yandex.cloud/ru/docs/smartcaptcha/cli-ref/captcha/create), [get](https://yandex.cloud/ru/docs/smartcaptcha/cli-ref/captcha/get), [get-secret-key](https://yandex.cloud/ru/docs/smartcaptcha/cli-ref/captcha/get-secret-key), [list](https://yandex.cloud/ru/docs/smartcaptcha/cli-ref/captcha/list), [update](https://yandex.cloud/ru/docs/smartcaptcha/cli-ref/captcha/update), [delete](https://yandex.cloud/ru/docs/smartcaptcha/cli-ref/captcha/delete).

## templates/

| Файл скилла | Тема | Официальные страницы |
|---|---|---|
| templates/widget-auto.html | Страница с автоматическим виджетом | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) |
| templates/widget-advanced.html | Страница с расширенным методом | [operations/advanced-method](https://yandex.cloud/ru/docs/smartcaptcha/operations/advanced-method), [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods) |
| templates/invisible.html | Страница с невидимой капчей | [concepts/invisible-captcha](https://yandex.cloud/ru/docs/smartcaptcha/concepts/invisible-captcha) |
| templates/webview-page.html | Страница для мобильного WebView | [tutorials/mobile-app/website](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/website) |
| templates/validate.py | Серверная проверка токена (Python) | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart), [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation) |
| templates/validate.js | Серверная проверка токена (Node.js) | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart), [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation) |
| templates/validate.php | Серверная проверка токена (PHP) | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart), [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation) |
| templates/validate-amphp.php | Проверка токена в event loop (AMPHP v3) | [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation) + [AMPHP](https://amphp.org) (семантика — официальная, async-обвязка — конвенция скилла) |
| templates/mock-validate.php | Локальный мок `/validate` для тестов | [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation), [operations/validate-captcha](https://yandex.cloud/ru/docs/smartcaptcha/operations/validate-captcha) (формы ответов — из документации; сам мок — утилита скилла) |
| templates/useSmartCaptcha.ts | Vue 3 composable | [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods) (JS API — официальный; Vue-обвязка — конвенция скилла) |
| templates/smartcaptcha.d.ts | TypeScript-типы `window.smartCaptcha` | [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods) |
| templates/SmartCaptchaField.tsx | React-компонент обычной капчи | [concepts/react](https://yandex.cloud/ru/docs/smartcaptcha/concepts/react) |
| templates/InvisibleCaptchaForm.tsx | React-компонент невидимой капчи | [concepts/react](https://yandex.cloud/ru/docs/smartcaptcha/concepts/react), [concepts/invisible-captcha](https://yandex.cloud/ru/docs/smartcaptcha/concepts/invisible-captcha) |

## scripts/

| Файл скилла | Тема | Официальные страницы |
|---|---|---|
| scripts/check_token.py | CLI-утилита ручной проверки токена через `/validate` | [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation), [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) |

## workflows/

| Файл скилла | Тема | Официальные страницы |
|---|---|---|
| workflows/setup-captcha.md | Создать и настроить капчу в Yandex Cloud | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart), [operations/create-captcha](https://yandex.cloud/ru/docs/smartcaptcha/operations/create-captcha), [operations/get-keys](https://yandex.cloud/ru/docs/smartcaptcha/operations/get-keys) |
| workflows/integrate-website.md | Интеграция на классический сайт (HTML + backend) | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart), [concepts/widget-methods](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods), [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation) |
| workflows/integrate-react.md | Интеграция в React/SPA | [concepts/react](https://yandex.cloud/ru/docs/smartcaptcha/concepts/react), [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation) |
| workflows/integrate-mobile.md | Интеграция в мобильное приложение | [tutorials/](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/), [tutorials/mobile-app/website](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/website), [tutorials/mobile-app/android/quickstart-android](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/android/quickstart-android), [tutorials/mobile-app/ios/quickstart-ios](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/ios/quickstart-ios), [tutorials/mobile-app/android/quickstart-android-flutter](https://yandex.cloud/ru/docs/smartcaptcha/tutorials/mobile-app/android/quickstart-android-flutter), [concepts/js-interface](https://yandex.cloud/ru/docs/smartcaptcha/concepts/js-interface) |

## examples/

| Файл скилла | Тема | Официальные страницы |
|---|---|---|
| examples/README.md | Обзор примеров | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) |
| examples/express-fullstack/package.json | Зависимости примера Express | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) (вкладка Node.js) |
| examples/express-fullstack/server.js | Backend Express: приём формы и проверка токена | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) (вкладка Node.js), [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation) |
| examples/express-fullstack/public/index.html | Страница с виджетом для примера Express | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) |
| examples/express-fullstack/README.md | Запуск примера Express | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) |
| examples/flask-fullstack/requirements.txt | Зависимости примера Flask | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) (вкладка Python) |
| examples/flask-fullstack/app.py | Backend Flask: приём формы и проверка токена | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) (вкладка Python), [concepts/validation](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation) |
| examples/flask-fullstack/templates/index.html | Страница с виджетом для примера Flask | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) |
| examples/flask-fullstack/README.md | Запуск примера Flask | [quickstart](https://yandex.cloud/ru/docs/smartcaptcha/quickstart) |

## Страницы снимка, не привязанные к отдельным файлам скилла

* [release-notes](https://yandex.cloud/ru/docs/smartcaptcha/release-notes) — история изменений; просматривай при обновлении скилла, чтобы найти новые возможности.
* [api-ref/Operation/](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/Operation/) и [api-ref/grpc/](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/grpc/) (OperationService) — служебные методы работы с операциями; в скилле упоминаются только в контексте references/management-api.md.
* `cli-ref/v0/*` и `cli-ref/v1/*` — версионированные дубли CLI-справочника; скилл опирается на неверсионированный `cli-ref/captcha/*`.

## Как обновлять знания скилла

1. Источник истины — репозиторий документации Yandex Cloud: https://github.com/yandex-cloud/docs, раздел `ru/smartcaptcha`.
2. Локальный снимок раздела хранится в корне проекта в папке `docs/` (вне скилла; не путать с папкой `docs/` внутри самого скилла). Дата текущего снимка: **2026-07-03**.
3. Порядок обновления: обнови локальный снимок из репозитория → посмотри diff по файлам → по таблицам выше найди файлы скилла, привязанные к изменившимся страницам → внеси правки → сверь канонические факты (URL `captcha.js`, endpoint `/validate`, endpoint management API, имена CLI-команд и Terraform-ресурса) с новым снимком.
4. Если в снимке появились новые страницы, добавь их в эту карту и реши, какой файл скилла должен их покрывать; устаревшие страницы убирай из таблиц вместе с зависимым содержимым.

## См. также

* [../SKILL.md](../SKILL.md) — роутер скилла.
* [../docs/overview.md](../docs/overview.md) — обзор сервиса и выбор способа интеграции.
* [validate-api.md](validate-api.md), [widget-params.md](widget-params.md), [js-api.md](js-api.md), [management-api.md](management-api.md) — остальные справочники скилла.
* Официальная документация: https://yandex.cloud/ru/docs/smartcaptcha/
* Репозиторий документации: https://github.com/yandex-cloud/docs
