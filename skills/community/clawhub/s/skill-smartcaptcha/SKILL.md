---
name: skill-smartcaptcha
description: >-
  Интеграция и администрирование Yandex SmartCaptcha: виджет на сайте (обычный, расширенный, невидимая капча),
  серверная проверка токена через /validate, React (@yandex/smart-captcha), мобильные приложения (Android/iOS/Flutter
  через WebView), создание и настройка капчи в Yandex Cloud (консоль, CLI, Terraform, REST/gRPC API), диагностика и
  тарификация. Используй этот скилл всегда, когда упоминаются SmartCaptcha, «умная капча», «смарткапча», капча Яндекса,
  smart-token, smartcaptcha.yandexcloud.net, yandex_smartcaptcha_captcha, защита форм/логина/регистрации от ботов и
  спама в Yandex Cloud, стоимость или квоты SmartCaptcha, а также когда капча Яндекса не отображается или пропускает
  ботов — даже если слово «капча» не прозвучало, но нужна антибот-защита веб-формы или мобильного приложения.
---

# Yandex SmartCaptcha — интеграция и управление

Yandex SmartCaptcha — сервис Yandex Cloud для защиты сайтов и приложений от ботов. Принцип работы: виджет на странице проверяет пользователя и выдаёт **одноразовый токен** (живёт 5 минут) → фронтенд передаёт токен на ваш бэкенд → бэкенд **обязан** проверить токен POST-запросом на `/validate` и принять решение по полю `status`.

Начни с [docs/overview.md](docs/overview.md) — как работает сервис и как выбрать способ интеграции.

## Ключевые факты

| Что | Значение |
|---|---|
| Скрипт виджета | `<script src="https://smartcaptcha.yandexcloud.net/captcha.js" defer></script>` |
| Проверка токена | `POST https://smartcaptcha.yandexcloud.net/validate` (`x-www-form-urlencoded`: `secret`, `token`, `ip`) → `{"status": "ok"\|"failed", "message": "...", "host": "..."}` |
| Токен | Одноразовый, срок жизни 5 минут; лежит в `<input type="hidden" name="smart-token">` |
| При сбое сервиса | HTTP != 200 → fail-open: пропустить пользователя, залогировать |
| Ключи | Ключ клиента (`ysc1_…`, публичный, для виджета) и ключ сервера (`ysc2_…`, секрет, только на бэкенде, env `SMARTCAPTCHA_SERVER_KEY`) |
| React | Пакет `@yandex/smart-captcha` (официальный) |
| Vue 3 | Официального пакета нет — composable на расширенном методе, см. [docs/vue.md](docs/vue.md) |
| Управление | REST `https://smartcaptcha.api.cloud.yandex.net/smartcaptcha/v1/captchas`, CLI `yc smartcaptcha captcha`, Terraform `yandex_smartcaptcha_captcha` |

## Выбор сценария

| Задача | Пошаговый план | Ключевые знания |
|---|---|---|
| Создать/настроить капчу в Yandex Cloud | [workflows/setup-captcha.md](workflows/setup-captcha.md) | [docs/captcha-management.md](docs/captcha-management.md), [docs/captcha-settings.md](docs/captcha-settings.md), [docs/keys.md](docs/keys.md) |
| Капча на обычном сайте (HTML + бэкенд) | [workflows/integrate-website.md](workflows/integrate-website.md) | [docs/widget-auto.md](docs/widget-auto.md), [docs/server-validation.md](docs/server-validation.md) |
| Капча в React / SPA | [workflows/integrate-react.md](workflows/integrate-react.md) | [docs/react.md](docs/react.md) |
| Капча во Vue 3 / Nuxt | [workflows/integrate-react.md](workflows/integrate-react.md) (шаги те же, код — Vue) | [docs/vue.md](docs/vue.md) |
| Капча в мобильном приложении | [workflows/integrate-mobile.md](workflows/integrate-mobile.md) | [docs/mobile-webview.md](docs/mobile-webview.md) + файл платформы |
| Капча без кнопки «Я не робот» | [workflows/integrate-website.md](workflows/integrate-website.md) | [docs/invisible-captcha.md](docs/invisible-captcha.md) |
| Капча не работает / пропускает ботов | — | [docs/troubleshooting.md](docs/troubleshooting.md) |
| Оценить стоимость и лимиты | — | [docs/pricing-limits.md](docs/pricing-limits.md) |

## Карта знаний — docs/

