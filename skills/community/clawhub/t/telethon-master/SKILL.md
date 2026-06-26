# Telethon Master

Скилл для работы с Telegram MTProto через Telethon Bridge. Предоставляет доступ к 23 инструментам (`telegram_*`) для отправки сообщений, голосовых (ElevenLabs TTS), истории чатов, реакций, файлов, управления каналами и статистики.

Поддерживает **Claude Code** (прямые MCP-вызовы) и **OpenClaw** (через Gateway).

## Когда использовать

- Отправить сообщение через Telegram (не через бота)
- Получить историю чата, список диалогов
- Сгенерировать голосовое (voice note) через ElevenLabs TTS
- Отправить файл или фото
- Поставить реакцию на сообщение
- Получить статистику чата
- Управлять каналами (описание, удаление)
- Скачать медиа из сообщения
- Пользователь спрашивает о работе MCP-инструментов Telethon

## Архитектура

```
Claude Code / OpenClaw
        │
        ▼
MCP Server (telethon-mcp/server.py)  ← HTTP-обёртка над REST API
        │
        ▼
REST API (telethon-bridge/server.py) ← Telethon MTProto + sag (ElevenLabs)
        │
        ▼
SOCKS5 (127.0.0.1:1080) ← SSH-туннель ← VPS (45.13.225.151)
        │
        ▼
Telegram DC
```

- **MCP Server** (`~/.openclaw/mcp-servers/telethon-mcp/server.py`) — тонкая обёртка, HTTP-запросы к REST API
- **REST API** (`~/.openclaw/workspace/general/telethon-bridge/server.py`) — Telethon клиент + sag CLI
- **Сессия:** `session/savant` (SQLite), одна активная сессия
- **Прокси:** SOCKS5 напрямую через SSH-туннель (127.0.0.1:1080)
- **TTS:** sag CLI → ElevenLabs API → MP3 → FFmpeg (Opus OGG) → Telegram voice note
- **Gateway:** `gateway.mjs` (порт 18793) — форвардит входящие от owner в OpenClaw агент
- **Systemd:** `telethon-bridge.service` (user, порт 18792), `telegateway.service` (user, порт 18793)

## Безопасность: ALLOWED_CHAT_IDS

MCP-сервер поддерживает переменную `TG_ALLOWED_CHAT_IDS` — список разрешённых chat_id через запятую. Если переменная установлена, **write-операции** (send, edit, delete, forward, react, click, file, voice, pin, read, audio, circle, channel about/delete, join) разрешены только для указанных чатов.

Установка в `mcp.json`:
```json
"env": {
    "TELEGATEWAY_URL": "http://127.0.0.1:18792",
    "TG_ALLOWED_CHAT_IDS": "me,1144466778,kngserious55"
}
```

Read-операции (messages, chats, search, stats, get_chat, get_photo, get_chatlist, download_media) не ограничены.

## Инструменты (Claude Code MCP)

В Claude Code все инструменты доступны как `mcp__telethon-bridge__<имя>`.

### Сообщения

| Инструмент | Параметры | Описание |
|---|---|---|
| `telegram_send` | `chat_id`, `text` | Отправка текстового сообщения |
| `telegram_edit` | `chat_id`, `msg_id`, `text` | Редактирование сообщения |
| `telegram_delete` | `chat_id`, `msg_ids[]` | Удаление сообщений |
| `telegram_forward` | `from_chat`, `to_chat`, `msg_ids[]` | Пересылка сообщений |
| `telegram_pin` | `chat_id`, `msg_id`, `unpin?` | Закреп/откреп сообщения |

### Чтение

| Инструмент | Параметры | Описание |
|---|---|---|
| `telegram_messages` | `chat_id`, `limit?`, `offset_id?` | История сообщений с пагинацией |
| `telegram_search` | `chat_id`, `query`, `limit?`, `from_user?` | Поиск сообщений |
| `telegram_read` | `chat_id`, `max_id?` | Отметить как прочитанное |

### Чаты и пользователи

| Инструмент | Параметры | Описание |
|---|---|---|
| `telegram_chats` | `limit?` (default 30) | Список диалогов |
| `telegram_get_chat` | `chat_id` | Инфо о чате/канале/пользователе |
| `telegram_me` | — | Инфо о текущем пользователе |
| `telegram_get_photo` | `chat_id?` (default "me") | Скачать фото профиля |
| `telegram_join_chat` | `hash` | Вступить по invite-hash |
| `telegram_get_chatlist` | `slug` | Каналы из t.me/addlist |

### Медиа

| Инструмент | Параметры | Описание |
|---|---|---|
| `telegram_file` | `chat_id`, `file_path`, `caption?` | Отправка файла (документ) |
| `telegram_voice` | `chat_id`, `text`, `voice?` (default "Roger") | Voice note через ElevenLabs |
| `telegram_send_audio` | `chat_id`, `file_path`, `title?`, `performer?` | Аудиофайл с тегами |
| `telegram_send_circle` | `chat_id`, `file_path` | Круглое видео (video note) |
| `telegram_download_media` | `chat_id`, `msg_id` | Скачать медиа в /tmp/bridge_dl/ |

### Интеракции

| Инструмент | Параметры | Описание |
|---|---|---|
| `telegram_react` | `chat_id`, `msg_id`, `reaction` | Реакция (эмодзи или document_id) |
| `telegram_click` | `chat_id`, `msg_id`, `row?`, `col?` | Клик по inline-кнопке |

### Управление каналами

| Инструмент | Параметры | Описание |
|---|---|---|
| `telegram_set_channel_about` | `chat_id`, `text` | Установить описание канала |
| `telegram_delete_channel` | `chat_id` | Удалить канал (только owner) |

### Аналитика

