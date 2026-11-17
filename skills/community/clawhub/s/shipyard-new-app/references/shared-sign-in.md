# One sign-in across apps on subdomains (Supabase)

Use when several apps live on subdomains of one domain (`app1.<domain>`, `app2.<domain>`) and people should sign in once for all of them.

## Requirements

- **One Supabase project** for all the apps (see `shared-project.md`): same users table, same session. Different projects can never share a session.
- **Cookies, not localStorage.** localStorage belongs to one exact origin, so `app1.<domain>` cannot read `app2.<domain>`'s. Use `@supabase/ssr` (`createBrowserClient`, `createServerClient` and the proxy), which stores the session in cookies.
- **The same cookie options in every app and in every client** (browser, server, proxy):

```ts
const isProd = process.env.NODE_ENV === "production";
export const authCookieOptions = {
  name: "sb-<shared-name>-auth",          // identical in every app
  ...(isProd ? { domain: ".<domain>" } : {}), // prod only: localhost and *.vercel.app previews must not get it
  sameSite: "lax" as const,
  secure: isProd,
  path: "/",
};
// createBrowserClient(url, key, { cookieOptions: authCookieOptions }) and the same in createServerClient
```

A name or domain that differs between apps, or between an app's own browser and server clients, makes sign-in look fine and then forget the user on the next page.

## Supabase and Google settings

- Auth > URL configuration: add every app's `https://appN.<domain>/**` to the redirect allow-list (a wildcard `https://*.<domain>/**` also works). The Site URL stays the main app.
- Google OAuth client: add each app's origin to Authorized JavaScript origins; the redirect URI stays the Supabase callback.

## Tell the student first

- **One-time logout**: switching an existing app from its own cookie name to the shared one signs current users out once. Say so before merging.
- **Signed in everywhere**: anyone signed in to one app is signed in to all. An app that needs extra setup (a profile, age check, consent, a paid plan) must check for it on its own, server-side, and send the person through onboarding instead of assuming a signed-in user is ready.

## When to keep a separate auth project

Keep an app on its own project when it holds outside parties' business data (a company's accounting, clients' records, anything under a data-processing agreement), has different legal or residency rules, or its users are a different audience (staff accounts of a business). Merging projects later means migrating every account and its data; give it the same-looking sign-in button instead.
