# Auth, Sessions, and Security

**Contents**: [The Session Cookie Baseline](#the-session-cookie-baseline) · [Where the Guard Goes](#where-the-guard-goes) · [Session Storage Choices](#session-storage-choices) · [Passwords and Login Endpoints](#passwords-and-login-endpoints) · [OAuth and Third-Party Providers](#oauth-and-third-party-providers) · [Authorization Beyond "Logged In"](#authorization-beyond-logged-in) · [What Reaches the Browser](#what-reaches-the-browser) · [Injection, Redirects, Traversal](#injection-redirects-traversal) · [Headers, Framing, and CSP](#headers-framing-and-csp) · [Security Checklist](#security-checklist)

Authentication answers "who is this request", once per request, in `hooks.server.js`. Authorization answers "may they do this", separately in every load, action, and endpoint that touches data. Conflating the two is the origin of most SvelteKit auth bugs: a `handle` hook that also decides access looks like a guard and is not one.

## The Session Cookie Baseline

```js
// hooks.server.js — authentication only
export const handle = async ({ event, resolve }) => {
  const sid = event.cookies.get('sid');
  event.locals.user = sid ? await db.userBySession(sid) : null;   // null, never a throw
  return resolve(event);
};

// +page.server.js — the login action
export const actions = {
  login: async ({ request, cookies }) => {
    const form = await request.formData();
    const user = await verifyCredentials(form.get('email'), form.get('password'));
    if (!user) return fail(400, { email: form.get('email'), error: 'Invalid credentials' });

    const session = await db.createSession(user.id);              // new id on every login
    cookies.set('sid', session.id, {
      path: '/', httpOnly: true, sameSite: 'lax', secure: true,
      maxAge: 60 * 60 * 24 * 7
    });
    redirect(303, '/app');
  }
};
```

| Cookie flag | Why it is not optional |
|---|---|
| `path: '/'` | Required by `cookies.set`/`delete` (`@sveltejs/kit >=2`); a mismatched path on delete leaves the session alive |
| `httpOnly: true` | JavaScript cannot read it, so an XSS bug cannot exfiltrate the session. Never mirror the token into `localStorage` |
| `secure: true` | Kit sets it automatically except on localhost; behind a TLS-terminating proxy it depends on `ORIGIN` being right |
| `sameSite: 'lax'` | Blocks the cross-site POST that CSRF needs. `'none'` (plus `secure`) only for a cookie an external site must send — an OAuth `form_post` callback |
| `maxAge` | Absolute lifetime. Rotate the session id on privilege change (login, password change, role grant), or session fixation survives the login |

Logout deletes both sides: `cookies.delete('sid', { path: '/' })` **and** the server row. Deleting only the cookie leaves a valid session id in whatever copied it.

## Where the Guard Goes

| Placement | Protects | Does not protect |
|---|---|---|
| `handle` hook, by path prefix | Every request to that prefix, including `+server.js` and actions | Nothing under a different prefix — one route moved out of `/app` is public |
| `+layout.server.js` load | The first server render of pages under it | Actions, endpoints, and client-side navigations where the layout load did not rerun (SKILL.md rule 7) |
| `+page.server.js` load / each action / each endpoint | Exactly that operation | Nothing else, which is why it is the only placement that cannot be bypassed by accident |

- Deny by default: `const user = requireUser(locals)` at the top of every server load, action, and handler, where `requireUser` calls `redirect(303, '/login?next=…')` or `error(403)`. One helper, imported everywhere, greps as a checklist.
- A guard in a universal `+page.js` guards nothing: that code also runs in the browser and the user owns the browser.
- `+layout.server.js` is still the right place to *provide* `user` to the page tree; treat its output as data, not as a gate.
- Test it the way it breaks: request the protected endpoint directly with `curl` and no cookie, and click through with a second, unauthorized account.

## Session Storage Choices

| Approach | Revocation | Cost | Pick when |
|---|---|---|---|
| Session id + server table | Immediate: delete the row | One lookup per request (cache it in the hook, not in a module variable — SKILL.md rule 4) | Default. Anything with logout-everywhere, bans, or role changes |
| Signed/encrypted cookie holding claims | None until expiry, unless you keep a denylist | Zero lookups | Short-lived tokens, or a stateless edge deployment where a DB hop per request is the latency budget |
| Third-party provider session (`@auth/sveltekit`, a hosted IdP) | Provider's semantics | An SDK and its release cadence | You need many OAuth providers, SAML, or enterprise SSO |

Whatever holds the session, the session id is a credential: generate it from a CSPRNG, store a hash of it if the table is ever readable by support tooling, and never put it in a URL — URLs land in logs, `Referer` headers, and pasted bug reports.

## Passwords and Login Endpoints

- Hash with argon2id or bcrypt on the server, never a bare SHA. Both are native modules: on an edge runtime (`adapter-cloudflare`, Vercel edge) they will not load, so either keep the login route on a Node runtime via `export const config`, or use a Web Crypto PBKDF2 implementation deliberately chosen for that constraint.
- Compare with the library's own verify function — it is constant-time. A `===` on hashes leaks timing.
- Return the same failure for unknown email and wrong password, and take the same time for both, or the form becomes a user-enumeration oracle.
- Rate-limit by (IP, identifier) pair in the action itself; a hook-level limiter that counts page views does not see the POST it needs to count.
- `fail()` echoes back what you pass it, and it renders into the HTML: repopulate the email, never the password (SKILL.md Traps and the forms guidance in Quick Reference).
- Do not log `FormData` wholesale in `handleError` or a middleware — that is how credentials reach a log aggregator.

## OAuth and Third-Party Providers

- The callback is a `+server.js` `GET`, not a page: it exchanges the code, creates the session, and returns a `redirect(303, …)`.
- Store the `state` value in a short-lived `httpOnly` cookie before the redirect out, and compare on return; PKCE (`code_verifier`) goes in the same cookie. A callback that skips this accepts any provider response.
- Client secrets come from `$env/static/private` or `$env/dynamic/private`. A `PUBLIC_`-prefixed secret is in the bundle for everyone.
- The provider's email is not proof of ownership unless the provider says it is verified; matching an existing local account on an unverified email is an account-takeover path.

## Authorization Beyond "Logged In"

- Object-level checks belong in the query, not after it: `db.getInvoice(id, user.orgId)` rather than fetching by id and comparing in JavaScript. The version that fetches first leaks through any code path that forgets the comparison.
- Route params are user input: a param matcher validates shape, never ownership. `[id=integer]` proves the id is a number, not that it is yours.
- Roles live in `locals` from the session, never in a form field, a query string, or a cookie the client can rewrite.
- Multi-tenant apps: put the tenant id in `locals` in the hook and require it in every query signature, so a missing tenant scope is a type error rather than a full-table read.

## What Reaches the Browser

Everything a server load returns is serialized into the HTML document — visible in view-source, in the client payload, and in any cache in between.

- Return the fields the page renders. `return { user }` on a row that carries `passwordHash`, `stripeCustomerId`, or an internal note ships all of it.
- `PUBLIC_`-prefixed env values are in the JavaScript bundle by definition; there is no semi-public key.
- `$lib/server/**` and `*.server.js` cannot be imported from client-reachable code — the build fails and names the import chain. A shared `utils.js` that imports one server-only helper poisons every importer, so split the module rather than weakening the boundary.
- Error objects are sanitized to a generic 500 before they reach the client; put the detail in `handleError`'s log, and keep the `App.Error` shape free of internals.

## Injection, Redirects, Traversal

| Surface | The bug | The fix |
|---|---|---|
| `{@html value}` | Stored XSS from user content, and scoped styles do not apply to it | Sanitize on the server with an allowlist sanitizer, store the sanitized copy, style with `:global` |
| `?next=` after login | Open redirect to a phishing clone | Accept only a path starting with `/` and not `//` or `/\`; reject absolute URLs |
| `[...path]` file routes | Traversal to `../../etc/passwd` | Resolve against a base directory and verify the resolved path is still inside it |
| SQL/ORM string interpolation | Injection | Parameterized queries; the ORM's raw escape hatch is where this reappears |
| JSON `+server.js` with cookie auth | Kit's origin check targets form-encoded submissions, so a JSON endpoint authenticated purely by cookie is the CSRF gap | `sameSite` cookie plus a required custom header or token, or keep the mutation in a form action |
| Uploaded files | Content type from the extension, executed on serve | Validate from the bytes, store outside the served root or in object storage, serve with `content-disposition` |

## Headers, Framing, and CSP

- Clickjacking on authenticated pages: `frame-ancestors 'none'` in the CSP directives (the modern replacement for `X-Frame-Options`).
- CSP is configured through `kit.csp` in `svelte.config.js` so Kit can hash or nonce its own hydration script; a hand-rolled header that omits that produces a page which renders and never becomes interactive (deployment guidance in the SKILL.md Quick Reference).
- `strict-transport-security`, `x-content-type-options: nosniff`, and a `referrer-policy` belong in the same `handle` hook, applied to every response rather than per route.
- `filterSerializedResponseHeaders` decides which upstream headers ride along in the SSR payload; the default of none is a privacy default, not an oversight.

## Security Checklist

- Authentication in `handle`, authorization repeated in every load, action, and endpoint that reads or writes data
- Session cookie `httpOnly` + `secure` + `sameSite`, id rotated on login and privilege change, logout deleting the server row
- Every protected endpoint verified with a direct request carrying no cookie, and with a second user's cookie
- Passwords hashed with argon2id/bcrypt on a runtime that can run them; identical response for unknown user and wrong password
- Load return values narrowed to rendered fields; no hash, token, or internal id in the payload
- `{@html}` sanitized server-side; `?next=` redirects restricted to same-site paths
- CSP through `kit.csp` with `frame-ancestors`, plus HSTS and `nosniff` on every response
