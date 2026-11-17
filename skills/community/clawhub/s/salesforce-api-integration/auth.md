# Auth — Connected Apps, OAuth Flows, and Orgs

**Before any call**, read `## Org Context` in `~/Clawic/data/salesforce-api-integration/memory.md` — or `orgs.md` if the `## Boxes` index points there. The instance URL, API version, auth flow and credential pointer for each org live there, sandboxes included. Guessing an instance URL is the most common way to spend an hour on a working integration.

**Contents:** [Pick the Flow](#pick-the-flow) · [JWT Bearer](#jwt-bearer-the-server-to-server-default) · [Web Server Flow](#web-server-flow-a-human-is-present) · [Refresh Token](#refresh-token) · [Client Credentials](#client-credentials) · [Device Flow](#device-flow) · [The Connected App Itself](#the-connected-app-itself) · [The Integration User](#the-integration-user) · [Instance URL and My Domain](#instance-url-and-my-domain) · [Sandboxes](#sandboxes) · [Session Lifetime](#session-lifetime) · [Auth Failures](#auth-failures)

## Pick the Flow

| Situation | Flow | Why |
|---|---|---|
| Server, cron, ETL — no human ever present | **JWT bearer** | No secret in transit, no refresh token to lose, no password to expire |
| A user logs in and the app acts as them | **Web server (authorization code + PKCE)** | The only flow that produces a per-user session legitimately |
| Long-lived background job that must act as a specific user who consented once | **Refresh token**, obtained from the web server flow | Survives session expiry; dies if the user's password changes or the token is revoked |
| Machine-to-machine where the org has designated a run-as user | **Client credentials** | Simplest server flow when it is enabled; returns no refresh token |
| CLI or a device without a browser | **Device flow** | User approves on their phone; you poll for the token |
| Anything, in 2026 | **Not username-password** | Salesforce has been disabling this flow by default, new orgs first. It also requires the user's password and security token in your config, which is two secrets you now own |

Default when nothing is stated: `auth_flow` = jwt-bearer.

## JWT Bearer (the server-to-server default)

Three preconditions, and every failure is one of them missing:

1. A certificate (self-signed is fine) uploaded to the Connected App's **Use digital signatures** field. You keep the private key; Salesforce keeps the public half.
2. The Connected App's **Permitted Users** set to *Admin approved users are pre-authorized*, and the integration user's profile or permission set assigned to the app. Without this, every attempt returns `invalid_grant` with `user hasn't approved this consumer`.
3. `aud` matching the environment: `https://login.salesforce.com` for production and developer orgs, `https://test.salesforce.com` for sandboxes. This is the single most common cause of a JWT that works in one org and not the other.

The assertion's claims: `iss` = Consumer Key, `sub` = the integration user's username (the *sandbox* username in a sandbox), `aud` as above, `exp` a few minutes out — Salesforce rejects a long-lived assertion, so mint a fresh one per token request rather than caching the JWT.

```bash
curl -X POST "https://login.salesforce.com/services/oauth2/token" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer" \
  -d "assertion=$SIGNED_JWT"
```

The response carries `access_token` and `instance_url` and **no refresh token** — that is the point. When the token expires you sign another assertion. Nothing to rotate, nothing to leak.

Certificates expire, usually a year out, and nothing warns you: the integration simply stops authenticating one morning. Put the expiry date in the `## Due` table of `memory.md` the day the cert is created.

## Web Server Flow (a human is present)

```
GET https://login.salesforce.com/services/oauth2/authorize
  ?response_type=code
  &client_id=<consumer key>
  &redirect_uri=<exact callback registered on the app>
  &scope=api%20refresh_token
  &code_challenge=<PKCE S256 challenge>
  &state=<csrf value you generated>
```

Then exchange the code:

```bash
curl -X POST "https://login.salesforce.com/services/oauth2/token" \
  -d "grant_type=authorization_code" \
  -d "client_id=$SF_CLIENT_ID" \
  -d "client_secret=$SF_CLIENT_SECRET" \
  -d "redirect_uri=$SF_CALLBACK" \
  -d "code=$CODE" \
  -d "code_verifier=$PKCE_VERIFIER"
```

- `redirect_uri` must match the registered callback **exactly**, including trailing slash and scheme. A mismatch is `redirect_uri_mismatch`, not a 404.
- Ask for `refresh_token` in scope only if you intend to keep acting later; `offline_access` is what keeps it valid while the user is away.
- Add `&prompt=login` to force re-authentication and `&login_hint=<username>` to preselect the user.

## Refresh Token

```bash
curl -X POST "$SF_LOGIN_HOST/services/oauth2/token" \
  -d "grant_type=refresh_token" \
  -d "client_id=$SF_CLIENT_ID" \
  -d "client_secret=$SF_CLIENT_SECRET" \
  -d "refresh_token=$SF_REFRESH_TOKEN"
```

The refresh token's lifetime is a Connected App policy, not a fixed value — "valid until revoked" is the default, but an org can set it to expire after a period of inactivity. Anything that invalidates the user's sessions (password change, admin revoke, the app being uninstalled) kills it too. Treat "refresh failed" as "re-run the interactive flow", never as "retry harder".

A refresh token is a permanent credential. It is the payload inside an `sfdx` auth URL, which is why that string is a secret and never goes in a file under `~/Clawic/data/`.

## Client Credentials

Available when the org has enabled it and designated a run-as user on the Connected App:

```bash
curl -X POST "$SF_LOGIN_HOST/services/oauth2/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=$SF_CLIENT_ID" \
  -d "client_secret=$SF_CLIENT_SECRET"
```

Every action is attributed to the run-as user, so audit trails show one name for the entire integration. That is a feature for support and a problem for compliance regimes that require per-actor attribution — decide before building.

## Device Flow

For a CLI or a headless box with a human somewhere: POST `grant_type=device_code` with the client id, show the returned `user_code` and `verification_uri`, then poll the token endpoint with the `device_code` until it stops returning `authorization_pending`. Respect the returned `interval`; polling faster earns `slow_down`.

## The Connected App Itself

- Changes take **up to ten minutes** to propagate. A brand-new app that returns `invalid_client_id` is usually not misconfigured, it is not deployed yet — wait before debugging.
- Scopes are a ceiling, not a grant: `api` for data access, `refresh_token`/`offline_access` to stay logged in, `web` for the UI, `id`/`openid` for identity. `full` is the lazy option and grants more than any integration needs.
- **Relax IP restrictions** on the app when the caller has no fixed IP; the alternative is whitelisting the caller's range in the profile's Login IP Ranges. Leaving both strict is what turns a working local script into `IP_RANGE_ERROR` in CI.
- The Consumer Key is public by design and belongs in the notes. The Consumer Secret does not, ever.
- Revoke a compromised token immediately at `POST /services/oauth2/revoke` with `token=<token>`; introspect a suspicious one at `/services/oauth2/introspect`, and read who a token belongs to at `/services/oauth2/userinfo`.

## The Integration User

The permissions of the user you authenticate as are the permissions of your integration — every FLS and sharing rule applies (Rule 7 in `SKILL.md`).

- Dedicated user, never a person's account. When the admin leaves the company, an integration bound to their login dies with their deactivation.
- Restrict the profile to API-only where the edition offers it: no UI login means a stolen token cannot be used to browse the org.
- Grant through a permission set, not the profile, so what the integration can do is one assignable object you can diff.
- Audit the set on a cadence — an object added last quarter is invisible to the integration until someone notices. Record the audit in `## Due`.
- `SELECT Id FROM User WHERE Username = '...'` before a load: an integration user that got deactivated fails every call with a session error that looks like a token problem.

## Instance URL and My Domain

Every org has a My Domain host (`https://<mydomain>.my.salesforce.com`), and the token response returns the exact `instance_url` to use. Use the returned value; store it on the org's row in `## Org Context` (or `orgs.md`). Salesforce moves orgs between instances, and a hardcoded legacy host resolves to nothing or to a redirect that eats your Authorization header.

The org id and My Domain name are working data, keep them. The session that reaches them is not.

## Sandboxes

| Type | Refresh interval | Contains |
|---|---|---|
| Developer | 1 day | Metadata only |
| Developer Pro | 1 day | Metadata only, larger storage |
| Partial Copy | 5 days | Metadata + a sample of data |
| Full | 29 days | Metadata + all data |

- Login host is `https://test.salesforce.com`; the My Domain form is `https://<mydomain>--<sandbox>.sandbox.my.salesforce.com`.
- **Sandbox usernames are the production username plus `.<sandboxname>`**. The password is whatever it was in production at refresh time — for the integration user, usually unknown, which is one more reason to use JWT.
- A refresh **resets the sandbox to production's state**: certificates and Connected App configuration have to be re-checked, the integration user's permission sets re-verified, and email deliverability is off by default so anything expecting a notification silently stops.
- External IDs survive a refresh; Salesforce ids do not match production's. Any mapping keyed on Salesforce id is worthless across orgs — this is the argument for external IDs in one sentence.
- Put the earliest legal refresh date in `## Due`; a full sandbox cannot be refreshed again for 29 days, so an unplanned refresh burns the window a release needed.

## Session Lifetime

Access tokens live as long as the org's session timeout, which is a setting (commonly two hours of inactivity, configurable from minutes to a day) — not a constant you can hardcode. Detect expiry, do not predict it: on 401 with `INVALID_SESSION_ID`, re-authenticate once and retry the call, and fail loudly on the second 401 rather than looping.

## Auth Failures

| Response | Cause | Fix |
|---|---|---|
| `invalid_grant` + `user hasn't approved this consumer` | JWT without pre-authorization | Permitted Users = admin approved, assign the profile/permission set to the app |
| `invalid_grant` + `invalid assertion` | `aud` wrong for the environment, or clock skew | `test.salesforce.com` for sandboxes; check the server clock, `exp` is minutes |
| `invalid_grant` on a sandbox that works in prod | Production username used as `sub` | Append `.<sandboxname>` |
| `invalid_client_id` | App not propagated, or key from the wrong org | Wait ten minutes; confirm which org the app lives in |
| `invalid_client` | Consumer Secret wrong, or the flow requires one and none was sent | JWT sends no secret; web server and refresh do |
| `redirect_uri_mismatch` | Callback differs by a character | Copy it from the app definition, do not retype it |
| `IP_RANGE_ERROR` | Caller's IP outside the profile's ranges | Relax IP restrictions on the app, or whitelist the range |
| 401 `INVALID_SESSION_ID` on a token minted seconds ago | Token sent to the wrong instance URL | Use the `instance_url` from that token response |
| Everything fails after a deactivation | The integration user was disabled | Reactivate or repoint; no token can outlive its user |

**Before finishing an auth session**: write the org's alias, type, instance URL, API version, flow and credential *pointer* into `## Org Context` — or `orgs.md` from the second org — and put any certificate or secret expiry into the `## Due` table of `memory.md`. Never write the token, the secret, the key or an `sfdx` auth URL; the pointer is `keychain:sf-prod`, `env:SF_CLIENT_SECRET`, `file:~/.certs/sf-jwt.key`.