Прочитай соответствующий файл **до** написания кода: имена параметров, поля ответов и шаги бери из него, а не по памяти.

**Основы:**
- [docs/overview.md](docs/overview.md) — принцип работы, жизненный цикл токена, таблица выбора метода интеграции.
- [docs/keys.md](docs/keys.md) — ключ клиента и ключ сервера: получение (консоль/CLI/API), безопасность, действия при компрометации.

**Виджет на сайте:**
- [docs/widget-auto.md](docs/widget-auto.md) — автоматический метод: `div.smart-captcha`, data-атрибуты, скрытое поле `smart-token`.
- [docs/widget-advanced.md](docs/widget-advanced.md) — расширенный метод: `?render=onload`, `window.smartCaptcha.render()`, callback, несколько виджетов, отправка токена fetch'ем, отложенная загрузка.
- [docs/invisible-captcha.md](docs/invisible-captcha.md) — невидимая капча: `invisible: true` + `execute()`, уведомление об обработке данных (`shieldPosition`/`hideShield`).

**Серверная проверка:**
- [docs/server-validation.md](docs/server-validation.md) — проверка токена на `/validate`: параметры, разбор ответов, «решение только по `status`», одноразовость, fail-open, таймауты, IP за прокси.

**Фреймворки и платформы:**
- [docs/react.md](docs/react.md) — `@yandex/smart-captcha`: компоненты `SmartCaptcha` и `InvisibleSmartCaptcha`, props, события, сброс через `key`.
- [docs/vue.md](docs/vue.md) — Vue 3 / Nuxt: composable на расширенном методе (официального пакета нет), жизненный цикл в SPA, невидимая капча как Promise, обзор community-пакетов.
- [docs/mobile-webview.md](docs/mobile-webview.md) — общий подход для мобильных: страница в WebView, мост в нативный код, готовая страница `smartcaptcha.yandexcloud.net`, параметр `webview`.
- [docs/mobile-android.md](docs/mobile-android.md) — Android: Kotlin, `@JavascriptInterface`, обычная и невидимая капча.
- [docs/mobile-ios.md](docs/mobile-ios.md) — iOS: WKWebView, `WKScriptMessageHandler`, приём токена в Swift.
- [docs/mobile-flutter.md](docs/mobile-flutter.md) — Flutter: `webview_flutter`, канал `jsBridge`.

**Управление и настройка:**
- [docs/captcha-management.md](docs/captcha-management.md) — создание/обновление/удаление капчи: консоль, CLI, Terraform, REST API; роли IAM `smart-captcha.*`; метрики Monitoring; аудитные логи Audit Trails; миграция условий на `host_matcher`.
- [docs/captcha-settings.md](docs/captcha-settings.md) — задания (чекбокс/слайдер; текст/силуэты/калейдоскоп), сложность, варианты заданий и правила показа по условиям трафика, метаданные (`metadata`), валидация домена.

**Эксплуатация:**
- [docs/troubleshooting.md](docs/troubleshooting.md) — «симптом → причины → решение»: виджет не отображается, `Invalid or expired Token`, ограниченный режим, доступность, как тестировать капчу при разработке.
- [docs/pricing-limits.md](docs/pricing-limits.md) — тарификация (платны только `status=ok`, 10 000/мес бесплатно), квоты, публичные IP сервиса.

## Справочники — references/

Точные таблицы для сверки имён и значений:

- [references/widget-params.md](references/widget-params.md) — все параметры `render()` и data-атрибуты (включая `test`, `webview`, `invisible`, `hideShield`, `metadata`).
- [references/js-api.md](references/js-api.md) — методы `window.smartCaptcha` с сигнатурами и все события `subscribe` с полезной нагрузкой.
- [references/validate-api.md](references/validate-api.md) — `/validate`: параметры запроса, все варианты ответов с примерами JSON, свойства токена.
- [references/management-api.md](references/management-api.md) — REST endpoint'ы, gRPC-сервисы, команды CLI, поля Terraform-ресурса, ключи `style_json`, IAM-токен, пример curl.
- [references/source-map.md](references/source-map.md) — какой файл скилла на какой странице официальной документации основан; как обновлять знания.

## Шаблоны — templates/ и утилита scripts/

Готовый код: копируй и адаптируй, а не пиши с нуля.

