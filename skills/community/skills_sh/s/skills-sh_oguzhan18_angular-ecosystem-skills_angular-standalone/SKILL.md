---
name: angular-standalone
description: "ALWAYS use when working with Angular Standalone Components, imports array, bootstrapping, or migrating from NgModules in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Standalone Components

**Version:** Angular 21 (2025)
**Tags:** Standalone, Components, Imports, Bootstrap

**References:** [Standalone Guide](https://angular.dev/guide/components/standalone) • [Migration](https://angular.dev/guide/components/importing)

## API Changes

This section documents recent version-specific API changes.

- NEW: Standalone by default — New components are standalone by default since Angular 17

- NEW: provideRouter for standalone — Use functional providers instead of RouterModule

- NEW: ng generate @angular/core:standalone — Migration schematic

- DEPRECATED: NgModule — Migration to standalone components recommended

## Best Practices

- Create standalone components

```ts
@Component({
  standalone: true,
  imports: [CommonModule, MatButtonModule],
  selector: 'app-my',
  template: `<button>Click</button>`
})
export class MyComponent {}
```

- Use imports array for dependencies

```ts
@Component({
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MyChildComponent
  ],
  template: `
    <mat-card>
      <app-my-child></app-my-child>
    </mat-card>
  `
})
export class ParentComponent {}
```

- Bootstrap standalone component

```ts
// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch(err => console.error(err));
```

- Use functional providers

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    provideAnimations()
  ]
};
```

- Use provideZoneChangeDetection

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true })
  ]
};
```

- Migrate from NgModule

```bash
# Full migration
ng generate @angular/core:standalone

# Specific component
ng generate @angular/core:standalone --path=path/to/component
```

- Use Router Outlet with standalone

```ts
@Component({
  standalone: true,
  imports: [RouterOutlet],
  template: `<router-outlet></router-outlet>`
})
export class AppComponent {}
```

- Lazy load standalone components

```ts
const routes: Routes = [
  {
    path: 'admin',
    loadComponent: () => import('./admin/admin.component').then(m => m.AdminComponent)
  }
];
```

- Use forwardRef for circular imports

```ts
@Component({
  standalone: true,
  imports: [forwardRef(() => OtherComponent)]
})
export class MyComponent {}
```

- Export standalone components

```ts
@Component({
  standalone: true,
  exports: [MyComponent],
  imports: [MyComponent]
})
export class FeatureComponent {}
```
