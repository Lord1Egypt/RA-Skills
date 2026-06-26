# Example files

Copy these into your project as needed. Path mapping:

| This file                   | Copy to (in your project)                                         |
| --------------------------- | ----------------------------------------------------------------- |
| `next.config.ts`            | `next.config.ts` (merge with existing)                            |
| `i18n/routing.ts`           | `src/i18n/routing.ts`                                             |
| `i18n/request.ts`           | `src/i18n/request.ts`                                             |
| `i18n/navigation.ts`        | `src/i18n/navigation.ts`                                          |
| `proxy.ts`                  | `src/proxy.ts` (Next 16) or `src/middleware.ts`                   |
| `app-locale-layout.tsx`     | `src/app/[locale]/layout.tsx`                                     |
| `app-locale-page.tsx`       | `src/app/[locale]/page.tsx`                                       |
| `app-locale-about-page.tsx` | `src/app/[locale]/about/page.tsx`                                 |
| `BackToHomeButton.tsx`      | Any client component (e.g. `src/components/BackToHomeButton.tsx`) |
| `Nav-client.tsx`            | Any client nav component                                          |
| `messages-en.json`          | `messages/en.json` (add `ja.json`, etc. per locale)               |

Adjust `@/i18n/routing` and `@/i18n/navigation` if your alias differs.
