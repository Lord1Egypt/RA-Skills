# Справочник API /validate

Читай этот файл, когда нужны точные параметры запроса к `/validate` и все варианты ответов. Как правильно встроить проверку в backend (fail-open, таймауты, одноразовость токена) — в [../docs/server-validation.md](../docs/server-validation.md).

## Endpoint

```
POST https://smartcaptcha.yandexcloud.net/validate
Content-Type: application/x-www-form-urlencoded
```

Тело запроса: `secret=<ключ_сервера>&token=<токен>&ip=<IP-адрес_пользователя>`

## Параметры запроса

| Параметр | Обязательный | Описание |
|---|---|---|
| `secret` | Да | [Ключ сервера](../docs/keys.md). Без него — `failed` с `Authentication failed. Secret has not provided.` |
| `token` | Да | Одноразовый токен, полученный после прохождения проверки (поле формы `smart-token` или аргумент колбэка виджета). Токен живёт 5 минут и валидируется только один раз. |
| `ip` | Нет (рекомендуется) | IP-адрес пользователя, с которого пришёл запрос. Передавать просят для улучшения качества работы SmartCaptcha. |

## Коды HTTP

| Код | Значение | Что делать |
|---|---|---|
| `200` | Запрос обработан, в теле — JSON с результатом | Разбирать поле `status` |
| Не `200` | Ошибка сервиса | Рекомендуется обрабатывать как `"status": "ok"` (fail-open), чтобы не задерживать пользователя |

## Ответы (HTTP 200)

Поля JSON-ответа: `status` (`ok` | `failed`), `message` (диагностика), `host` — добавляется только при `status: ok` и показывает сайт, на котором пройдена проверка.

| Ситуация | `status` | Пример ответа |
|---|---|---|
| Человек, проверка пройдена на сайте | `ok` | `{"status": "ok", "message": "", "host": "example.com"}` |
| Человек, проверка пройдена через нестандартный порт | `ok` | `{"status": "ok", "message": "", "host": "example.com:8080"}` |
| Пустой `host`: облако заблокировано или внутренний сбой сервиса | `ok` | `{"status": "ok", "message": "", "host": ""}` |
| Робот | `failed` | `{"status": "failed", "message": ""}` |
| Поддельный, повреждённый, просроченный или повторно использованный токен (робот) | `failed` | `{"status": "failed", "message": "Invalid or expired Token."}` |
| Запрос без ключа сервера | `failed` | `{"status": "failed", "message": "Authentication failed. Secret has not provided."}` |
| Запрос без токена | `failed` | `{"status": "failed", "message": "Invalid or expired Token."}` |

Правила обработки:

* Решение принимай только по `status`: `ok` — пропустить, `failed` — отказать.
* `failed` с пустым `message` — «это робот»; `failed` с непустым `message` — ошибка в самом запросе (чинить на этапе разработки).
* `message` не предназначено для сравнения в коде — только для логов и диагностики.

> **Метаданные.** Если при отрисовке виджета передавался параметр `metadata` (см. [widget-params.md](widget-params.md)), по официальной схеме проверки ответ `/validate` содержит метаданные из справки о прохождении капчи — сверяй их со значениями, сохранёнными на бэкенде, для защиты от подделки. Точный формат поля в документации не приведён; схема описана в [../docs/captcha-settings.md](../docs/captcha-settings.md).

## Свойства токена

| Свойство | Значение |
|---|---|
| Срок жизни | 5 минут, затем токен недействителен |
| Использование | Однократное; повторная валидация → `failed`, `Invalid or expired Token` |
| Где лежит на странице | `<input type="hidden" name="smart-token" value="<токен>">` внутри контейнера виджета |

## См. также

* [../docs/server-validation.md](../docs/server-validation.md) — как встроить проверку: fail-open, таймауты, IP за прокси.
* [../docs/keys.md](../docs/keys.md) — где взять ключ сервера.
* [../templates/validate.py](../templates/validate.py), [../templates/validate.js](../templates/validate.js), [../templates/validate.php](../templates/validate.php) — готовые функции проверки.
* [../scripts/check_token.py](../scripts/check_token.py) — ручная проверка токена из командной строки.
* Официальная документация:
  * [Валидация пользователя](https://yandex.cloud/ru/docs/smartcaptcha/concepts/validation)
  * [Проверить капчу](https://yandex.cloud/ru/docs/smartcaptcha/operations/validate-captcha)
