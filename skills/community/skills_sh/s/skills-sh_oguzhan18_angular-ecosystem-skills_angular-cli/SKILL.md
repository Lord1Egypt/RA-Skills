---
name: angular-cli
description: "ALWAYS use when working with Angular CLI, generating components, services, building applications, or workspace configuration in Angular projects."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# @angular/cli

**Version:** Angular 21 (2025)
**Tags:** CLI, Generators, Build, Scaffolding

**References:** [CLI Reference](https://angular.dev/cli) • [Generators](https://angular.dev/cli/generate) • [Builders](https://angular.dev/cli/build)

## API Changes

This section documents recent version-specific API changes.

- NEW: Control flow migration — `ng g @angular/core:control-flow` for @if/@for migration [source](https://angular.love/angular-generators)

- NEW: Signal input migration — `ng g @angular/core:signal-input-migration` for signal inputs [source](https://angular.love/angular-generators)

- NEW: Route lazy loading migration — `ng g @angular/core:route-lazy-loading` for standalone routes

- NEW: Named workspaces — Multiple applications in single angular.json

- NEW: esbuild by default — Faster builds with esbuild/Vite

## Best Practices

- Use generators for scaffolding

```bash
# Generate component
ng g c components/my-component

# Generate service
ng g s services/my-service

# Generate guard
ng g g guards/auth

# Generate interceptor
ng g interceptor timing

# Generate library
ng g library my-lib

# Generate with standalone
ng g c my-component --standalone
```

- Use schematics for migrations

```bash
# Migrate to control flow
ng g @angular/core:control-flow

# Migrate to signal inputs
ng g @angular/core:signal-input-migration

# Migrate to lazy loading routes
ng g @angular/core:route-lazy-loading
```

- Use ng add for packages

```bash
# Add Angular Material
ng add @angular/material

# Add SSR
ng add @angular/ssr

# Add PWA
ng add @angular/pwa
```

- Configure workspace defaults

```json
{
  "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
  "version": 1,
  "newProjectRoot": "projects",
  "projects": {
    "my-app": {
      "schematics": {
        "@schematics/angular:component": {
          "style": "scss",
          "standalone": true
        }
      }
    }
  }
}
```

- Use ng run for builders

```bash
# Run custom builder
ng run my-app:build

# Run SSR
ng run my-app:serve-ssr

# Run prerender
ng run my-app:prerender
```

- Use ng config for settings

```bash
# Set default style
ng config defaults.style=scss

# Enable analytics
ng analytics enable
```

- Use ng update for migrations

```bash
# Update packages
ng update

# Update specific package
ng update @angular/core
```

- Use ng build with options

```bash
# Production build
ng build --configuration=production

# Dev build with stats
ng build --stats-json
```

- Use standalone by default

```bash
# New project with standalone
ng new my-app --standalone
```

- Use functional over class-based

```bash
# Generate functional guard
ng g g guards/auth --functional

# Generate functional interceptor
ng g interceptor my-interceptor --functional
```