| Инструмент | Параметры | Описание |
|---|---|---|
| `telegram_stats` | `chat_id?` (default "me"), `days?` (default 7) | Статистика чата |

**Важно:** `chat_id` принимает username (`kngserious55`), ID (`1184174498`), или `"me"` для сохранёнок.

## TTS / Voice Notes (ElevenLabs)

### Как это работает

`telegram_voice` вызывает sag CLI, который обращается к ElevenLabs API:

```
sag speak -v <voice> --model-id eleven_multilingual_v2 --format mp3_44100_192 -o <wav> <text>
ffmpeg -i <wav> -c:a libopus -b:a 192k -ar 48000 -ac 1 <ogg>
Telethon send_file(voice_note=True)
```

### Параметры качества (настроены в `server.py`)

| Параметр | Значение |
|---|---|
| Модель | `eleven_multilingual_v2` |
| Формат | `mp3_44100_192` (192 kbps) |
| OGG кодек | Opus 192k, 48000 Hz, mono |

### Доступные голоса (24 шт., ElevenLabs-аккаунт `@savantbeats`)

Голос передаётся напрямую в sag (без маппинга). Имя должно существовать в ElevenLabs-аккаунте.

**Женские:** Sarah, Laura, Alice, Matilda, Jessica, Bella, Lily
**Мужские:** Adam, Roger, Charlie, George, Callum, River, Harry, Liam, Will, Eric, Chris, Brian, Daniel, Bill

### Выбор голоса под задачу

| Задача | Рекомендация |
|---|---|
| Разговорный, casual | Roger, Adam |
| Деловой, профессиональный | Bella, Matilda |
| Яркий, эмоциональный | Jessica, Laura |
| Спокойный, тёплый | Sarah, Lily |

### Устранение проблем

| Ошибка | Причина | Решение |
|---|---|---|
| `500: Internal Server Error` | Голос не существует в аккаунте ElevenLabs | Использовать голос из таблицы выше |
| `500: Voice error: ffmpeg ...` | Неподдерживаемый sample rate | Opus поддерживает: 8000/12000/16000/24000/48000 |
| `sag: missing API key` | `ELEVENLABS_API_KEY` не установлен | Проверить `.env` бриджа |
| `database is locked` | Два клиента Telethon одновременно | Бридж держит одну сессию — не подключаться параллельно |
| `FloodWait` | Бридж автоматически ретраит до 3 раз (capped 60s) | Ждать или уменьшить частоту |

## Быстрые рецепты

### Отправить сообщение

```
mcp__telethon-bridge__telegram_send(chat_id="username", text="Привет!")
```

### Отправить голосовое

```
mcp__telethon-bridge__telegram_voice(chat_id="me", text="Привет, мир!", voice="Jessica")
```

### Получить последние сообщения

```
mcp__telethon-bridge__telegram_messages(chat_id="username", limit=10)
```

### Найти чат по имени

```
mcp__telethon-bridge__telegram_chats(limit=30)
// → ищем в выдаче нужный username/ID
```

### Отправить файл

```
mcp__telethon-bridge__telegram_file(chat_id="username", file_path="/path/to/file.pdf")
```

### Поставить реакцию

```
mcp__telethon-bridge__telegram_react(chat_id="username", msg_id=12345, reaction="🔥")
```

## Claude Code vs OpenClaw

| | Claude Code | OpenClaw |
|---|---|---|
| Вызов инструментов | `mcp__telethon-bridge__<tool>()` | `mcp.call_tool("telethon-bridge", "<tool>", {})` |
| TTS | Через `telegram_voice` | `sag speak` напрямую или `telegram_voice` |
| Доступ к файлам | Прямой (локальная ФС) | Через OpenClaw workspace |
| Перезапуск бриджа | `systemctl --user restart telethon-bridge.service` | Тоже самое |
| Логи бриджа | `journalctl --user -u telethon-bridge.service` | Тоже самое |

## Обслуживание бриджа

```bash
# Статус
systemctl --user status telethon-bridge.service

# Перезапуск (после правок server.py)
systemctl --user restart telethon-bridge.service

# Логи
journalctl --user -u telethon-bridge.service -f

# Ручной запуск (отладка)
cd ~/.openclaw/workspace/general/telethon-bridge
python3 server.py

# Убить зависший процесс
fuser -k 18792/tcp

# Проверить здоровье
curl -s http://127.0.0.1:18792/health
```

## Безопасность и ограничения

| Правило | Описание |
|---|---|
| **Никакого спама** | Не отправлять рекламные сообщения без явного запроса |
| **Чувствительные данные** | Не логировать содержимое сообщений |
| **Rate limiting** | Не более ~30 сообщений в минуту |
| **Приватные чаты** | Не читать ЛС без явного разрешения владельца аккаунта |
| **FLOOD_WAIT** | Бридж ретраит автоматически (до 3 попыток, capped 60s) |
| **ALLOWED_CHAT_IDS** | Ограничивает write-операции заданным списком чатов |

## Референсы

- Telethon Bridge REST API: `~/.openclaw/workspace/general/telethon-bridge/server.py`
- MCP Server: `~/.openclaw/mcp-servers/telethon-mcp/server.py`
- Gateway Bridge: `~/.openclaw/workspace/general/telethon-bridge/gateway.mjs`
- `.env` бриджа: `~/.openclaw/workspace/general/telethon-bridge/.env`
- Systemd unit: `~/.config/systemd/user/telethon-bridge.service`
- ElevenLabs голоса: `ELEVENLABS_API_KEY` в `.env` → `https://api.elevenlabs.io/v1/voices`
- sag CLI: `/home/linuxbrew/.linuxbrew/bin/sag speak --help`
- Формат voice note: OGG Opus, 48000 Hz, mono, 192k
