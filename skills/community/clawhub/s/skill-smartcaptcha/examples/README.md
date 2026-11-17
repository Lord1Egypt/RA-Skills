# Примеры интеграции SmartCaptcha

Читайте этот файл, когда нужен готовый запускаемый образец интеграции целиком — от виджета на странице до проверки токена на сервере, — чтобы выбрать подходящий стек и скопировать рабочий код.

## Список примеров

| Пример | Стек | Что показывает |
| --- | --- | --- |
| [express-fullstack](express-fullstack/README.md) | Node.js 18+, Express (единственная зависимость) | Страница с автоматическим виджетом, `POST /submit`, проверка токена глобальным `fetch` + `URLSearchParams` |
| [flask-fullstack](flask-fullstack/README.md) | Python, Flask + requests | Jinja2-шаблон с автоматическим виджетом, `POST /submit`, проверка токена по образцу Python из официального быстрого старта |

## Общее для всех примеров

Оба примера реализуют один и тот же сценарий и одну и ту же семантику проверки — меняется только язык:

* **Виджет** подключается автоматическим методом: скрипт `https://smartcaptcha.yandexcloud.net/captcha.js` и контейнер `div.smart-captcha` с `data-sitekey` (подробности — [../docs/widget-auto.md](../docs/widget-auto.md)).
* **Токен** приходит на сервер в поле формы `smart-token`; сервер проверяет его запросом `POST https://smartcaptcha.yandexcloud.net/validate` с параметрами `secret`, `token`, `ip` (подробности — [../docs/server-validation.md](../docs/server-validation.md)).
* **Решение** принимается только по полю `status` (`ok` / `failed`); ошибки HTTP-протокола (код не 200), таймаут и сетевые сбои обрабатываются как fail-open — пользователь пропускается, чтобы сбой сервиса не блокировал ваш сайт.
* **Ключи** берутся из переменных окружения `SMARTCAPTCHA_CLIENT_KEY` (sitekey, подставляется в страницу) и `SMARTCAPTCHA_SERVER_KEY` (секрет для `/validate`); как их получить — [../docs/keys.md](../docs/keys.md).
* **Токен одноразовый и живет 5 минут** — повторная отправка формы с тем же токеном будет отклонена; это нормальное поведение, а не ошибка примера.

Перед запуском создайте капчу в Yandex Cloud и добавьте домен в список разрешенных сайтов — пошагово в [../workflows/setup-captcha.md](../workflows/setup-captcha.md). Полный сценарий интеграции на существующий сайт — [../workflows/integrate-website.md](../workflows/integrate-website.md).

## См. также

* [express-fullstack/README.md](express-fullstack/README.md) — инструкция к примеру на Node.js.
* [flask-fullstack/README.md](flask-fullstack/README.md) — инструкция к примеру на Flask.
* [../docs/server-validation.md](../docs/server-validation.md) — серверная проверка токена: все варианты ответов `/validate`.
* [../docs/widget-auto.md](../docs/widget-auto.md) — автоматическое подключение виджета.
* [../docs/keys.md](../docs/keys.md) — ключ клиента и ключ сервера.
* Официальная документация: [Быстрый старт](https://yandex.cloud/ru/docs/smartcaptcha/quickstart), [Валидация пользователя](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation), [Методы установки виджета](https://yandex.cloud/ru/docs/smartcaptcha/concepts/widget-methods).
