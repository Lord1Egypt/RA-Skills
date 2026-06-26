---
name: Angular
detect:
  files: ["angular.json", ".angular-cli.json"]
  dependencies: ["@angular/core", "@angular/platform-browser", "@angular/router"]
  keywords: ["Angular"]
---

## attack-surface-frontend

**Angular Security Bypass Vectors:**
1. **`bypassSecurityTrust*` Methods:**
   - Grep for `bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustStyle`, `bypassSecurityTrustUrl`, `bypassSecurityTrustResourceUrl`
   - For each occurrence: is the input user-controlled? These methods explicitly disable Angular's built-in sanitization
   - Is there a custom pipe that wraps `DomSanitizer.bypassSecurityTrust*`? (common pattern that hides the bypass)
2. **`innerHTML` Binding:**
   - Grep for `[innerHTML]` in templates — Angular sanitizes this by default but `bypassSecurityTrustHtml` disables it
   - Is `DomSanitizer.sanitize()` called with `SecurityContext.HTML` before binding? (correct pattern)
3. **Template Injection:**
   - Is `Compiler.compileModuleAndAllComponentsAsync` or `JitCompilerFactory` used at runtime?
   - Are there dynamic templates constructed from user input?
   - Can an attacker inject Angular template syntax (`{{}}`, `[()]`, `*ngIf`) into rendered content?
4. **URL/Resource Injection:**
   - Grep for `[src]`, `[href]` bindings — can a user inject `javascript:` or `data:` URLs?
   - Is `bypassSecurityTrustResourceUrl` used for iframe sources with user-controlled URLs?
5. **Server-Side Rendering (Angular Universal):**
   - If SSR is used: are there hydration mismatches that expose server-only data?
   - Is `TransferState` used? Does the serialized state contain sensitive data?
   - Can an attacker inject content via SSR that bypasses client-side sanitization?

**Angular Router Security:**
6. **Route Guards:**
   - Read all route guard implementations (`CanActivate`, `CanActivateChild`, `CanLoad`, `CanMatch`)
   - Can guards be bypassed by navigating directly to a URL vs clicking through the app?
   - Are lazy-loaded modules protected by `CanLoad`? (without it, the module code is downloaded even if navigation is blocked)
7. **Router State Exposure:**
   - Are query parameters or route data used to render content without sanitization?
   - Can `ActivatedRoute.snapshot.params` values be injected into the DOM?

## config-infrastructure

**Angular Build & Deployment Security:**
1. **`angular.json` Configuration:**
   - Is `optimization` enabled for production builds? (unoptimized builds leak source maps)
   - Are `sourceMap` files generated for production? (exposes original source code)
   - Is `budgets` configured to catch unexpected bundle size increases? (possible supply chain injection)
2. **Environment Files:**
   - Read `src/environments/environment.ts` and `src/environments/environment.prod.ts`
   - Are API keys or secrets in environment files? (they compile into the client bundle)
   - Is `production: true` set in the production environment? (enables Angular production mode)
3. **Content Security Policy:**
   - Angular requires `unsafe-eval` for JIT compilation but NOT for AOT
   - Is the app compiled with AOT? (check `angular.json` for `"aot": true`) — if so, CSP can be stricter
   - Is `unsafe-inline` in the CSP? Angular's `style` bindings may need it, but it weakens XSS protection
4. **Service Worker:**
   - If `@angular/service-worker` is used: read `ngsw-config.json`
   - Is the service worker caching API responses that contain sensitive data?
   - Can the service worker cache be poisoned?

## dependency-audit

**Angular-Specific Dependency Concerns:**
1. Check `@angular/core` version for known security issues (template compiler bypasses, XSS in older versions)
2. Is `@angular/platform-browser-dynamic` in production dependencies? (JIT compiler should be dev-only for AOT apps)
3. Are `zone.js` patches exposing timing information? (zone.js wraps all async operations)
4. Check third-party Angular libraries for `bypassSecurityTrust*` usage — inherited vulnerabilities
