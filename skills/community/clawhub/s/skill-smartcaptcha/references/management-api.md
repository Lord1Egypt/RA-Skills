# Справочник API управления SmartCaptcha

Читай этот файл, когда нужен точный REST endpoint, gRPC-вызов, команда CLI или поле Terraform для управления капчами. Пошаговые инструкции — в [../docs/captcha-management.md](../docs/captcha-management.md).

## Аутентификация в API

Все запросы к API управления требуют IAM-токен в заголовке `Authorization`:

```
Authorization: Bearer <IAM-токен>
```

Быстрый способ получить токен для своего аккаунта — через CLI:

```bash
yc iam create-token
```

Инструкции для сервисных, федеративных и локальных аккаунтов: https://yandex.cloud/ru/docs/iam/operations/iam-token/create-for-sa (и соседние страницы раздела). Не путай IAM-токен (управление капчами) с серверным ключом (проверка токена пользователя, см. [validate-api.md](validate-api.md)).

## REST API

Базовый URL: `https://smartcaptcha.api.cloud.yandex.net`

| Метод | Путь | Что делает |
|---|---|---|
| `POST` | `/smartcaptcha/v1/captchas` | Создаёт капчу в каталоге (тело: `folderId`, `name`, опционально `allowedSites`, `complexity`, `styleJson`, `turnOffHostnameCheck`, `preCheckType`, `challengeType`, `securityRules`, `overrideVariants`) |
| `GET` | `/smartcaptcha/v1/captchas?folderId=<id>` | Список капч каталога; `folderId` обязателен, пагинация и фильтры не поддерживаются — возвращаются все капчи |
| `GET` | `/smartcaptcha/v1/captchas/{captchaId}` | Информация о капче (включая `clientKey`) |
| `GET` | `/smartcaptcha/v1/captchas/{captchaId}:getSecretKey` | Серверный ключ; ответ `{"serverKey": "string"}` |
| `PATCH` | `/smartcaptcha/v1/captchas/{captchaId}` | Изменяет капчу |
| `DELETE` | `/smartcaptcha/v1/captchas/{captchaId}` | Удаляет капчу; её ключи прекращают действовать |

В ответах `Get`/`List` есть поле `suspend` (`boolean`) — признак, что капча сейчас в [ограниченном режиме](../docs/troubleshooting.md): удобно для программной диагностики (в ограниченном режиме `/validate` отвечает `ok` даже роботам).

Операции асинхронного API (базовый URL `https://operation.api.cloud.yandex.net`):

| Метод | Путь | Что делает |
|---|---|---|
| `GET` | `/operations/{operationId}` | Статус операции |
| `GET` | `/operations/{operationId}:cancel` | Отмена операции |

## gRPC

Service URL: `https://smartcaptcha.api.cloud.yandex.net`. Определения интерфейсов: https://github.com/yandex-cloud/cloudapi/tree/master/yandex/cloud/smartcaptcha/v1

| Сервис | Методы |
|---|---|
| `CaptchaService` | `Create`, `Get`, `GetSecretKey`, `List`, `Update`, `Delete` |
| `OperationService` | `Get`, `Cancel` |

## CLI: yc smartcaptcha captcha

| Команда | Что делает |
|---|---|
| `yc smartcaptcha captcha create` | Создаёт капчу в каталоге |
| `yc smartcaptcha captcha list` | Список капч каталога |
| `yc smartcaptcha captcha get <имя_или_id>` | Информация о капче (включая `client_key`) |
| `yc smartcaptcha captcha get-secret-key` | Серверный ключ капчи |
| `yc smartcaptcha captcha update <id>` | Изменяет капчу (маска полей — из переданных флагов или `--update-mask`) |
| `yc smartcaptcha captcha delete <имя_или_id>` | Удаляет капчу |

Основные флаги `create`/`update`:

| Флаг | Значение |
|---|---|
| `--name` | Имя капчи, уникально в каталоге |
| `--folder-id` | Каталог (по умолчанию — из профиля CLI) |
| `--allowed-sites` | Список хостов (домены/IP без протокола), работает и на поддоменах |
| `--complexity` | `easy` \| `medium` \| `hard` \| `force-hard` (в примерах документации — `EASY`/`MEDIUM`/`HARD`/`FORCE_HARD`) |
| `--pre-check-type` | `checkbox` \| `slider` |
| `--challenge-type` | `image-text` \| `silhouettes` \| `kaleidoscope` |
| `--style-json` | JSON внешнего вида; для динамической схемы — ключи `light` и `dark` |
| `--turn-off-hostname-check` | Отключить проверку домена |
| `--security-rules`, `--security-rules-file` | Правила показа: shorthand/JSON в аргументе или YAML-файл |
| `--override-variants`, `--override-variants-file` | Варианты заданий: shorthand/JSON или YAML-файл |
| `--deletion-protection` | Защита от удаления |
| `--disallow-data-processing` | Запретить использование данных запросов командой Яндекса |
| `--description`, `--labels` | Описание и метки `ключ:значение` |
| `-r`, `--request-file` | Файл запроса; шаблон: `--example-json` / `--example-yaml` |

