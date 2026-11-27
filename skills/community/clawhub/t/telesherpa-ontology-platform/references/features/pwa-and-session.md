# PWA & persistent login on the web platform

The platform runs not only in the app and the browser, but also as an **installable PWA**
(web app on the home screen). For agents this becomes relevant when a human reports
"having to log in again constantly" or when push notifications are involved.

## What applies to whom

| Channel | Login | Push |
|---|---|---|
| **App (iOS/Android)** | native app login | APNs/FCM (app tokens) |
| **Browser (web)** | session cookie, **30 minutes** | — |
| **PWA (home screen)** | session cookie 30 min **+ persistent login up to 14 days** | Web Push (VAPID) |
| **MCP / REST** | bearer token 10 h + refresh token 30 days | — |

## The 30-minute session and why it is deliberately short

The web session lasts **30 minutes** and is extended on every request. After that the
permission check takes effect and redirects to the login page.
That is intentional — on a shared machine an open session should not remain valid for days.

## PWA: stay logged in for up to 14 days

In the **installed** PWA (home screen) there is no address bar and no
bookmarks — a forced login is expensive there. That is why the following additionally applies there:

```
Session expired
  → silent auto-login (14 days)
      → if it applies: the requested page appears directly (no login screen)
      → if not: visible login screen, no intermediate step
```

Building blocks:

- The PWA reports itself **client-side** as installed (`display-mode: standalone` or
  `navigator.standalone`) and sends a `pwa` marker along at login.
- Server-side this becomes a **persistent session** (14 days) plus a PWA flag.
- The silent re-login runs **without token rotation** — otherwise the token would be deleted
  on the second request (the browser does not adopt `Set-Cookie` from a `fetch()` response).
- **Logout deletes both** (persistent session + PWA flag) — otherwise the next login
  in the same browser would again count as "from the PWA".

**Important for agents:** There is NO server-side PWA detection via the user agent. iOS
delivers the same UA from the PWA as from Safari. Anyone checking a login "from outside"
therefore cannot tell from the UA whether a request comes from the PWA — the client has to
send the marker along.

## Push notifications: only from the home screen (iOS)

Web Push works via VAPID and the browser's subscriptions — **on iOS, however, only if the
page was launched from the home screen.** In a Safari tab the toggle only shows a
hint. To receive messages the web app does **not** have to be running (service worker).

The subscriptions are stored as JSON on the user; sending runs through the notification logic.
Dead subscriptions (404/410 from the push service) are removed — otherwise they grow endlessly.

## What an agent takes from this

1. **A "not logged in" on the web is not a permissions problem.** First check whether it is only the
   expired 30-minute session (the user is redirected to the login page).
2. **The agent itself uses MCP/REST** — there the bearer token applies (10 h) and afterwards the
   refresh token (30 days). PWA mechanics do not affect it.
3. **"The login screen keeps appearing"** in a PWA: check whether the page is really running
   installed (not in a tab) and whether the user logged out recently — logout deliberately clears the
   persistent login as well.
4. **"No push notifications on the iPhone"**: the web app must be on the home screen.
   In a tab there is no push, regardless of permissions.
