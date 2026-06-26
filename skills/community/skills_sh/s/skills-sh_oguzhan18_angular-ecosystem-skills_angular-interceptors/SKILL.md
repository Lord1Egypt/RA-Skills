---
name: angular-interceptors
description: "ALWAYS use when working with Angular HTTP Interceptors, request/response transformation, auth interceptors, or error handling in HTTP calls."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular HTTP Interceptors

**Version:** Angular 21 (2025)
**Tags:** HTTP, Interceptors, Auth, Middleware

**References:** [Interceptors Guide](https://angular.dev/guide/http/interceptors) • [API](https://angular.io/api/common/http/HttpInterceptor)

## API Changes

This section documents recent version-specific API changes.

- NEW: Functional interceptors — Use `HttpInterceptorFn` instead of class-based

- NEW: provideHttpClient with withInterceptors — Modern interceptor setup

- NEW: HttpContext — Per-request metadata with HttpContextToken

- DEPRECATED: Class-based HttpInterceptor — Migrate to functional

## Best Practices

- Create functional interceptor

```ts
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();
  
  if (token) {
    const authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
    return next(authReq);
  }
  return next(req);
};
```

- Register interceptors

```ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([authInterceptor, logInterceptor])
    )
  ]
};
```

- Handle errors in interceptor

```ts
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        inject(Router).navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
};
```

- Use multiple interceptors (order matters)

```ts
provideHttpClient(
  withInterceptors([loggingInterceptor, authInterceptor, errorInterceptor])
)
```

- Use HttpContext for per-request flags

```ts
const CACHE_KEY = new HttpContextToken<boolean>(() => false);

export const cacheInterceptor: HttpInterceptorFn = (req, next) => {
  if (req.context.get(CACHE_KEY)) {
    // Check cache
  }
  return next(req);
};

// Usage
http.get('/api/data', { context: new HttpContext().set(CACHE_KEY, true) });
```

- Transform request

```ts
export const transformInterceptor: HttpInterceptorFn = (req, next) => {
  if (req.url.includes('/api/')) {
    const transformed = req.clone({
      setHeaders: { 'X-Custom-Header': 'value' }
    });
    return next(transformed);
  }
  return next(req);
};
```

- Transform response

```ts
export const responseInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    map(event => {
      if (event instanceof HttpResponse) {
        return event.clone({ body: transformData(event.body) });
      }
      return event;
    })
  );
};
```
