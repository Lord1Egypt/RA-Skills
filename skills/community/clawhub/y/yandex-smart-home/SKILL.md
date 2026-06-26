---
name: yandex-smart-home
description: "Управление устройствами умного дома Яндекса (Алиса) через официальный IoT API. Позволяет получать список устройств, читать их состояние, включать/выключать и управлять параметрами (яркость, температура, режимы и т.д.), а также запускать сценарии. Требует переменную окружения YANDEX_IOT_TOKEN с OAuth-токеном Яндекса."
---

# Yandex Smart Home Skill

Управление устройствами умного дома Яндекса через API `https://api.iot.yandex.net`.

---

## Требования

- Переменная окружения **`YANDEX_IOT_TOKEN`** — OAuth-токен Яндекса с правами `iot:view` и `iot:control`.
- Утилита **`curl`** (есть в большинстве систем по умолчанию).

### Как получить токен

1. Зайдите на https://oauth.yandex.ru/client/new
2. Создайте приложение, выберите платформу «Веб-сервисы»
3. В разделе «Доступы» добавьте `iot:view` и `iot:control`
4. После создания получите отладочный токен по ссылке:
   `https://oauth.yandex.ru/authorize?response_type=token&client_id=<ВАШ_CLIENT_ID>`
5. Установите токен в конфиге OpenClaw:
   ```
   YANDEX_IOT_TOKEN=y0_AgAAAA...
   ```

---

## API Base

```
BASE_URL=https://api.iot.yandex.net/v1.0
AUTH=Authorization: Bearer $YANDEX_IOT_TOKEN
```

---

## Операции

### 1. Получить все устройства, комнаты и сценарии

Используй эту команду в начале, чтобы узнать ID устройств:

```bash
curl -s -X GET "$BASE_URL/user/info" \
  -H "$AUTH" | python3 -m json.tool
```

Ответ содержит:
- `devices[]` — список всех устройств с полями `id`, `name`, `type`, `capabilities[]`, `properties[]`
- `rooms[]` — комнаты с устройствами внутри
- `scenarios[]` — сценарии с `id` и `name`
- `groups[]` — группы устройств

**Всегда начинай с этого запроса**, если пользователь не указал конкретный ID устройства.

---

### 2. Получить состояние конкретного устройства

```bash
curl -s -X GET "$BASE_URL/devices/{DEVICE_ID}" \
  -H "$AUTH" | python3 -m json.tool
```

Возвращает текущее состояние всех `capabilities` (умений) и `properties` (свойств, например температура датчика).

---

### 3. Управление устройством (отправить команду)

```bash
curl -s -X POST "$BASE_URL/devices/actions" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "devices": [
      {
        "id": "{DEVICE_ID}",
        "actions": [
          {
            "type": "{CAPABILITY_TYPE}",
            "state": {
              "instance": "{INSTANCE}",
              "value": {VALUE}
            }
          }
        ]
      }
    ]
  }' | python3 -m json.tool
```

---

### 4. Управление группой устройств

```bash
curl -s -X POST "$BASE_URL/groups/{GROUP_ID}/actions" \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [
      {
        "type": "{CAPABILITY_TYPE}",
        "state": {
          "instance": "{INSTANCE}",
          "value": {VALUE}
        }
      }
    ]
  }' | python3 -m json.tool
```

---

### 5. Запустить сценарий

```bash
curl -s -X POST "$BASE_URL/scenarios/{SCENARIO_ID}/actions" \
  -H "$AUTH" | python3 -m json.tool
```

---

## Справочник умений (capabilities)

### Включение/выключение — `devices.capabilities.on_off`

```json
{
  "type": "devices.capabilities.on_off",
  "state": {
    "instance": "on",
    "value": true
  }
}
```

- `value: true` — включить
- `value: false` — выключить

---

### Яркость — `devices.capabilities.range` (instance: `brightness`)

```json
{
  "type": "devices.capabilities.range",
  "state": {
    "instance": "brightness",
    "value": 70
  }
}
```

- `value` — от 0 до 100 (проценты)

---

### Цветовая температура — `devices.capabilities.color_setting` (instance: `temperature_k`)

```json
{
  "type": "devices.capabilities.color_setting",
  "state": {
    "instance": "temperature_k",
    "value": 4000
  }
}
```

- Тёплый свет: ~2700K, нейтральный: ~4000K, холодный: ~6500K

