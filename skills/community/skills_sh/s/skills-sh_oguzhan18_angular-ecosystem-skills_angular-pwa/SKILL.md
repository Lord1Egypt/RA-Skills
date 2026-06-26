---
name: angular-pwa
description: "ALWAYS use when working with Angular PWA, service workers, offline support, manifest, or web app installation in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# @angular/pwa

**Version:** Angular 21 (2025)
**Tags:** PWA, Service Worker, Offline, Web App Manifest

**References:** [PWA Guide](https://angular.dev/guide/pwa) • [ngsw-config](https://angular.io/guide/service-worker-config)

## API Changes

This section documents recent version-specific API changes.

- NEW: Angular Service Worker v2 — Improved caching strategies

- NEW: esbuild PWA support — Faster builds

- NEW: @angular/build:application — Modern PWA building

## Best Practices

- Add PWA to project

```bash
ng add @angular/pwa
```

- Configure ngsw-config.json

```json
{
  "$schema": "./node_modules/@angular/service-worker/config/schema.json",
  "index": "/index.html",
  "assetGroups": [
    {
      "name": "app",
      "installMode": "prefetch",
      "resources": {
        "files": [
          "/favicon.ico",
          "/index.html",
          "/*.css",
          "/*.js"
        ]
      }
    },
    {
      "name": "assets",
      "installMode": "lazy",
      "updateMode": "prefetch",
      "resources": {
        "files": [
          "/assets/**",
          "/*.(svg|cur|jpg|jpeg|png)"
        ]
      }
    }
  ],
  "dataGroups": [
    {
      "name": "api-freshness",
      "urls": ["/api/**"],
      "cacheConfig": {
        "strategy": "freshness",
        "maxSize": 100,
        "maxAge": "1h",
        "timeout": "10s"
      }
    }
  ]
}
```

- Use network-first for API calls

```json
{
  "dataGroups": [
    {
      "name": "api",
      "urls": ["/api/**"],
      "cacheConfig": {
        "strategy": "freshness",
        "maxSize": 50,
        "maxAge": "1h"
      }
    }
  ]
}
```

- Use cache-first for static assets

```json
{
  "assetGroups": [
    {
      "name": "static",
      "installMode": "prefetch",
      "updateMode": "prefetch",
      "resources": {
        "files": ["/*.js", "/*.css"]
      }
    }
  ]
}
```

- Handle offline state

```ts
import { SwPush } from '@angular/service-worker';

constructor(private swPush: SwPush) {}

subscribeToNotifications() {
  if (this.swPush.isEnabled) {
    this.swPush.requestSubscription({
      serverPublicKey: 'VAPID_PUBLIC_KEY'
    });
  }
}
```

- Check service worker updates

```ts
import { SwUpdate } from '@angular/service-worker';

constructor(private updates: SwUpdate) {
  this.updates.versionUpdates.subscribe(event => {
    if (event.type === 'VERSION_READY') {
      // Reload to get new version
      window.location.reload();
    }
  });
}
```

- Customize manifest

```json
{
  "name": "My PWA",
  "short_name": "MyPWA",
  "theme_color": "#1976d2",
  "background_color": "#ffffff",
  "display": "standalone",
  "scope": "/",
  "start_url": "/",
  "icons": [
    {
      "src": "assets/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```
