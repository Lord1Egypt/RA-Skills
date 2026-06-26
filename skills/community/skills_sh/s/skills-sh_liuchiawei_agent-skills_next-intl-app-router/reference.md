# next-intl App Router — Reference

## Example files (in this skill)

Full copy-paste examples live in the [examples/](examples/) folder. Mapping to your project:

| Purpose                     | Example file                                                                                                       | Your project path                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------- |
| Plugin                      | [examples/next.config.ts](examples/next.config.ts)                                                                 | `next.config.ts`                      |
| Routing config              | [examples/i18n/routing.ts](examples/i18n/routing.ts)                                                               | `src/i18n/routing.ts`                 |
| Request / messages          | [examples/i18n/request.ts](examples/i18n/request.ts)                                                               | `src/i18n/request.ts`                 |
| Navigation                  | [examples/i18n/navigation.ts](examples/i18n/navigation.ts)                                                         | `src/i18n/navigation.ts`              |
| Middleware / proxy          | [examples/proxy.ts](examples/proxy.ts)                                                                             | `src/proxy.ts` or `src/middleware.ts` |
| Locale layout + provider    | [examples/app-locale-layout.tsx](examples/app-locale-layout.tsx)                                                   | `src/app/[locale]/layout.tsx`         |
| Index page                  | [examples/app-locale-page.tsx](examples/app-locale-page.tsx)                                                       | `src/app/[locale]/page.tsx`           |
| About page                  | [examples/app-locale-about-page.tsx](examples/app-locale-about-page.tsx)                                           | `src/app/[locale]/about/page.tsx`     |
| Client component (Link + t) | [examples/BackToHomeButton.tsx](examples/BackToHomeButton.tsx), [examples/Nav-client.tsx](examples/Nav-client.tsx) | Any client component                  |
| Messages                    | [examples/messages-en.json](examples/messages-en.json)                                                             | `messages/en.json` (+ one per locale) |

See [examples/README.md](examples/README.md) for copy-to-path mapping.

## defineRouting options

```ts
defineRouting({
  locales: ["en", "ja", "zh-CN", "zh-TW"],
  defaultLocale: "en",
  localePrefix: "as-needed", // or "always" | "never"
  pathnames: { "/about": "/about", "/users": "/users" }, // optional
});
```

- **localePrefix**: `"always"` (e.g. `/en/about`), `"as-needed"` (default locale can omit prefix), `"never"` (no prefix in URL).

## getRequestConfig return shape

```ts
return {
  locale: "en",
  messages: { ... },
  timeZone: "Asia/Tokyo",        // optional
  now: new Date(),              // optional
  defaultTranslationValues: {}, // optional
};
```

## Server vs client APIs

| Context | Hook / API                                     | Import from         |
| ------- | ---------------------------------------------- | ------------------- |
| Client  | `useTranslations(namespace)`                   | `next-intl`         |
| Client  | `Link`, `useRouter`, `usePathname`, `redirect` | `@/i18n/navigation` |
| Server  | `getTranslations({ locale, namespace })`       | `next-intl/server`  |
| Server  | `getMessages()`, `setRequestLocale(locale)`    | `next-intl/server`  |
| Server  | `hasLocale(routing.locales, locale)`           | `next-intl`         |

## Links

- [Getting started (App Router)](https://next-intl.dev/docs/getting-started/app-router)
- [Routing setup](https://next-intl.dev/docs/routing/setup)
- [Routing configuration](https://next-intl.dev/docs/routing/configuration)
- [Translations](https://next-intl.dev/docs/usage/translations)
