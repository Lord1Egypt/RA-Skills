# Создание и управление капчей

Читай этот файл, когда нужно создать капчу в Yandex Cloud, получить её ключи, изменить или удалить её, а также настроить доступ, мониторинг и аудит. Типы заданий, сложность и правила показа подробно описаны в [captcha-settings.md](captcha-settings.md); точные endpoint'ы, команды и поля — в [../references/management-api.md](../references/management-api.md).

Капчей управляют четырьмя способами: консоль управления (интерактивно, с предпросмотром внешнего вида), CLI `yc smartcaptcha captcha ...` (скрипты и разовые операции), Terraform-ресурс `yandex_smartcaptcha_captcha` (IaC), REST/gRPC API (автоматизация). Результат одинаковый — выбирай по тому, как вы управляете остальной инфраструктурой.

> **Важно.** Для повышения качества защиты сервис использует информацию об HTTP-запросах для обучения ML-моделей. Это можно отключить при создании капчи (раздел «Обучение ML-моделей» в консоли, флаг `--disallow-data-processing` в CLI).

## Создание капчи

### Консоль управления

1. В [консоли управления](https://console.yandex.cloud) выбери каталог и перейди в сервис **SmartCaptcha**.
2. Нажми **Создать капчу**.
3. Укажи **Имя** (2–63 символа: строчные латинские буквы, цифры, дефисы; первый символ — буква, последний — не дефис).
4. (Опционально) Добавь метки в формате `ключ: значение`.
5. (Опционально) Включи **Отключить проверку домена** — тогда капча будет работать на любом хосте.
6. Введи **Список хостов** — IP-адреса или доменные имена без протокола и без `/` в конце (например, `example.com`). Капча работает и на всех поддоменах указанных доменов.
7. Настрой **Внешний вид**: опция **Динамическая цветовая схема** (автопереключение по теме браузера), стандартная и тёмная схемы — через форму или JSON. Изменения видны в окне предпросмотра. JSON стилей можно скопировать на вкладке `JSON` — он пригодится для CLI/Terraform.
8. Настрой **Варианты заданий**: для варианта **По умолчанию** укажи основное задание, дополнительное задание и сложность. Чтобы показывать разную капчу разным запросам, добавь варианты (**Добавить вариант**) и правила показа (**Добавить правило**): имя, вариант, приоритет `1`–`999999` (проверяются от меньшего к большему, применяется первое сработавшее) и условия по `IP`, `HTTP header`, `URI`, `Host` или `Metadata`. Подробности — в [captcha-settings.md](captcha-settings.md).
9. Нажми **Создать**. Капча появится в разделе **Список капч**.

### CLI

Нужен установленный и инициализированный [Yandex Cloud CLI](https://yandex.cloud/ru/docs/cli/quickstart). Минимальный вариант — только имя:

```bash
yc smartcaptcha captcha create simple-captcha
```

Ответ содержит `id`, `folder_id` и `client_key` (клиентский ключ) — сохрани их. Типовое создание с основными флагами:

```bash
yc smartcaptcha captcha create \
  --name advanced-captcha \
  --turn-off-hostname-check \
  --allowed-sites example.ru,example.kz \
  --style-json "$(cat ./style.json)" \
  --pre-check-type CHECKBOX \
  --challenge-type IMAGE_TEXT \
  --complexity HARD \
  --override-variants-file captcha-variants.yaml \
  --security-rules-file captcha-rules.yaml
```

Ключевые флаги: `--pre-check-type` (`CHECKBOX`, `SLIDER`), `--challenge-type` (`IMAGE_TEXT`, `SILHOUETTES`, `KALEIDOSCOPE`), `--complexity` (`EASY`, `MEDIUM`, `HARD`, `FORCE_HARD`), `--style-json` (JSON стилей; для динамической схемы — ключи `light` и `dark`), `--override-variants-file` и `--security-rules-file` — YAML-файлы с вариантами заданий и правилами показа. Форматы файлов и полный список флагов — в [../references/management-api.md](../references/management-api.md). Шаблон запроса генерируется командой `yc smartcaptcha captcha create --example-yaml > request.yaml`, затем `yc smartcaptcha captcha create -r request.yaml`.

### Terraform

Минимальный конфиг:

```hcl
# Минимальная капча SmartCaptcha; подробности — docs/captcha-management.md
resource "yandex_smartcaptcha_captcha" "simple-captcha" {
  name           = "simple-captcha"
  complexity     = "HARD"
  pre_check_type = "SLIDER"
  challenge_type = "IMAGE_TEXT"
}
```

Типовой конфиг с хостами, вариантом задания и правилами показа:

```hcl
# Капча с вариантами заданий и правилами показа; подробности — docs/captcha-management.md
resource "yandex_smartcaptcha_captcha" "advanced-captcha" {
  name                    = "advanced-captcha"
  turn_off_hostname_check = true
  style_json              = "${file("style.json")}"
  complexity              = "HARD"
  pre_check_type          = "SLIDER"
  challenge_type          = "IMAGE_TEXT"

  allowed_sites = ["example.ru", "example.kz"]

  override_variant {
    uuid           = "variant-1"
    description    = "Simple variant"
    complexity     = "EASY"
    pre_check_type = "CHECKBOX"
    challenge_type = "SILHOUETTES"
  }

  # Условие по хосту — в новом формате host_matcher (см. раздел про миграцию)
  security_rule {
    name                  = "rule-1"
    priority              = 11
    description           = "My first security rule"
    override_variant_uuid = "variant-1"

    condition {
      host {
        host_matcher {
          pire_regex_match = "example\\.com|example\\.net"
        }
      }
    }
  }

  security_rule {
    name                  = "rule-2"
    priority              = 12
    override_variant_uuid = "variant-1"

    condition {
      source_ip {
        geo_ip_match {
          locations = ["ru", "kz"]
        }
      }
    }
  }
}
```

Примени стандартно: `terraform validate` → `terraform plan` → `terraform apply` (подтверди вводом `yes`). Проверь результат: `yc smartcaptcha captcha list`.

### REST API

Создание — метод `Captcha.Create`, POST с IAM-токеном (как его получить — в [../references/management-api.md](../references/management-api.md)):

```bash
curl -X POST \
  'https://smartcaptcha.api.cloud.yandex.net/smartcaptcha/v1/captchas' \
  -H "Authorization: Bearer $(yc iam create-token)" \
  -H 'Content-Type: application/json' \
  -d '{
    "folderId": "<идентификатор_каталога>",
    "name": "simple-captcha"
  }'
```

В теле поддерживаются те же настройки, что и в CLI/Terraform, в camelCase: `allowedSites`, `complexity`, `styleJson`, `turnOffHostnameCheck`, `preCheckType`, `challengeType`, `securityRules`, `overrideVariants`. Есть и gRPC-вызов `CaptchaService/Create`.

## Список, информация, ключи

* **Список капч**: консоль — страница **Список капч** в каталоге; CLI — `yc smartcaptcha captcha list` (таблица с ID, NAME, COMPLEXITY, типами заданий, числом правил); API — `GET /smartcaptcha/v1/captchas?folderId=...` (пагинация и фильтры не поддерживаются — возвращаются все капчи каталога).
* **Информация о капче**: консоль — страница **Обзор** капчи; CLI — `yc smartcaptcha captcha get <имя_или_идентификатор>`; API — `GET /smartcaptcha/v1/captchas/{captchaId}`; Terraform — data-источник `yandex_smartcaptcha_captcha` c `captcha_id` и блоком `output`.
* **Ключи**: консоль — вкладка **Обзор**, поля **Ключ клиента** и **Ключ сервера**. Клиентский ключ (`client_key`) возвращается в ответах `create`/`get`/`list`; серверный ключ выдаётся отдельным вызовом `GetSecretKey` (`GET /smartcaptcha/v1/captchas/{captchaId}:getSecretKey` → `{"serverKey": "..."}`) или командой `yc smartcaptcha captcha get-secret-key`, потому что это секрет — храни его только на сервере. Назначение и безопасность ключей — в [keys.md](keys.md).

## Обновление капчи

Консоль — измени настройки на странице капчи. CLI — `yc smartcaptcha captcha update <идентификатор_капчи>` с теми же флагами, что и у `create`; маска обновляемых полей строится из переданных флагов, при необходимости задай её явно через `--update-mask`. Terraform — измени конфигурацию и выполни `terraform apply`. API — `PATCH /smartcaptcha/v1/captchas/{captchaId}` (метод `Captcha.Update`). Флаг `--deletion-protection` включает защиту капчи от удаления.

## Удаление капчи

> **Важно.** Ключи удалённой капчи сразу прекращают действовать: сервис вернёт ошибку на все запросы с этими ключами. Сначала убери виджет и проверку с сайта или переключи их на другую капчу.

* Консоль: выбери капчу → меню **...** → **Удалить** → подтверди.
* CLI: `yc smartcaptcha captcha delete <имя_или_идентификатор_капчи>`.
* Terraform: удали блок `resource "yandex_smartcaptcha_captcha"` из конфигурации и выполни `terraform apply`.
* API: `DELETE /smartcaptcha/v1/captchas/{captchaId}` (метод `Captcha.Delete`).

## Роли доступа

Роли назначаются на организацию, облако или каталог и наследуются капчами внутри них. Используй сервисные роли вместо примитивных (`viewer`/`editor`/`admin`) — это соответствует принципу минимальных привилегий. Каждая роль включает разрешения предыдущей:

| Роль | Что добавляет |
|---|---|
| `smart-captcha.auditor` | Просмотр информации о капчах и назначенных правах доступа |
| `smart-captcha.viewer` | + получение ключей капчи |
| `smart-captcha.editor` | + создание, изменение и удаление капч |
| `smart-captcha.admin` | + управление правами доступа к капчам |

Минимальные роли по действиям: просмотр информации — `smart-captcha.viewer`; создание, редактирование, удаление — `smart-captcha.editor`; управление ролями пользователей на капче — `smart-captcha.admin`. Сервисному аккаунту бэкенда, которому нужен только серверный ключ, достаточно `smart-captcha.viewer`.

## Мониторинг

SmartCaptcha поставляет метрики в Yandex Monitoring (тип `IGAUGE`, штуки; метки `service=smartcaptcha` и `captcha=<идентификатор_капчи>`):

* показы и решения основного задания: `smartcaptcha.captcha.precheck.shows|success_count|failed_count` (агрегированно), а также отдельно `checkbox.shows|success_count|failed_count` и `slider.shows|success_count`;
* решения дополнительного задания: `smartcaptcha.captcha.advanced.success_count|failed_count|refresh_count` (агрегированно), отдельно `image.success_count|failed_count|refresh_count`, `silhouette.success_count|failed_count`, `kaleidoscope.success_count|failed_count`;
* серверная валидация: `smartcaptcha.captcha.validate.success_count|failed_count` — следи за ней: рост `failed_count` может означать повторное использование токенов или атаку.

## Аудитные логи

Audit Trails отслеживает события уровня конфигурации (Control Plane): `CreateCaptcha`, `UpdateCaptcha`, `DeleteCaptcha`. Тип события: `yandex.cloud.audit.audit.smartcaptcha.<имя_события>`. Кроме того, все действия с ресурсами сохраняются как список операций: консоль → SmartCaptcha → **Операции** (включая операции над уже удалёнными ресурсами).

## Миграция формата условий (host_matcher)

С 9 июня 2026 года сервис перешёл на новый формат условий по хосту в правилах показа — это важно, если ты задаёшь `security_rules` через API, CLI или Terraform:

* поле `hosts` (список условий) переименовано в `host_matcher` (одно условие);
* несколько значений объединяются в одно текстовое поле через `|`: вместо списка `example.com`, `example.net` — `pire_regex_match = "example\\.com|example\\.net"` (в API — `"pireRegexMatch"`);
* разные типы условий старого формата (`exact_match` + `exact_not_match` и т. п.) объединяются в одно регулярное выражение; `~` — логическое отрицание, например `"example\.com|~(example\.net)"`;
* специальные символы `( ) { } [ ] . * + ? ^ $ | \ & ~`, используемые как обычные, экранируй через `\`.

Правила, созданные в старом формате, перенесены автоматически и продолжают работать, но новые конфигурации пиши в новом формате. Перед использованием обнови CLI: `yc components update`, форматы полей смотри в `yc smartcaptcha captcha create -h`.

## См. также

* [../references/management-api.md](../references/management-api.md) — таблицы endpoint'ов, команд CLI и полей Terraform.
* [captcha-settings.md](captcha-settings.md) — типы заданий, сложность, варианты и правила показа, домены.
* [keys.md](keys.md) — ключ клиента и ключ сервера: использование и безопасность.
* [../workflows/setup-captcha.md](../workflows/setup-captcha.md) — пошаговый сценарий создания и настройки капчи.
* Официальная документация: [создание капчи](https://yandex.cloud/ru/docs/smartcaptcha/operations/create-captcha), [удаление](https://yandex.cloud/ru/docs/smartcaptcha/operations/delete-captcha), [роли](https://yandex.cloud/ru/docs/smartcaptcha/security/), [метрики](https://yandex.cloud/ru/docs/smartcaptcha/metrics), [аудитные логи](https://yandex.cloud/ru/docs/smartcaptcha/at-ref), [миграция условий](https://yandex.cloud/ru/docs/smartcaptcha/operations/api-migration).
