---
name: angular-performance
description: "ALWAYS use when optimizing Angular applications for performance, change detection, bundle size, lazy loading, or runtime performance."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Performance

**Version:** Angular 21 (2025)
**Tags:** Performance, Optimization, Bundle Size, Change Detection

**References:** [Performance Guide](https://angular.dev/guide/performance) • [Change Detection](https://angular.dev/guide/change-detection)

## API Changes

This section documents recent version-specific API changes.

- NEW: Zoneless change detection — Disable zone.js for better performance [source](https://angular.dev/guide/experimental/zoneless)

- NEW: Deferrable views (@defer) — Lazy load component code

- NEW: Signal-based reactivity — Use signals instead of zone.js

- NEW: afterNextRender — Run code after rendering without zone.js

## Best Practices

- Use OnPush change detection strategy

```ts
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  // ...
})
export class MyComponent {}
```

- Use trackBy with @for

```ts
@Component({
  template: `
    @for (item of items; track item.id) {
      {{ item.name }}
    }
  `
})
export class MyComponent {}
```

- Use lazy loading for routes

```ts
const routes: Routes = [
  {
    path: 'dashboard',
    loadComponent: () => import('./dashboard/dashboard.component').then(m => m.DashboardComponent)
  }
];
```

- Use @defer for lazy loading

```ts
@Component({
  template: `
    @defer (on viewport) {
      <heavy-chart-component />
    } @placeholder {
      <div>Loading...</div>
    }
  `
})
export class MyComponent {}
```

- Use trackBy in @for loops

```ts
@for (item of items; track item.id) {
  <li>{{ item.name }}</li>
}
```

- Use pure pipes

```ts
@Pipe({
  name: 'myPipe',
  pure: true // Default - only runs when input changes
})
export class MyPipe implements PipeTransform {}
```

- Avoid function calls in templates

```ts
// ❌ Bad
{{ calculateTotal() }}

// ✅ Good
{{ total }}
```

- Use ngSrc for images

```ts
<img [ngSrc]="imageUrl" width="100" height="100" priority>
```

- Use ChangeDetectionRef manually when needed

```ts
constructor(private cdr: ChangeDetectorRef) {}

updateData() {
  this.data = newData;
  this.cdr.detectChanges();
}
```

- Use runOutsideAngular for third-party libs

```ts
import { runOutsideAngular } from '@angular/core/zone';

onClick() {
  runOutsideAngular(() => {
    this第三方Lib.doSomething();
  });
}
```

- Use provideZonelessChangeDetection

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideZonelessChangeDetection()
  ]
};
```

- Use afterNextRender for initialization

```ts
constructor() {
  afterNextRender(() => {
    // Runs after rendering, outside zone
  });
}
```

- Optimize bundle size

```bash
# Analyze bundle
ng build --stats-json
npx webpack-bundle-analyzer dist/stats.json
```

- Use standalone components

```ts
@Component({
  standalone: true,
  imports: [CommonModule],
  // ...
})
export class MyComponent {}
```
