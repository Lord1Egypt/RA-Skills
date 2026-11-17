---
name: web-push-go
description: >-
  Send Web Push notifications from a Go backend using webpush-go (VAPID
  authentication, payload encryption, subscription storage, and browser
  subscribe flow). Use when working with Push API subscriptions in Go,
  Web Push Protocol, VAPID key management, browser push notifications, or
  migrating a Node web-push implementation to Go. Covers VAPID key
  generation, encrypting payloads, the aes128gcm encoding, subscription
  persistence in Postgres, and the browser-side subscribe code.
license: MIT
user-invocable: true
metadata:
  author: monaxamo
  version: "1.0.0"
  category: backend
  topics:
    - webpush
    - golang
    - vapid
    - pwa
    - notifications
---

# Web Push Notifications (Go)

Отправка push-уведомлений в браузеры (Chrome, Firefox, Edge, Safari) из
Go-бэкенда через библиотеку `github.com/SherClockHolmes/webpush-go`:
аутентификация VAPID, шифрование payload по Message Encryption for Web Push,
хранение подписок и подписка на стороне браузера.

Это Go-версия навыка `web-push` (Node.js). Выбирай её, когда бэкенд на Go.

## When to Apply

- Отправка push из Go-сервиса (Push API, VAPID, web-push-go).
- Миграция с Node.js-реализации `web-push` на Go.
- Хранение подписок в Postgres и рассылка по расписанию.
- Подписка в браузере через Service Worker.

## Quick Start

```go
import (
    "encoding/json"
    "log"
    "net/http"

    "github.com/SherClockHolmes/webpush-go"
)

func send(sub webpush.Subscription, payload []byte) error {
    vapidPublic := "BNc..."   // из конфигурации, генерируются ОДИН раз
    vapidPrivate := "q1tX..."
    subject := "mailto:admin@example.org"

    _, err := webpush.SendNotification(sub, payload, &webpush.Options{
        VAPIDPublicKey:  vapidPublic,
        VAPIDPrivateKey: vapidPrivate,
        Subscriber:      subject,
        TTL:             3600,
        Urgency:         webpush.UrgencyNormal,
    })
    return err
}
```

`webpush.SendNotification` сам шифрует payload, формирует заголовки
`Authorization` (VAPID) и `Crypto-Key`, ставит `Content-Encoding:
aes128gcm` и сам отправляет POST на endpoint подписки.

## Core Workflows

### 1. Сгенерировать VAPID-ключи (один раз, навсегда)

```go
privateKey, publicKey, err := webpush.GenerateVAPIDKeys()
if err != nil {
    log.Fatal(err)
}
fmt.Println("public:", publicKey)   // отдаём в браузер
fmt.Println("private:", privateKey)  // храним в секретах сервера
```

**Критично:** ключи генерируются ОДИН раз и хранятся постоянно.
Перегенерация ломает все существующие подписки — браузеры продолжают
присылать старую public key, а сервер подписывает новой, и push не
доходит.

### 2. Подписаться в браузере

```javascript
// service-worker.js
const publicKey = '<VAPID public key (URL-safe base64)>';

self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  event.waitUntil(
    self.registration.showNotification(data.title || 'Уведомление', {
      body: data.body || '',
      icon: '/icons/icon-192.png',
      badge: '/icons/badge-96.png',
      tag: data.tag || undefined,
      data: { url: data.url || '/' },
    })
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(clients.openWindow(event.notification.data?.url || '/'));
});
```

```javascript
// страница подписки
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map((c) => c.charCodeAt(0)));
}

async function subscribe() {
  const reg = await navigator.serviceWorker.register('/service-worker.js');
  const sub = await reg.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
  });
  await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sub),
  });
}
```

Публичный VAPID-ключ отдаётся клиенту как константа или через
`/api/push/key` — он не секрет.

### 3. Принять и сохранить подписку

```go
type Subscription struct {
    ID        string    `json:"id"`
    Endpoint  string    `json:"endpoint"`
    P256DH    string    `json:"p256dh"`
    Auth      string    `json:"auth"`
    CreatedAt time.Time `json:"created_at"`
    UserID    string    `json:"user_id"`
}

// POST /api/push/subscribe
func handleSubscribe(w http.ResponseWriter, r *http.Request) {
    var in struct {
        Endpoint string `json:"endpoint"`
        Keys     struct {
            P256DH string `json:"p256dh"`
            Auth   string `json:"auth"`
        } `json:"keys"`
    }
    if err := json.NewDecoder(r.Body).Decode(&in); err != nil {
        http.Error(w, "bad json", http.StatusBadRequest)
        return
    }
    if in.Endpoint == "" || in.Keys.P256DH == "" || in.Keys.Auth == "" {
        http.Error(w, "incomplete subscription", http.StatusBadRequest)
        return
    }
    // webpush-go ждёт JSON-подобную структуру: {"endpoint":..,"keys":{..}}
    raw, _ := json.Marshal(map[string]any{
        "endpoint": in.Endpoint,
        "keys":     map[string]string{"p256dh": in.Keys.P256DH, "auth": in.Keys.Auth},
    })
    var sub webpush.Subscription
    if err := json.Unmarshal(raw, &sub); err != nil {
        http.Error(w, "bad subscription", http.StatusBadRequest)
        return
    }
    // ... сохранить в Postgres: endpoint уникален, апсерт по endpoint
    w.WriteHeader(http.StatusNoContent)
}
```