Формат YAML-файла вариантов (`--override-variants-file`): список записей `uuid`, `description`, `complexity`, `pre_check_type`, `challenge_type`. Формат файла правил (`--security-rules-file`): список записей `name`, `priority` (1–999999, меньше — приоритетнее), `description`, `override_variant_uuid`, `condition` (по `host` — новый формат `host_matcher`, `uri` (`path`, `queries`), `headers`, `source_ip` — `ip_ranges_match`/`ip_ranges_not_match`/`geo_ip_match`/`geo_ip_not_match`; типы сравнения: `exact_match`, `exact_not_match`, `prefix_match`, `prefix_not_match`, `pire_regex_match`, `pire_regex_not_match`).

## Terraform: yandex_smartcaptcha_captcha

Ресурс `yandex_smartcaptcha_captcha`, ключевые поля:

| Поле | Значение |
|---|---|
| `name` | Имя капчи |
| `complexity` | `EASY` \| `MEDIUM` \| `HARD` \| `FORCE_HARD` |
| `pre_check_type` | `CHECKBOX` \| `SLIDER` |
| `challenge_type` | `IMAGE_TEXT` \| `SILHOUETTES` \| `KALEIDOSCOPE` |
| `allowed_sites` | Список хостов |
| `turn_off_hostname_check` | Отключение проверки домена |
| `style_json` | JSON внешнего вида (удобно через `file("style.json")`) |
| `override_variant` | Блок варианта: `uuid`, `description`, `complexity`, `pre_check_type`, `challenge_type` (повторяемый) |
| `security_rule` | Блок правила: `name`, `priority`, `description`, `override_variant_uuid`, `condition` (повторяемый); для условий по хосту используй `host { host_matcher { pire_regex_match = "..." } }` |

Data-источник `yandex_smartcaptcha_captcha` (аргумент `captcha_id`) возвращает параметры капчи, включая `client_key`. Документация провайдера: ресурс — https://terraform-provider.yandexcloud.net/Resources/smartcaptcha_captcha, data-источник — https://terraform-provider.yandexcloud.net/Data%20Sources/smartcaptcha_captcha

### Ключи style_json

Пример стандартной цветовой схемы из официальной документации (те же ключи можно скопировать в формате JSON из консоли, вкладка **JSON** в настройках внешнего вида):

```json
{
    "text-color-primary": "#1e1f20",
    "base-background-color": "#c7d0d6",
    "popup-image-container-background-color": "#aab4ba",
    "base-checkbox-background-color": "#5a7080",
    "base-checkbox-background-color-checked": "#5a7080",
    "base-checkbox-border": "2px solid #5a7080",
    "base-checkbox-spin-color": "#5a7080",
    "popup-textinput-background-color": "#c7d0d6",
    "popup-action-button-background-color": "#5a7080",
    "popup-action-button-background-color-hover": "#485863"
}
```

Для динамической схемы оберни объекты в ключи `light` и `dark`: `{"light": {...}, "dark": {...}}`. Ещё один документированный ключ — `focus-color`.

## Пример: создание капчи через curl

```bash
# Создание капчи с правилом показа (новый формат hostMatcher); подробности — ../docs/captcha-management.md
curl -X POST \
  'https://smartcaptcha.api.cloud.yandex.net/smartcaptcha/v1/captchas' \
  -H "Authorization: Bearer $(yc iam create-token)" \
  -H 'Content-Type: application/json' \
  -d '{
    "folderId": "<идентификатор_каталога>",
    "name": "captcha",
    "securityRules": [
      {
        "name": "captcha-rule",
        "priority": 1,
        "condition": {
          "host": {
            "hostMatcher": {
              "pireRegexMatch": "a|b"
            }
          }
        }
      }
    ]
  }'
```

## См. также

* [../docs/captcha-management.md](../docs/captcha-management.md) — инструкции по созданию, обновлению, удалению; роли, мониторинг, аудит.
* [../docs/captcha-settings.md](../docs/captcha-settings.md) — семантика типов заданий и правил показа.
* [validate-api.md](validate-api.md) — проверка токена пользователя (`/validate`, серверный ключ).
* Официальная документация: [REST API](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/), [аутентификация в API](https://yandex.cloud/ru/docs/smartcaptcha/api-ref/authentication), [справочник Terraform](https://yandex.cloud/ru/docs/smartcaptcha/tf-ref), [миграция формата условий](https://yandex.cloud/ru/docs/smartcaptcha/operations/api-migration).
