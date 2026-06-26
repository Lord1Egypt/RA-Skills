# web-push Complete API Reference

## Installation & Configuration

```bash
npm install web-push --save
```

## sendNotification(pushSubscription, payload?, options?)

Core method for sending Web Push notifications. Automatically handles payload encryption and VAPID authentication headers.

```javascript
const webpush = require('web-push');

const pushSubscription = {
  endpoint: '<Push Endpoint URL>',
  keys: {
    p256dh: '<User Public Key>',
    auth: '<Authentication Secret>'
  }
};

await webpush.sendNotification(
  pushSubscription,
  payload,   // string | Buffer | null
  options     // optional
);
```

### Parameter: pushSubscription

JSON serialized result from the browser's `PushSubscription`, containing:
- `endpoint`: Endpoint URL of the push service
- `keys.p256dh`: User public key (for encryption)
- `keys.auth`: Authentication secret (for encryption)

### Parameter: payload (optional)

Push data, either `string` or Node.js `Buffer`. If this parameter is set, the PushSubscription must contain the `keys` object.

### Parameter: options (optional)

| Option | Type | Description |
|--------|------|-------------|
| `vapidDetails` | `{ subject, publicKey, privateKey }` | Override global VAPID configuration |
| `gcmAPIKey` | `string` | GCM API key (legacy browsers) |
| `TTL` | `number` | Push retention seconds (default 4 weeks = 2419200) |
| `contentEncoding` | `'aes128gcm'` \| `'aesgcm'` | Encryption encoding (default `aes128gcm`) |
| `urgency` | `'very-low'` \| `'low'` \| `'normal'` \| `'high'` | Urgency level |
| `topic` | `string` | Notification identifier for coalescing, max 32 characters |
| `timeout` | `number` | Request timeout in milliseconds |
| `proxy` | `string` \| `object` | HTTP proxy server |
| `agent` | `https.Agent` | Custom HTTPS Agent (mutually exclusive with proxy) |
| `headers` | `object` | Additional HTTP request headers |

### Return Value

Promise that resolves on success and rejects on failure. The following are accessible in both cases:
- `statusCode` — HTTP status code
- `headers` — Response headers
- `body` — Response body

### Notes

- Safari 16+: VAPID `subject` cannot be `https://localhost`, otherwise returns `BadJwtToken`
- If the push subscription does not contain a `keys` object, only empty payload can be sent

---

## generateVAPIDKeys()

Generates a URL-Safe Base64 encoded VAPID key pair.

```javascript
const vapidKeys = webpush.generateVAPIDKeys();
// vapidKeys.publicKey  — URL Base64 public key, used as applicationServerKey
// vapidKeys.privateKey — URL Base64 private key, used for server-side signing
```

- **No parameters**
- **Generate only once and persist** — regenerating will break existing subscriptions

---

## setVapidDetails(subject, publicKey, privateKey)

Globally sets VAPID configuration. All subsequent `sendNotification()` and `generateRequestDetails()` calls will use it.

```javascript
webpush.setVapidDetails(
  'mailto:user@example.org',   // mailto: or https: URI
  process.env.VAPID_PUBLIC_KEY,
  process.env.VAPID_PRIVATE_KEY
);
```

- `subject`: Contact address (`mailto:` or `https:`)
- `publicKey`: VAPID public key
- `privateKey`: VAPID private key

---

## setGCMAPIKey(apiKey)

Sets the GCM API key (required for legacy Chrome/Opera/Samsung Internet browsers).

```javascript
webpush.setGCMAPIKey('<Your GCM API Key Here>');
```

Obtain from Google Developer Console or the Cloud Messaging page of a Firebase project.

---

## encrypt(userPublicKey, userAuth, payload, contentEncoding)

Manually encrypts the push payload (`sendNotification` already calls this internally, manual use is generally not needed).

```javascript
const encrypted = await webpush.encrypt(
  pushSubscription.keys.p256dh,
  pushSubscription.keys.auth,
  'My Payload',
  'aes128gcm'    // or 'aesgcm'
);
// → { localPublicKey, salt, cipherText: Buffer }
```

---

## getVapidHeaders(audience, subject, publicKey, privateKey, contentEncoding, expiration?)

Manually generates VAPID Authorization and Crypto-Key request headers.

```javascript
const parsedUrl = require('url').parse(subscription.endpoint);
const audience = parsedUrl.protocol + '//' + parsedUrl.hostname;

const vapidHeaders = webpush.getVapidHeaders(
  audience,
  'mailto:example@web-push-node.org',
  vapidDetails.publicKey,
  vapidDetails.privateKey,
  'aes128gcm'
);
```

---

## generateRequestDetails(pushSubscription, payload?, options?)

Generates raw HTTPS request details for use with custom network requests. Does not send the request.

```javascript
const details = webpush.generateRequestDetails(
  pushSubscription,
  payload,    // string | Buffer (optional)
  {           // Same options as sendNotification
    vapidDetails: { ... },
    contentEncoding: 'aesgcm',
    TTL: 60
  }
);
// → { endpoint, method: 'POST', headers, body: Buffer }
```

> When payload is null, no body is generated and encryption-related headers are excluded.

---

## Command Line Usage

```bash
# Installation
npm install web-push -g
```

```bash
# Generate VAPID keys
web-push generate-vapid-keys --json

# Send push notification
web-push send-notification \
  --endpoint=https://fcm.googleapis.com/fcm/send/... \
  --key=<p256dh> \
  --auth=<auth_secret> \
  --payload="Message content" \
  --vapid-subject=mailto:example@qq.com \
  --vapid-pubkey=<VAPID public key> \
  --vapid-pvtkey=<VAPID private key> \
  --ttl=3600 \
  --encoding=aes128gcm \
  --gcm-api-key=<GCM key>
```

---

## Client-Side Subscription

```javascript
// Browser-side Service Worker
const publicKey = '<VAPID public key (URL Base64)>';

registration.pushManager.subscribe({
  userVisibleOnly: true,
  applicationServerKey: publicKey
}).then(subscription => {
  // Send subscription.toJSON() to backend for storage
  fetch('/api/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription)
  });
});
```

```javascript
// Helper function to convert URL Base64 VAPID public key to Uint8Array
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}
```

---

## Browser Compatibility

| Browser | Empty Payload | Payload with Data | VAPID | Notes |
|---------|---------------|-------------------|-------|-------|
| Chrome | v42+ | v50+ | v52+ | v51 and below require gcm_sender_id |
| Edge | v17+ | v17+ | v17+ | |
| Firefox | v44+ | v44+ | v46+ | |
| Opera | v39+ | v39+ | ✗ | Android only, requires gcm_sender_id |
| Safari | v16+ | v16+ | v16+ | macOS 13+ |
| Samsung Internet | v4+ | v5+ | ✗ | Requires gcm_sender_id |

---

## Common Error Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `BadJwtToken` | VAPID subject is `https://localhost` | Use `mailto:user@example.org` instead |
| Encryption failure | PushSubscription missing keys.p256dh/keys.auth | Browser `subscribe()` must return complete keys |
| No response to push | Endpoint expired / user unsubscribed | Call `subscribe()` again and update backend |
| Legacy browser subscription failure | Missing gcm_sender_id | Configure in web app manifest |