# webpush-go — API целиком

Построчный разбор `github.com/SherClockHolmes/webpush-go` для бэкенда на Go.
Источник Node-реализации `web-push` перенесён по смыслу; имена и сигнатуры
Go-версии приведены по документации библиотеки.

## Установка

```bash
go get github.com/SherClockHolmes/webpush-go
```

В `go.mod`:
```
require github.com/SherClockHolmes/webpush-go v1.4.0
```

## Типы

### `Subscription`

```go
type Subscription struct {
    Endpoint string `json:"endpoint"`
    Keys     Keys   `json:"keys"`
}

type Keys struct {
    P256DH string `json:"p256dh"`
    Auth   string `json:"auth"`
}
```

Структура повторяет JSON, который присылает браузер
(`PushSubscription.toJSON()`), поэтому её можно разобрать обычным
`json.Unmarshal` без конвертации.

### `Options`

```go
type Options struct {
    VAPIDPublicKey  string
    VAPIDPrivateKey string
    Subscriber      string   // контакт: "mailto:..." или "https://..."
    TTL             int      // секунд; по умолчанию 2419200 (4 недели)
    Urgency         Urgency
    Topic           string   // <= 32 URL-safe символов
    RecordSize      uint32
    Encoding        Encoding
    Subscriber      string
}
```

### `Urgency`

```go
const (
    UrgencyVeryLow Urgency = "very-low"
    UrgencyLow     Urgency = "low"
    UrgencyNormal  Urgency = "normal"
    UrgencyHigh    Urgency = "high"
)
```

### `Encoding`

```go
const (
    EncodingAES128GCM Encoding = "aes128gcm" // по умолчанию
    EncodingAESGCM    Encoding = "aesgcm"    // legacy: Chrome < 50, Opera
)
```

## Функции

### `GenerateVAPIDKeys() (privateKey, publicKey string, err error)`

Генерирует пару ключей в URL-safe base64. Публичный ключ уходит в
браузер как `applicationServerKey`, приватный хранится в секретах.

**Вызывать один раз.** Перегенерация ломает все подписки.

### `SendNotification(s Subscription, message []byte, options *Options) (*http.Response, error)`

Главная функция. Делает всё:

1. берёт `audience` из `scheme://host` endpoint'а;
2. формирует VAPID-заголовок `Authorization: vapid=t=<jwt>,k=<pub>`;
3. если payload непустой — шифрует по RFC 8291 (`aes128gcm`): генерирует
   salt и эфемерную пару ECDH, считает HKDF-ключи, добавляет
   `Content-Encoding`, `Encryption`, `Crypto-Key`;
4. отправляет POST с `TTL` и `Urgency` в заголовках;
5. возвращает ответ push-сервиса.

Возвращённый `*http.Response` нужно закрыть. Код ответа:
- `201` — доставлено;
- `404` / `410` — подписка мертва, удалить;
- `400` — неверные ключи или payload;
- `401` / `403` — проблема с VAPID (чаще всего перегенерированные ключи
  или неверный `Subscriber`).

### `EncryptPayload(message []byte, p256dh, auth string, encoding Encoding) (*Encryption, error)`

Шифрование отдельно, без отправки. Нужно редко — только если нужно
положить зашифрованный payload в свою очередь.

```go
enc, err := webpush.EncryptPayload(
    []byte("привет"),
    sub.Keys.P256DH,
    sub.Keys.Auth,
    webpush.EncodingAES128GCM,
)
// enc.LocalPublicKey, enc.Salt, enc.CipherText
```

### `GenerateVAPIDHeaders(audience, subject, publicKey, privateKey string, expiration time.Duration) (http.Header, error)`

Формирует только VAPID-заголовки без шифрования payload. Полезно для
отладки: сразу видно, валиден ли JWT.


## Безопасность эндпоинта

Push-эндпоинт — это данные, контролируемые подписчиком. Перед отправкой
проверь его: только HTTPS, только хост из allowlist push-сервисов, без
loopback и приватных адресов, без редиректов на другой хост, с таймаутом.
Полный пример проверки — в разделе «Безопасность: проверяй эндпоинт перед
отправкой» файла SKILL.md.

Подписки храни как чувствительные данные: эндпоинт идентифицирует
конкретный браузер, доступ к таблице ограничь, в публичные выгрузки
эндпоинты не попадают.

## Обработка ошибок

```go
resp, err := webpush.SendNotification(sub, payload, opts)
if err != nil {
    log.Printf("push %s: %v", sub.Endpoint, err)
    return
}
defer resp.Body.Close()

switch resp.StatusCode {
case http.StatusCreated:
    // ok
case http.StatusNotFound, http.StatusGone:
    // подписка отозвана или просрочена — удалить из БД
    db.Exec(ctx, `DELETE FROM push_subscriptions WHERE endpoint = $1`, sub.Endpoint)
default:
    log.Printf("push %s: HTTP %d", sub.Endpoint, resp.StatusCode)
}
```

## Генерация ключей через CLI

```bash
go run ./cmd/vapidgen
```

или одна строка:

```bash
cat > /tmp/vapid.go <<'EOF'
package main

import (
	"fmt"
	"github.com/SherClockHolmes/webpush-go"
)

func main() {
	priv, pub, err := webpush.GenerateVAPIDKeys()
	if err != nil {
		panic(err)
	}
	fmt.Println("public:", pub)
	fmt.Println("private:", priv)
}
EOF
go run /tmp/vapid.go
```

## Хранение ключей

Ключи — секрет. В проекте «Зелёный град» инфраструктура использует SOPS:

```bash
sops secrets.yaml > /run/secrets/vapid.yaml
```

В коде:

```go
type Config struct {
    VAPIDPublicKey  string `env:"VAPID_PUBLIC_KEY"`
    VAPIDPrivateKey string `env:"VAPID_PRIVATE_KEY"`
    ContactEmail    string `env:"CONTACT_EMAIL"`
}
```

Публичный ключ можно отдавать клиенту:

```go
func handleKey(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{
        "publicKey": cfg.VAPIDPublicKey,
    })
}
```

## Отправка по расписанию (river)

В проекте очередь — `river`:

```go
func (w *PushWorker) Work(ctx context.Context, job river.Job) error {
    var payload Payload
    if err := json.Unmarshal(job.Args, &payload); err != nil {
        return fmt.Errorf("decode: %w", err)
    }
    return w.mailer.Broadcast(ctx, payload.Title, payload.Body, payload.URL)
}
```

`river` даёт повтор с backoff при временных ошибках и `UnrecoverableError`
для мёртвых подписок — их удаляем, а не повторяем.

## Ограничения Go-версии относительно Node

| Возможность | Node `web-push` | `webpush-go` |
|---|---|---|
| Отправка push | ✔ | ✔ |
| Шифрование aes128gcm | ✔ | ✔ |
| Шифрование aesgcm (legacy) | ✔ | ✔ |
| VAPID-заголовки | ✔ | ✔ |
| `setGCMAPIKey` (legacy Chrome/Opera) | ✔ | ✗ |
| CLI | ✔ | ✗ (свой на Go) |
| Отправка в очередь | вручную | river |

Отсутствие GCM-ключа не страшно: он нужен только для Chrome ≤ 51,
Opera и Samsung Internet — доли в 2026 году пренебрежимо малы.
