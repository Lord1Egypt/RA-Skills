# Telegram Post Skill

## Назначение
Отправка сообщений в Telegram-группы через OpenClaw CLI.

## Когда использовать
Используй этот навык, когда Влад просит:
- "Опубликуй в группу"
- "Отправь пост в Telegram"
- "Напиши в группу робототехники"
- "Сделай отчёт о занятии"

## Команда

```bash
openclaw message send --channel telegram --target "<CHAT_ID>" --message "<ТЕКСТ>" [--media "<ПУТЬ>"]
```

## Параметры

| Параметр | Описание | Пример |
|---|---|---|
| `--channel` | Всегда `telegram` | |
| `--target` | ID группы | `-1003856211981` |
| `--message` | Текст сообщения | `"Отчёт о занятии"` |
| `--media` | Путь к фото/видео (опционально) | `/home/larthe/.openclaw/media/inbound/file.jpg` |

## Группы

- `-1003856211981` — **Робототехника 8-11 лет** (основная)
- `-1003829257143` — другая группа
- `-1003879018559` — другая группа

## Примеры

### 1. Текстовое сообщение
```bash
openclaw message send --channel telegram --target "-1003856211981" --message "Напоминание: завтра занятие в 11:50"
```

### 2. Фото с текстом
```bash
openclaw message send --channel telegram --target "-1003856211981" \
  --message "🤖 ОТЧЁТ О ЗАНЯТИИ
📅 Дата: 22 марта 2026
👨‍🏫 Преподаватель: Владислав

📌 ПРОЕКТ: ТАНКИ ИЗ LEGO WeDo 2.0
..." \
  --media "/home/larthe/.openclaw/media/inbound/file_14---a50e3b78-c5cc-4b70-9bc0-a7c362c13cb2.jpg"
```

### 3. Видео
```bash
openclaw message send --channel telegram --target "-1003856211981" \
  --message "📹 Видео с занятия" \
  --media "/home/larthe/.openclaw/media/inbound/IMG_5285.mp4"
```

### 4. Альбом (через API, до 10 фото)
```bash
curl -X POST "https://api.telegram.org/bot8415787322:AAGK4aQCCGei35g9t2ybKhexlR4BdCZs-3M/sendMediaGroup" \
  -F "chat_id=-1003856211981" \
  -F 'media=[{"type":"photo","media":"attach://f1","caption":"Текст"},{"type":"photo","media":"attach://f2"}]' \
  -F "f1=@/home/larthe/.openclaw/media/inbound/file1.jpg" \
  -F "f2=@/home/larthe/.openclaw/media/inbound/file2.jpg"
```

## Медиа-файлы

Папка: `/home/larthe/.openclaw/media/inbound/`

Список файлов:
```bash
ls -la /home/larthe/.openclaw/media/inbound/*.jpg
```

## Важно

✅ Бот имеет **Privacy Mode: Disabled** — видит все сообщения в группах
✅ **groupPolicy: "open"** — может отправлять без упоминания
✅ Бот — админ в группе `-1003856211981`
✅ Gateway запущен на порту 18789

## Проверка статуса

```bash
# Проверить gateway
curl -s http://127.0.0.1:18789/health

# Проверить бота
curl -s "https://api.telegram.org/bot8415787322:AAGK4aQCCGei35g9t2ybKhexlR4BdCZs-3M/getMe"
```