---

### Цвет RGB — `devices.capabilities.color_setting` (instance: `rgb`)

```json
{
  "type": "devices.capabilities.color_setting",
  "state": {
    "instance": "rgb",
    "value": 16711680
  }
}
```

- `value` — цвет в десятичном формате RGB (16711680 = красный #FF0000)
- Для перевода: R×65536 + G×256 + B

---

### Температура (термостат) — `devices.capabilities.range` (instance: `temperature`)

```json
{
  "type": "devices.capabilities.range",
  "state": {
    "instance": "temperature",
    "value": 22
  }
}
```

---

### Режим работы — `devices.capabilities.mode`

```json
{
  "type": "devices.capabilities.mode",
  "state": {
    "instance": "program",
    "value": "auto"
  }
}
```

Значения `instance`: `program`, `work_speed`, `fan_speed`, `heat`, `clean`, `swing`  
Конкретные значения `value` зависят от устройства — смотри в ответе `/user/info`.

---

### Произвольное переключение — `devices.capabilities.toggle`

```json
{
  "type": "devices.capabilities.toggle",
  "state": {
    "instance": "ionization",
    "value": true
  }
}
```

Значения `instance`: `backlight`, `controls_locked`, `ionization`, `keep_warm`, `mute`, `oscillation`, `pause`

---

## Интерпретация пользовательских запросов

| Что сказал пользователь | Что сделать |
|---|---|
| «включи свет в гостиной» | найти устройства типа `light` в комнате с «гостиная» в названии → `on_off: true` |
| «выключи всё» | `on_off: false` для всех активных устройств |
| «сделай свет потеплее» | `color_setting/temperature_k` → уменьшить текущее значение |
| «приглуши лампу до 30%» | `range/brightness → value: 30` |
| «поставь 23 градуса» | `range/temperature → value: 23` |
| «запусти сценарий "Кино"» | найти в `scenarios[]` по имени → POST `/scenarios/{id}/actions` |
| «какие устройства онлайн?» | GET `/user/info` → отфильтровать `online: true` |

---

## Алгоритм выполнения команды

1. Если ID устройства неизвестен — сначала выполни `GET /user/info`, найди нужное устройство по имени или комнате.
2. Проверь, что нужное `capability` есть у устройства в поле `capabilities[]`.
3. Составь и выполни запрос `POST /devices/actions`.
4. Проверь в ответе `action_result.status`:
   - `DONE` — успех, сообщи пользователю.
   - `ERROR` — сообщи код ошибки из `error_code` и `error_message`.

---

## Обработка ошибок

| HTTP-код | Причина | Действие |
|---|---|---|
| 401 | Невалидный токен | Попроси пользователя проверить `YANDEX_IOT_TOKEN` |
| 403 | Нет прав `iot:control` | Токен выдан только с `iot:view`, нужно переполучить |
| 404 | Устройство не найдено | Проверь ID через `/user/info` |
| 429 | Превышен лимит запросов | Подожди несколько секунд и повтори |

---

## Примеры готовых команд

**Включить лампу:**
```bash
curl -s -X POST "https://api.iot.yandex.net/v1.0/devices/actions" \
  -H "Authorization: Bearer $YANDEX_IOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"devices":[{"id":"DEVICE_ID","actions":[{"type":"devices.capabilities.on_off","state":{"instance":"on","value":true}}]}]}'
```

**Выключить и уменьшить яркость одновременно (два действия сразу):**
```bash
curl -s -X POST "https://api.iot.yandex.net/v1.0/devices/actions" \
  -H "Authorization: Bearer $YANDEX_IOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "devices": [{
      "id": "DEVICE_ID",
      "actions": [
        {"type":"devices.capabilities.range","state":{"instance":"brightness","value":30}},
        {"type":"devices.capabilities.on_off","state":{"instance":"on","value":true}}
      ]
    }]
  }'
```

**Список всех устройств с именами и ID:**
```bash
curl -s "https://api.iot.yandex.net/v1.0/user/info" \
  -H "Authorization: Bearer $YANDEX_IOT_TOKEN" | \
  python3 -c "
import json,sys
data=json.load(sys.stdin)
for d in data.get('devices',[]):
    print(f\"{d['name']:<30} id={d['id']}  type={d['type']}  online={d.get('online','?')}\")
"
```