| Файл | Что это |
|---|---|
| [templates/widget-auto.html](templates/widget-auto.html) | Страница с формой и автоматическим виджетом |
| [templates/widget-advanced.html](templates/widget-advanced.html) | Расширенный метод: отложенная загрузка, `render`, отправка токена fetch'ем |
| [templates/invisible.html](templates/invisible.html) | Невидимая капча: `execute()` на submit, события `token-expired`/`network-error` |
| [templates/webview-page.html](templates/webview-page.html) | Страница для мобильного WebView (мосты Android `NativeClient` и iOS `messageHandlers`) |
| [templates/validate.py](templates/validate.py) | Проверка токена: Python (requests) |
| [templates/validate.js](templates/validate.js) | Проверка токена: Node.js 18+ (fetch, ESM) |
| [templates/validate.php](templates/validate.php) | Проверка токена: PHP (cURL) |
| [templates/SmartCaptchaField.tsx](templates/SmartCaptchaField.tsx) | React-компонент обычной капчи (токен и сброс через ref) |
| [templates/InvisibleCaptchaForm.tsx](templates/InvisibleCaptchaForm.tsx) | React-форма с невидимой капчей (проверка по submit) |
| [templates/useSmartCaptcha.ts](templates/useSmartCaptcha.ts) | Vue 3 composable: синглтон-загрузка скрипта, lifecycle, невидимая капча как Promise |
| [templates/smartcaptcha.d.ts](templates/smartcaptcha.d.ts) | TypeScript-типы `window.smartCaptcha` (для Vue/vanilla TS проектов) |
| [templates/validate-amphp.php](templates/validate-amphp.php) | Проверка токена в event loop: PHP + AMPHP v3 (amphp/http-client) |
| [templates/mock-validate.php](templates/mock-validate.php) | Локальный мок `/validate` для юнит/смоук-тестов (`php -S`), все канонические сценарии |
| [scripts/check_token.py](scripts/check_token.py) | CLI-смоук-тест: `python check_token.py --secret <ключ> --token <токен>`; только stdlib |

## Примеры — examples/

Запускаемые фуллстек-примеры «форма + серверная проверка» ([examples/README.md](examples/README.md)):

- [examples/express-fullstack/](examples/express-fullstack/README.md) — Node.js 18+ / Express: [server.js](examples/express-fullstack/server.js), [public/index.html](examples/express-fullstack/public/index.html), [package.json](examples/express-fullstack/package.json).
- [examples/flask-fullstack/](examples/flask-fullstack/README.md) — Python / Flask: [app.py](examples/flask-fullstack/app.py), [templates/index.html](examples/flask-fullstack/templates/index.html), [requirements.txt](examples/flask-fullstack/requirements.txt).

## Правила работы

1. **Токен всегда проверяется на бэкенде.** Виджет без серверной проверки `/validate` не защищает ничего. Решение — только по полю `status`; `message` — лишь для логов.
2. **Ключ сервера — секрет.** Только переменные окружения (`SMARTCAPTCHA_SERVER_KEY`) или секретница; не во фронтенд, не в репозиторий. См. [docs/keys.md](docs/keys.md).
3. **Fail-open при сбоях сервиса** (HTTP != 200, таймаут ~1 с): пропусти пользователя и залогируй — иначе сбой капчи положит ваши формы.
4. **Уведомление об обработке данных обязательно.** Скрывая блок Shield (`hideShield`), обязан показать уведомление другим способом.
5. **Не выдумывай параметры.** Точные имена и значения — в [references/](references/widget-params.md); если чего-то нет в справочниках, сверься с официальной документацией по карте [references/source-map.md](references/source-map.md).
6. **Тестирование:** задание принудительно — `test: true` (только не в проде); поведение «как незнакомый пользователь» — инкогнито/VPN; ручная проверка токена — [scripts/check_token.py](scripts/check_token.py). Подробнее — [docs/troubleshooting.md](docs/troubleshooting.md).
7. **Выдавай запускаемое решение целиком.** Кроме основного кода приложи манифесты зависимостей (`package.json`, `requirements.txt`, `composer.json`), пример переменных окружения (`.env.example`) и написанные в ходе работы тесты/проверочные скрипты — они часть решения, а не черновик. Ориентир комплектности — [examples/](examples/README.md).
8. **Читай по маршруту, а не всё подряд.** Начни с таблицы «Выбор сценария», открой workflow и только те docs/references, на которые он ссылается: это экономит контекст и время.

## Тест-кейсы скилла

[evals/evals.json](evals/evals.json) — 7 сценариев для проверки скилла (Express, React invisible, Flask, Terraform, Android, диагностика домена, тарификация).
