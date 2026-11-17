# Web Push на стороне браузера

Клиентская часть целиком: Service Worker, подписка, показ уведомления,
обработка клика и поведение на разных платформах.

## Файлы

```
/service-worker.js     — приём push и показ уведомления
/app.js                 — запрос подписки и отправка её на сервер
/api/push/key           — публичный VAPID-ключ (JSON)
/api/push/subscribe     — приём подписки (POST)
/api/push/unsubscribe   — отписка (POST)
```

## Service Worker

```javascript
const CACHE = 'zel-v1';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((c) =>
      c.addAll(['/icons/icon-192.png', '/icons/badge-96.png'])
    )
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('push', (event) => {
  let data = {};
  try {
    data = event.data ? event.data.json() : {};
  } catch (e) {
    data = { title: 'Уведомление', body: event.data ? event.data.text() : '' };
  }

  const title = data.title || 'Зелёный град';
  const options = {
    body: data.body || '',
    icon: data.icon || '/icons/icon-192.png',
    badge: '/icons/badge-96.png',
    tag: data.tag || 'default',
    renotify: Boolean(data.tag),
    requireInteraction: Boolean(data.requireInteraction),
    data: { url: data.url || '/' },
    vibrate: data.vibrate || [80, 40, 80],
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const url = event.notification.data?.url || '/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((list) => {
      for (const client of list) {
        if ('focus' in client) {
          client.navigate(url);
          return client.focus();
        }
      }
      return self.clients.openWindow(url);
    })
  );
});
```

**Кэшировать иконки в SW важно:** без этого push-уведомление на медленной
сети покажет иконку-заглушку, а при офлайне — вообще ничего.

## Подписка на странице

```javascript
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map((c) => c.charCodeAt(0)));
}

async function getVapidKey() {
  const res = await fetch('/api/push/key');
  const { publicKey } = await res.json();
  return publicKey;
}

async function enablePush() {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    throw new Error('Браузер не поддерживает push');
  }

  const reg = await navigator.serviceWorker.register('/service-worker.js');
  await navigator.serviceWorker.ready;

  const permission = await Notification.requestPermission();
  if (permission !== 'granted') {
    throw new Error('Разрешение не выдано');
  }

  const vapidKey = await getVapidKey();
  let sub = await reg.pushManager.getSubscription();

  if (!sub) {
    sub = await reg.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(vapidKey),
    });
  }

  const res = await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sub.toJSON()),
  });

  if (!res.ok) {
    throw new Error(`Сервер отклонил подписку: ${res.status}`);
  }
  return sub;
}

async function disablePush() {
  const reg = await navigator.serviceWorker.getRegistration();
  const sub = await reg?.pushManager.getSubscription();
  if (!sub) return;
  await fetch('/api/push/unsubscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(sub.toJSON()),
  });
  await sub.unsubscribe();
}
```

## Проверка перед сдачей

```javascript
// в консоли браузера
await Notification.requestPermission();          // должно быть 'granted'
await navigator.serviceWorker.getRegistration();  // должен быть объект
const reg = await navigator.serviceWorker.ready;
await reg.pushManager.getSubscription();          // должен быть объект
```

## Особенности платформ

### iOS / iPadOS

- WebPush работает **только** для PWA, добавленной на главный экран
  («Добавить на экран Домой» в Safari).
- Требуется iOS 16.4 или новее.
- Внутри обычного Safari push **не работает** — только в standalone-режиме.
- `Notification.requestPermission()` вызывать нужно по действию пользователя
  (тап по кнопке), иначе Safari отклонит запрос.

Проверка standalone-режима:

```javascript
if (window.navigator.standalone === true || window.matchMedia('(display-mode: standalone)').matches) {
  // можно предлагать подписку
}
```

### Android / Chrome

- Push работает во вкладке, но с 2024 Chrome требует, чтобы PWA была
  **установлена** на устройство для показа уведомлений поверх всего.
- Если PWA не установлена, push всё равно доставляется, но показ может
  быть отложен.

### Политика уведомлений

- Chrome на Android: для push с payload нужен `userVisibleOnly: true`.
- Если приложение не в фокусе, `showNotification` всё равно показывает
  уведомление.
- `tag` в options группирует уведомления: с одним тегом старое
  уведомление заменяется новым. Для цен — удобно, чтобы не сыпать
  дубли.

### Тихие уведомления

Для несрочных обновлений (дайджест) `requireInteraction: false` — уведомление
не будет вибрировать и требовать нажатия. Для аварийных («прорыв трубы»)
нужен `requireInteraction: true` и `urgency: 'high'` на сервере.

## Отладка

```javascript
// Проверить, что SW активен
navigator.serviceWorker.controller          // null, если ещё не загрузился
// Перезагрузить SW после правки
navigator.serviceWorker.getRegistration().then((r) => r.update());
// Проверить подписку
navigator.serviceWorker.ready.then((r) => r.pushManager.getSubscription());
```

Chrome DevTools → Application → Service Workers: отметка «Update on reload»
перезагружает SW после каждой правки. Вкладка Application → Manifest
показывает, установлена ли PWA.
