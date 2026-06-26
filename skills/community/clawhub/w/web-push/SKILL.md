---
name: web-push
description: Send Web Push notifications from a Node.js backend using the web-push npm library (VAPID authentication, payload encryption). Covers generating VAPID keys, subscribing browsers, sending notifications, CLI usage, browser compatibility, and common pitfalls. 
---

# Web Push Notifications

Send push notifications to browsers (Chrome, Firefox, Edge, Safari) using the web-push npm library, which implements the Web Push Protocol with VAPID authentication and payload encryption per Message Encryption for Web Push.

## Use Cases

Use when working with Push API subscriptions, browser push notifications, VAPID key management, Web Push Protocol implementation, or web-push npm package integration.

## Quick Start

```javascript
const webpush = require('web-push');

// 1. Generate VAPID keys ONCE, store permanently
const vapidKeys = webpush.generateVAPIDKeys();

// 2. Set credentials
webpush.setGCMAPIKey('<Your GCM API Key Here>');
webpush.setVapidDetails(
  'mailto:example@yourdomain.org',
  vapidKeys.publicKey,
  vapidKeys.privateKey
);

// 3. Subscribe in the browser (client-side)
// registration.pushManager.subscribe({
//   userVisibleOnly: true,
//   applicationServerKey: vapidPublicKey
// });

// 4. Send from server
const pushSubscription = {
  endpoint: 'https://fcm.googleapis.com/fcm/send/...',
  keys: { p256dh: '...', auth: '...' }
};

await webpush.sendNotification(pushSubscription, 'Hello World');
```

## Core Workflows

### Generate VAPID Keys

Generate once, store permanently. The public key is used as `applicationServerKey` in the browser. Never regenerate for the same application — you'll break existing subscriptions.

```javascript
const vapidKeys = webpush.generateVAPIDKeys();
// { publicKey: '...', privateKey: '...' }
```

### Set Credentials

```javascript
webpush.setVapidDetails(
  'mailto:user@example.org',  // mailto: or https: URI
  process.env.VAPID_PUBLIC_KEY,
  process.env.VAPID_PRIVATE_KEY
);
```

### Subscribe in the Browser

```javascript
// Client-side Service Worker
registration.pushManager.subscribe({
  userVisibleOnly: true,
  applicationServerKey: urlBase64ToUint8Array(publicKey)
});
// Returns PushSubscription → send to server and store
```

### Send a Notification

```javascript
await webpush.sendNotification(pushSubscription, 'Hello World', {
  // vapidDetails overrides global setVapidDetails
  TTL: 60,             // seconds push service retains (default: 4 weeks)
  urgency: 'high',     // very-low | low | normal | high
  topic: 'updates',    // coalesce notifications, max 32 URL-safe base64 chars
  contentEncoding: 'aes128gcm',  // default; 'aesgcm' for legacy
  timeout: 5000,       // socket timeout in ms
});
```

### Encrypt Without Sending

```javascript
const encrypted = await webpush.encrypt(
  subscription.keys.p256dh,
  subscription.keys.auth,
  'My Payload',
  'aes128gcm'
);
// { localPublicKey, salt, cipherText }
```

### Generate Request Details Without Sending

```javascript
const details = webpush.generateRequestDetails(
  pushSubscription,
  payload,
  { vapidDetails: {...}, contentEncoding: 'aes128gcm' }
);
// { endpoint, method: 'POST', headers, body: Buffer }
```

## CLI Usage

```shell
# Install
npm install web-push -g

# Generate VAPID keys
web-push generate-vapid-keys --json

# Send notification
web-push send-notification \
  --endpoint=https://fcm.googleapis.com/fcm/send/... \
  --key=<p256dh> --auth=<auth_secret> \
  --vapid-subject=mailto:example@qq.com \
  --vapid-pubkey=<pub> --vapid-pvtkey=<priv> \
  --payload="Hello" [--ttl=<seconds>] [--encoding=aesgcm|aes128gcm]
```

## Critical Pitfalls

- **VAPID keys**: Generate ONCE. Store them. Never regenerate for the same app — breaks existing subscriptions.
- **Safari + localhost**: Safari rejects VAPID with `BadJwtToken` if subject is `https://localhost`. Use `mailto:` instead.
- **Payload encryption**: The PushSubscription MUST include `keys.p256dh` and `keys.auth`. Without them, only empty payloads work.
- **Encoding**: `aes128gcm` (default) for modern browsers; `aesgcm` only for legacy Chrome < 50 and Opera.

## Browser Compatibility

| Browser | Push w/o Payload | Push w/ Payload | VAPID |
|---------|-----------------|-----------------|-------|
| Chrome  | v42+            | v50+            | v52+  |
| Edge    | v17+            | v17+            | v17+  |
| Firefox | v44+            | v44+            | v46+  |
| Safari  | v16+ (macOS 13) | v16+            | v16+  |
| Opera   | v39+ (Android)  | v39+ (Android)  | ✗     |
| Samsung | v4+             | v5+             | ✗     |

## Full API Reference

See [references/webpush.md](references/webpush.md) for all functions (`sendNotification`, `generateVAPIDKeys`, `setGCMAPIKey`, `setVapidDetails`, `encrypt`, `getVapidHeaders`, `generateRequestDetails`) with detailed parameter tables and return types.