### 4. Отправить одному подписчику

```go
sub := webpush.Subscription{
    Endpoint: row.Endpoint,
    Keys: webpush.Keys{
        P256DH: row.P256DH,
        Auth:   row.Auth,
    },
}

payload, _ := json.Marshal(map[string]string{
    "title": "Цена упала",
    "body":  "Яндекс Станция Мини 3 — от 7 890 ₽",
    "url":   "/prices/mini3",
    "tag":   "price-mini3",
})

_, err := webpush.SendNotification(sub, payload, &webpush.Options{
    VAPIDPublicKey:  cfg.VAPIDPublicKey,
    VAPIDPrivateKey: cfg.VAPIDPrivateKey,
    Subscriber:      "mailto:" + cfg.ContactEmail,
    TTL:             86400,
    Urgency:         webpush.UrgencyHigh,
    Topic:           "price-mini3", // склейка повторов в один
})
```

### 5. Отправить всем (рассылка по расписанию)

```go
func broadcast(ctx context.Context, db *pgxpool.Pool, payload []byte) {
    rows, err := db.Query(ctx, `SELECT endpoint, p256dh, auth FROM push_subscriptions`)
    if err != nil {
        log.Printf("push: выбор подписок: %v", err)
        return
    }
    defer rows.Close()

    var dead []string
    for rows.Next() {
        var endpoint, p256dh, auth string
        if err := rows.Scan(&endpoint, &p256dh, &auth); err != nil {
            continue
        }
        sub := webpush.Subscription{
            Endpoint: endpoint,
            Keys:     webpush.Keys{P256DH: p256dh, Auth: auth},
        }
        _, err := webpush.SendNotification(sub, payload, &webpush.Options{
            VAPIDPublicKey:  cfg.VAPIDPublicKey,
            VAPIDPrivateKey: cfg.VAPIDPrivateKey,
            Subscriber:      "mailto:" + cfg.ContactEmail,
            TTL:             3600,
        })
        if err != nil {
            // 404 / 410 → подписка мертва, её надо удалить
            if isGone(err) {
                dead = append(dead, endpoint)
            }
            continue
        }
    }
    for _, e := range dead {
        db.Exec(ctx, `DELETE FROM push_subscriptions WHERE endpoint = $1`, e)
    }
}
```

## Опции `webpush.Options`

| Поле | Тип | Назначение |
|---|---|---|
| `VAPIDPublicKey` | string | публичный ключ, сгенерированный один раз |
| `VAPIDPrivateKey` | string | приватный ключ для подписи |
| `Subscriber` | string | контакт: `mailto:` или `https:` |
| `TTL` | int | сколько секунд push-сервис хранит сообщение (по умолчанию 4 недели) |
| `Urgency` | string | `very-low` \| `low` \| `normal` \| `high` |
| `Topic` | string | до 32 URL-safe символов: склеивает повторы в одно уведомление |
| `RecordSize` | uint32 | размер записи шифрования |
| `Subscriber` | string | см. выше |

## Удаление мёртвых подписок

Push-сервисы возвращают **404** или **410**, когда подписка отозвана или
просрочена. Их нужно удалять, иначе рассылка будет бить в мёртвые
endpoint'ы и тратить время. Проверяй `resp.StatusCode` из ошибки.

## Хранение подписок в Postgres

```sql
CREATE TABLE push_subscriptions (
    id          BIGSERIAL PRIMARY KEY,
    endpoint    TEXT NOT NULL UNIQUE,
    p256dh      TEXT NOT NULL,
    auth        TEXT NOT NULL,
    user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX push_subscriptions_user_idx ON push_subscriptions (user_id);
```

UNIQUE по `endpoint` — апсерт работает как «подписался повторно» без
дубликатов. `ON DELETE CASCADE` чистит подписки вместе с пользователем.


## Безопасность: проверяй эндпоинт перед отправкой

Push-эндпоинт приходит от браузера подписчика, а сервер делает к нему
POST. Если адрес не проверять, подписчик может заставить сервер ходить
во внутреннюю сеть (SSRF) или на свой ресурс. Перед каждой отправкой
проверяй эндпоинт:

```go
// pushAllowlist — известные push-сервисы. Эндпоинт ДОЛЖЕН быть из этого списка.
var pushAllowlist = []string{
    "fcm.googleapis.com",      // Chrome / Android
    "updates.push.services.mozilla.com", // Firefox
    "wns2-*.notify.windows.com",         // Edge / Windows
    "api.push.apple.com",                // Safari на iOS/macOS
}

func safeEndpoint(endpoint string) bool {
    u, err := url.Parse(endpoint)
    if err != nil || u.Scheme != "https" {
        return false
    }
    host := strings.ToLower(u.Hostname())
    // отсекаем внутренние адреса, даже если хост случайно подставили
    if ip := net.ParseIP(host); ip != nil {
        if ip.IsLoopback() || ip.IsPrivate() || ip.IsLinkLocalUnicast() ||
                ip.IsUnspecified() {
            return false
        }
    }
    if host == "localhost" || strings.HasSuffix(host, ".localhost") ||
            host == "169.254.169.254" {   // metadata облака
        return false
    }
    for _, allowed := range pushAllowlist {
        if host == allowed || strings.HasSuffix(host, "."+allowed) {
            return true
        }
    }
    return false
}

// при отправке
if !safeEndpoint(sub.Endpoint) {
    log.Printf("push: отклонён эндпоинт %q", sub.Endpoint)
    return errors.New("endpoint not allowed")
}
```

Правила, которые следуют из этого:

- **Только HTTPS.** Схема `http://` отклоняется до проверки хоста.
- **Только известные push-сервисы.** Эндпоинт не из allowlist — не
  отправляем, а удаляем подписку: она всё равно нерабочая.
- **Никаких редиректов на другой хост.** Клиент push-сервиса не должен
  перенаправлять на внутренний адрес; при 3xx-ответе подписку считаем
  битой.
- **Таймаут и лимит тела.** Запрос к эндпоинту — с таймаутом (5–10 с) и
  без передачи ответа тела в ответ клиенту.
- **Подписки — чувствительные данные.** Эндпоинт привязан к конкретному
  браузеру, поэтому храни его как персональные данные: ограничь доступ к
  таблице, не отдавай эндпоинты в публичные выгрузки, удаляй их вместе с
  учётной записью пользователя.

Ограничение allowlist поднимает ставку: новый push-сервис придётся
добавлять явно. Это осознанный размен — безопасность важнее того, чтобы
навык работал с любым адресом без правок.

## Critical Pitfalls

- **VAPID-ключи генерируются ОДИН раз.** Перегенерация ломает все
  существующие подписки безвозвратно.
- **Safari + localhost:** Safari отклоняет VAPID с `BadJwtToken`, если
  subject — `https://localhost`. Используй `mailto:`.
- **Подписка обязана содержать `keys.p256dh` и `keys.auth`.** Без них
  работает только пустой payload. Если ключей нет — не отправляй, а
  попроси браузер переподписаться.
- **Кодировка:** `aes128gcm` (по умолчанию) для современных браузеров;
  `aesgcm` — только для Chrome < 50 и Opera.
- **Service Worker обязателен:** `pushManager.subscribe()` без
  зарегистрированного SW бросает ошибку.
- **Safari на iOS:** WebPush работает только для PWA, добавленной на
  главный экран, и только с iOS 16.4+. Нативное приложение для
  гарантированного пуша — отдельная задача.

| Эндпоинт подписчика ведёт во внутреннюю сеть | Проверки хоста нет | Проверять эндпоинт по allowlist ДО отправки |

## Browser Compatibility

| Браузер | Пустой payload | Payload с данными | VAPID |
|---|---|---|---|
| Chrome | v42+ | v50+ | v52+ |
| Edge | v17+ | v17+ | v17+ |
| Firefox | v44+ | v44+ | v46+ |
| Safari | v16+ (macOS 13) | v16+ | v16+ |
| Opera | v39+ (Android) | v39+ (Android) | ✗ |
| Samsung Internet | v4+ | v5+ | ✗ |

## Migrating from Node.js `web-push`

| Node (`web-push`) | Go (`webpush-go`) |
|---|---|
| `webpush.generateVAPIDKeys()` | `webpush.GenerateVAPIDKeys()` |
| `webpush.setVapidDetails(...)` | передавать ключи в `webpush.Options` |
| `webpush.sendNotification(sub, payload, opts)` | `webpush.SendNotification(sub, payload, opts)` |
| `opts.TTL` | `Options.TTL` |
| `opts.urgency` | `Options.Urgency` |
| `opts.topic` | `Options.Topic` |
| `opts.contentEncoding` | `Options.Encoding` (`webpush.EncodingAES128GCM`) |
| `webpush.encrypt(...)` | `webpush.EncryptPayload(...)` |

Ключи VAPID совместимы: URL-safe base64, те же значения переносятся
между реализациями без конвертации.

## Минимальный go.mod

```
require github.com/SherClockHolmes/webpush-go v1.4.0
```

## Проверка

- Подписка принята и сохранена: в таблице `push_subscriptions` есть строка
  с непустыми `p256dh` и `auth`.
- Push доставлен: `SendNotification` вернул nil и код 201 от push-сервиса.
- Мёртвая подписка: после 404/410 запись удалена из таблицы.
- Повторная подписка не создаёт дубль: UNIQUE по `endpoint` отрабатывает.

## References

- `references/go-api.md` — построчный разбор API `webpush-go`: типы,
  опции, шифрование, обработка ошибок и статусов ответа.
- `references/browser-side.md` — Service Worker, подписка, показа уведомления,
  поведение на iOS и в режиме «не беспокоить».
