---
name: angular-security
description: "ALWAYS use when working with Angular Security, XSS prevention, CSRF protection, Content Security Policy, or sanitization in Angular applications."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Security

**Version:** Angular 21 (2025)
**Tags:** Security, XSS, CSRF, CSP, Sanitization

**References:** [Security Guide](https://angular.dev/guide/security) • [DomSanitizer](https://angular.io/api/platform-browser/DomSanitizer)

## API Changes

This section documents recent version-specific API changes.

- NEW: Trusted Types — Angular supports Trusted Types for CSP

- NEW: HttpClient CSRF — Built-in CSRF protection with CookieXSRFStrategy

- NEW: provideZoneChangeDetection with untrustedEvents — Zone.js event filtering

- NEW: afterNextRender security — Run code safely after rendering

## Best Practices

- Use DomSanitizer for safe HTML

```ts
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

constructor(private sanitizer: DomSanitizer) {}

getSafeHtml(html: string): SafeHtml {
  return this.sanitizer.bypassSecurityTrustHtml(html);
}
```

- Use bypassSecurityTrust methods carefully

```ts
// Only use when content is trusted
this.safeUrl = this.sanitizer.bypassSecurityTrustUrl(userInput);
this.safeScript = this.sanitizer.bypassSecurityTrustScript(script);
this.safeStyle = this.sanitizer.bypassSecurityTrustStyle(style);
this.safeResourceUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
```

- Use HttpClient with CSRF protection

```ts
// Automatically uses XSRF-TOKEN cookie
http.get('/api/data').subscribe();

// Configure CSRF
provideHttpClient(
  withXsrfConfiguration({
    cookieName: 'XSRF-TOKEN',
    headerName: 'X-XSRF-TOKEN'
  })
)
```

- Use innerHTML with sanitization

```ts
@Component({
  template: `<div [innerHTML]="safeContent"></div>`
})
export class MyComponent {
  // Angular sanitizes automatically
  safeContent = '<p>Safe content</p>';
}
```

- Avoid dynamic template evaluation

```ts
// ❌ Dangerous
eval(userInput);

// ✅ Safe - use Angular's binding
{{ userInput }}
```

- Use Content Security Policy

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self'">
```

- Use Trusted Types

```ts
import { provideTrustedTypes } from '@angular/core';

export const appConfig: ApplicationConfig = {
  providers: [
    provideTrustedTypes()
  ]
};
```

- Validate user input

```ts
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'escapeHtml' })
export class EscapeHtmlPipe implements PipeTransform {
  transform(value: string): string {
    return value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
}
```

- Use HttpClient interceptors for auth

```ts
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).getToken();
  
  if (token) {
    const authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
    return next(authReq);
  }
  return next(req);
};
```

- Use router guards for route protection

```ts
export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  
  if (auth.isAuthenticated()) {
    return true;
  }
  return router.createUrlTree(['/login']);
};
```
