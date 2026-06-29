# Credential Issue (web-browser topic)

Take a **service** + **command** as parameters, open the service's login screen via the detected
browser backend, wait for the user to sign in, then on a completion signal **issue the requested
access key / token / secret** and hand the result to follow-up automation (aws-cli upload, `gh secret
set`, terraform var injection, etc.).

This generalizes the "open the page + user interaction + collect the result" pattern into a reusable
parameterized flow. It is the credential-issuance counterpart to [ui-test.md](./ui-test.md).

## Parameters

| Param | Meaning | Example |
|-------|---------|---------|
| `service` | The provider whose console issues the credential | `cloudflare-r2`, `github`, `oci`, `aws`, `authentik` |
| `command` | What to issue / do once logged in | `issue R2 S3 token`, `issue fine-grained PAT`, `create OAuth app` |
| `login-url` | Direct URL to the issuance page (when known) | `https://dash.cloudflare.com/?to=/:account/r2/api-tokens` |
| `handoff` | Follow-up automation to run with the issued credential | `aws s3 cp`, `gh secret set`, `vault kv put` |

## Backend selection (Step 0 + credential-specific preference)

Detect the backend via **SKILL.md Step 0** first. For credential issuance the preference order
differs from ui-test, because the user must **sign in** and reusing their real logged-in session is
fastest:

| Priority | Backend | Why | When |
|----------|---------|-----|------|
| 1 | **chrome-devtools** (real session) | Reuses the user's already-logged-in browser session — often no login needed | `chrome-devtools-mcp` connected |
| 2 | **Default browser** (`Start-Process <url>` / `open <url>`) | Opens the user's real browser (real session, fully interactive) | login-required + chrome-devtools absent |
| 3 | **wmux/cmux panel** | User-visible panel, interactive | `$WMUX` / `$CMUX_SESSION` set |
| 4 | Playwright MCP | **Last resort** — invisible window, user cannot log in interactively | only when a persisted/automated session already exists (no fresh login needed) |

**Key rule**: Playwright MCP opens an **invisible** window — the user cannot complete an interactive
login there. For any flow that needs a fresh user sign-in, prefer chrome-devtools (real session) or
the user's default browser. Do not drive an interactive login through invisible Playwright.

**Disconnected automatable backend → offer reconnect before degrading**: if the priority-1
automatable backend (chrome-devtools) is *disconnected*, do NOT silently fall to the manual
default-browser path. The gap is large — chrome-devtools drives the whole token-generation UI
(navigate → fill → click Create → snapshot-extract the token), whereas default browser is fully
manual (the user does every click). Surface the disconnection and offer to reconnect via `/plugin`
(chrome-devtools) first; fall to default browser only after the user declines reconnect or it fails.
The static priority table picks the highest *currently-connected* backend — but a disconnected MCP is
reconnectable, so treat "disconnected" as a reconnect-offer trigger, not a terminal fact, whenever
the flow benefits from backend automation.

## Procedure (automation-first, then login-assisted)

1. **Check stored credentials first (MANDATORY)** — before opening any browser, look in: skill `data/`
   files, project memory, `.env`, the secret store (`vault kv get`, `gh secret list`). If the
   credential already exists and is valid, **skip issuance** and go straight to `handoff`.
2. **Try API/SDK issuance (1st)** — if the provider exposes a token-issuance API and you hold a
   parent credential with sufficient scope, issue programmatically (no browser).
3. **Confirm API impossibility** — verify one of: the console is the only issuance path (e.g., R2
   "Public Development URL" + S3 token, PAT issuance is UI-only), the parent token lacks scope, or
   the SDK does not expose the flow.
4. **Login-assisted issuance (2nd)** — via the selected backend:
   - Open `login-url` (or the service console root) in the **visible** backend.
   - Inspect state (snapshot) — is the user already logged in, or is a login screen shown?
   - **If login required → wait for the user.** Tell them exactly what to do: "I opened {URL}.
     Please sign in and {command}, then tell me the {values}." Provide the direct URL. **Do not close
     the browser** while waiting (an isolated/invisible browser on a login screen is kept open, not
     closed — let the user sign in).
   - Wait for the user's completion signal (their message with the issued values, or an
     AskUserQuestion answer).
5. **Collect the result** — receive the issued access key / token / secret / endpoint / public URL
   from the user (or scrape it from the page if the backend can read it post-issuance).
6. **Persist (HARD STOP — before handoff)** — every issued/refreshed credential MUST land in a reusable secret store so the next session does not re-issue. Persistence comes **before** any revoke discussion. See the Service × Store matrix below; pick the row matching `service`. Missing persistence = the same browser dance every session = procedural defect.
7. **Hand off to automation** — run `handoff` with the credential (`gh secret set`, `aws s3 cp`, `vault kv put`, etc.) only after step 6 succeeds.
8. **Forbidden**: ending with only "please go to {URL} and issue it yourself" with no browser opened
   and no follow-up.
9. **Forbidden**: suggesting revoke/Delete on a freshly issued credential because "it appeared in chat output". Chat exposure is downstream of persistence — the credential's job is to be usable across sessions. Revoke is a separate explicit decision, not the default response to exposure.

### Service × Store matrix (Step 6 Persist)

Pick the matching row before declaring step 6 complete. If your service isn't listed, default to the generic password-manager / Vault row.

| Service / token type | Primary store (preferred) | Persist command | Reuse path |
|---------------------|---------------------------|-----------------|------------|
| GitHub PAT (classic / fine-grained) | **gh CLI keyring** (OS-native — macOS Keychain / Windows Credential Manager / libsecret) | `echo <token> \| gh auth login --hostname github.com --with-token` | `gh auth token -u <user>` (and Docker uses `~/.docker/config.json` after `docker login` once) |
| GitHub Actions repo/org secret | **GitHub secret store** | `gh secret set <NAME> -b<token>` | Workflow `${{ secrets.NAME }}` |
| AWS access key / secret | **Vault** (preferred) or `~/.aws/credentials` profile | `vault kv put secret/aws/<profile> access_key=... secret_key=...` OR `aws configure --profile <name>` | `AWS_PROFILE=<name>` / `vault kv get -field=secret_key secret/aws/<profile>` |
| Cloudflare R2 S3 token | **Vault** | `vault kv put secret/r2/<bucket> access_key=... secret_key=...` | `vault kv get -field=secret_key secret/r2/<bucket>` |
| OCI API key | **`~/.oci/config`** (CLI-native) | append profile section + `oci_cli_rc` if needed | `OCI_CLI_PROFILE=<name>` |
| Authentik admin token | **Vault** | `vault kv put secret/authentik/<env> token=...` | `vault kv get -field=token secret/authentik/<env>` |
| Vault root/unseal | **External password manager** (Bitwarden / 1Password) — Vault cannot store its own root | manual entry in password manager — never plaintext in repo | password manager retrieval |
| Slack / Discord webhook | **Vault** or `gh secret set` (if used by GH Actions) | `vault kv put secret/<provider>/webhook url=...` | `vault kv get` |
| Anthropic / OpenAI API key | **Vault** or `.env` (chmod 600, gitignored) | `vault kv put secret/anthropic key=...` or `echo ANTHROPIC_API_KEY=... >> ~/.env` | `vault kv get` or `source ~/.env` |
| Generic / unlisted | **Vault** (preferred) → password manager → `.env` (chmod 600, gitignored) | provider-appropriate | provider-appropriate |

**Why this matrix exists**: without a per-service store, every fresh issuance is followed by either (a) the token rotting in chat history (b) re-issuance the next session. Both are procedural defects — persistence is the goal, not a side step.

## Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | End with "issue it from the {service} console yourself" + stop | Open the console in a visible backend → guide the exact steps → collect the result → run `handoff` |
| 2 | Drive an interactive login through invisible Playwright MCP | Use chrome-devtools (real session) or the user's default browser for fresh logins. Playwright MCP only when a session already exists |
| 3 | Close the browser when it lands on a login screen | Keep it open; ask the user to sign in, then continue |
| 4 | Skip the stored-credential check and open a browser immediately | Check skill data / memory / `.env` / secret store first — reuse if present |
| 5 | Collect the credential then stop ("now you have a token") | Run `handoff` with it + store it for reuse. Issuance is a means, the handoff is the goal |
| 6 | Hardcode one provider's flow | Parameterize on `service` + `command`. Provider specifics go in the scenarios table / the caller's args |
| 7 | Leave an issued secret only in chat | Persist to the secret store (`vault kv put`, `gh secret set`) so it is reusable and not lost |
| 8 | After user login completes, delegate the **token generation steps** (clicking "New Token", selecting scopes, clicking "Create", copying value) to the user with text instructions | Once logged in, **drive the token-generation UI via the backend** (chrome-devtools `click`/`fill`/`take_snapshot`) and **extract the token from the page snapshot** programmatically. User typing/copying is a fallback when backend extraction fails (e.g., token shown as `••••` masked, password manager intercepts) |
| 9 | Treat "wait for user" as applying to the entire issuance flow | "Wait for user" applies to **(a) interactive login** and **(b) token reveal/copy when the token is masked or only shown once outside the DOM**. Token generation form-filling and "Create" click are backend-automatable when the user is logged in |
| 10 | Suggest revoke/Delete the freshly issued credential because it appeared in chat output ("token exposed → revoke first") | Persistence wins. Run step 6 Persist (Service × Store matrix) **before** any revoke consideration. Revoke is a separate explicit user decision; chat-exposure-triggered auto-revoke is forbidden. Reusing the token across sessions is the design goal |
| 11 | Skip step 6 Persist ("we'll just use it in this session") | Persist is HARD STOP. Every credential issuance ends in the secret store, not in shell history alone. Future sessions retrieve, not re-issue |
| 12 | Treat the matrix as PAT-only — pick gh keyring for everything | Match the row to the credential type. AWS keys → vault/`~/.aws`, OCI → `~/.oci/config`, Vault root → password manager (Vault can't store itself), Anthropic → vault/`.env`. Wrong row = unusable persistence |

### Scope expansion / token refresh (HARD STOP — Settings UI first, CLI fallback)

**Token-refresh / OAuth scope expansion is the same shape as new issuance** — open the provider's Settings/Tokens page via the detected backend, let the user edit scopes (or issue a new token), capture the token, hand off. Driving `gh auth refresh` from a Bash prompt is a fragile path (CLI flag mismatches across versions, multi-account switching, device-code UX in nested shells); **prefer Settings UI** for human-in-the-loop control.

#### Trigger forms

| Form | Example | Mapping |
|------|---------|---------|
| GHCR pull denied → missing `read:packages` | `docker pull ghcr.io/.../image:tag` → `denied` + `www-authenticate: Bearer scope="repository:.../image:pull"` | service=`github`, command=`pat-scope-add`, args=`read:packages` (default scope-set per git.md PAT matrix) |
| GitHub PAT scope add via Settings UI | "PAT needs `workflow` scope to push CI yml" | service=`github`, command=`pat-edit`, target=token id |
| `gh auth refresh -s <scopes>` (CLI fallback) | `gh auth refresh -h github.com -s read:packages,repo,read:org,workflow,copilot` (active account only; for inactive account run `gh auth switch -u <user>` first) | service=`github`, command=`refresh-cli`, args=scope list |
| OAuth re-authorize (3rd party app needs new scope) | Slack/Discord/Notion OAuth app scope upgrade | service=`<provider>`, command=`oauth-reauthorize` |
| Device-code re-auth (gh, az, gcloud) | `gh auth login --web` / `az login --use-device-code` | service=`<cli>`, command=`device-auth` |

#### Procedure (Settings UI first — Recommended)

1. **Scope-set default** — per git.md PAT scope matrix: `read:packages,repo,read:org,workflow,copilot` (5 cumulative scopes). Narrow only when caller explicitly requires (e.g., `write:packages` only for publish operations).
2. **Identify token** — `gh auth status` to list accounts and confirm which user/PAT needs scope expansion. For inactive accounts, do not auto-switch — surface the multi-account choice to the user first.
3. **Open Settings UI in detected backend** — for GitHub PAT scope edit/issue:
   - Classic PAT edit: `https://github.com/settings/tokens` (token list → select existing → Edit → check missing scopes → Update token → copy new value if regenerated)
   - Classic PAT new: `https://github.com/settings/tokens/new?scopes=<comma-separated>&description=<note>` (pre-fills scope checkboxes)
   - Fine-grained PAT: `https://github.com/settings/personal-access-tokens/new`
   - Drive via cmux/wmux panel or chrome-devtools so the user sees the page in real time.
4. **Collect token** — receive the new token value via user paste (token reveal screen is shown once). The skill's existing "wait for user" rule applies (Don't/Do #5).
5. **Verify** — re-run the failed operation (e.g. `docker login ghcr.io -u <user> --password-stdin` + `docker pull <image>`) to confirm scope works. Failure = inspect `www-authenticate` header for remaining missing scope.
6. **Persist** — store token in the secret store (`gh auth login --with-token <`, password manager, Vault) so future runs reuse it.
7. **Handoff** — chain into the downstream command (the operation that originally hit `denied`).

#### Procedure (CLI fallback — when Settings UI is blocked)

Use only when (a) browser unavailable, (b) explicit user request, (c) automation pipeline. **Verify gh CLI syntax via `gh auth refresh --help` before running** — flags differ across gh versions and there is **no `-u/--user` flag on `refresh`**:

```bash
# Active account refresh — direct
gh auth refresh -h github.com -s read:packages,repo,read:org,workflow,copilot

# Inactive account — switch first, then refresh, then switch back
# (gh auth status does not have a structured --json output for the active user
#  as of gh 2.x; parse the human-readable output instead and verify the
#  capture in your own shell before relying on it.)
ACTIVE_BEFORE=$(gh auth status 2>&1 | awk '/active account/{for(i=1;i<=NF;i++) if ($i ~ /^[A-Za-z0-9_-]+$/ && $i != "active") {print $i; exit}}')
gh auth switch -u <target-user>
gh auth refresh -h github.com -s read:packages,repo,read:org,workflow,copilot
[ -n "$ACTIVE_BEFORE" ] && gh auth switch -u "$ACTIVE_BEFORE"
```

The device-code prompt appears in the terminal; the user enters it in the browser. Wait for `gh auth status` to show the new scope list.

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Output `gh auth refresh ...` text to the user and stop ("paste this yourself") | Open the Settings UI in a visible backend; CLI fallback only when explicitly chosen |
| 2 | Cite `-u/--user` on `gh auth refresh` (the flag does not exist) | Verify each CLI flag via `<cmd> --help` before placing it in a rule body. Cross-account refresh uses `gh auth switch` |
| 3 | Refresh only the missing scope (`read:packages` alone) — causes future re-refresh for the next missing scope | Default to git.md PAT matrix 5-scope set; only narrow when explicitly required |
| 4 | Treat `gh auth refresh` as "user-only command" outside skill scope | Skill owns the Settings UI path; CLI is the fallback layer of the same skill, not an out-of-scope shortcut |
| 5 | Skip when `gh auth status` shows the account is "logged in" (assume scope is fine) | "Logged in" ≠ "has required scopes". Always cross-check the scope list against the failing operation's PAT matrix entry |

### Login provider preference — GitHub SSO first for Azure/Microsoft (HARD STOP)

**Azure DevOps, VS Code Marketplace publisher, Microsoft Learn, Azure portal, and other Microsoft-account-gated services that accept GitHub SSO MUST use the GitHub sign-in option** instead of direct Microsoft account login.

#### Why

- The user's GitHub account (e.g., `DrumRobot`) is already mapped + auth maintained (gh CLI, browser session, PAT). Reuse it instead of a separate Microsoft account login round-trip
- Microsoft account login often triggers extra MFA prompts / phone verification / device verification. GitHub session is already authenticated on the user's browser
- Single identity surface = easier secret rotation + audit. Azure DevOps user identity links back to GitHub (`@github` suffix), making it traceable in repo audit logs
- vsce / ovsx publisher accounts can be linked to either, but consolidating on GitHub keeps the credential trail single-source

#### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Open `https://login.microsoftonline.com` directly and ask user to enter Microsoft account password | Open the service (Azure DevOps / Marketplace) and click **"Sign in with GitHub"** (or equivalent third-party SSO button) |
| 2 | Drive Microsoft account 2FA flow through automation | Switch to GitHub SSO — fewer hurdles, reuses existing browser session |
| 3 | Assume "Microsoft service = Microsoft account" without checking | Most Azure DevOps orgs accept GitHub SSO. Check the sign-in page for a "GitHub" button before defaulting to MS account |
| 4 | After failed MS account login, retry MS account with different email | If MS account flow fails / requires verification, switch to GitHub SSO immediately |

#### Self-check (before opening a Microsoft service login page)

1. Does the target service accept GitHub SSO? — Azure DevOps ✅, VS Code Marketplace ✅, Microsoft Learn ✅, Azure portal ⚠️ (org-policy dependent — fall back to MS account)
2. Is the user already signed into GitHub in this browser session? — If yes, GitHub SSO completes in 1-2 clicks (consent screen) vs MS account 3-5 clicks (email → password → 2FA → consent)
3. On the sign-in page snapshot, look for "Sign in with GitHub" / "Continue with GitHub" / GitHub Octocat icon → click that, not the MS account input

#### Scenarios

| Service | GitHub SSO URL pattern | Notes |
|---------|------------------------|-------|
| Azure DevOps (PAT issuance) | `https://dev.azure.com/<org>/_usersSettings/tokens` → "Sign in with GitHub" button on the login screen | The same MS account email backed by GitHub appears as `user@github` in Azure DevOps |
| VS Code Marketplace publisher | `https://marketplace.visualstudio.com/manage/publishers/<publisher>` → GitHub SSO via the same Azure DevOps identity | Publisher = Azure DevOps org membership |
| GitHub itself | direct (no SSO needed) | gh CLI session covers it |

### Boundary: login wait vs token automation

| Phase | Who does it | Why |
|-------|-------------|-----|
| 1. Authentication (Microsoft / OAuth / SSO sign-in) | User (interactive) | Security: credentials must stay with the user; backend cannot enter passwords or pass 2FA |
| 2. Navigation to the token issuance page | Backend (`navigate_page` / `new_page`) | Once authenticated, page navigation is automatable |
| 3. Form fill (token name, scopes, expiration) | **Backend** (`fill` / `click`) | These are deterministic form inputs the caller decided from `command` |
| 4. Click "Create" / "Generate" | **Backend** (`click`) | Automatable |
| 5. Extract the issued token value | **Backend** (`take_snapshot` → parse the textbox containing the token) — fallback to user copy only when the token is masked / behind a copy-only button | The token is visible in the page after generation; extract directly. User-typed input is fragile (typos, partial paste) |
| 6. Handoff (`gh secret set`, `vault kv put`, local CLI publish) | **Backend** (Bash) | Mandatory automation |
| 7. Persist for reuse (skill `data/secrets/`, keychain) | **Backend** (Write) | Mandatory automation |

## Self-check (before opening any browser for issuance)

1. Is the credential already stored (skill data / memory / `.env` / secret store)? → If yes, skip to `handoff`.
2. Can it be issued via API/SDK with a parent credential? → If yes, do that (no browser).
3. Console-only? → Pick the backend: chrome-devtools (real session) > default browser > wmux/cmux > Playwright (only with an existing session).
4. Does the flow need a fresh interactive login? → If yes, the backend MUST be user-visible. Never invisible Playwright.
5. After collecting the credential, did you **complete step 6 Persist** (Service × Store matrix row matched + persist command executed + reuse path verified)? `handoff` runs only after Persist succeeds.
6. **Login complete → token generation automation check**: once the user is signed in, did the backend drive the token-generation UI (navigate → fill → click "Create" → snapshot the token) instead of writing text instructions for the user to follow? If text instructions were written, that is a violation of the boundary in the table above unless the token is genuinely behind a masked / copy-only UI element.
7. **Persist-before-revoke check**: am I about to suggest revoke/Delete the freshly issued credential because it appeared in chat? Persistence wins — step 6 first; revoke is a separate explicit user decision, not the default exposure response.

## Scenarios

| service / command | API issuance? | Login-assisted issuance (console URL) | handoff |
|-------------------|---------------|----------------------------------------|---------|
| `cloudflare-r2` / issue S3 token + public URL | ❌ console-only (Public Dev URL + token) | `https://dash.cloudflare.com/?to=/:account/r2/overview` → enable R2 → create bucket → Public Development URL → Manage R2 API Tokens | `aws s3 cp --endpoint-url https://<acct>.r2.cloudflarestorage.com` upload → public `https://pub-*.r2.dev/<key>` |
| `github` / issue fine-grained PAT | ❌ security (UI-only) | `https://github.com/settings/personal-access-tokens/new` | `gh secret set` / git remote auth |
| `github` / create OAuth app | ❌ UI-only | `https://github.com/settings/developers` | store client id/secret in `vault kv put` |
| `oci` / Customer Secret Key | ❌ console-only | OCI console → User → Customer Secret Keys | rclone/aws-cli S3 config |
| `authentik` / akadmin API token | ✅ (terraform/API) | (only if console needed) | terraform var / `vault kv put` |
| `vsce` (VS Code Marketplace publisher) / issue Azure DevOps PAT for `vsce publish` | ❌ UI-only (Azure DevOps Personal Access Token) | `https://dev.azure.com/<org>/_usersSettings/tokens` — `<org>` is the Azure DevOps organization linked to the Marketplace publisher (if not provided by caller, **ask via AskUserQuestion** before opening the page). Sign in via "Sign in with GitHub" SSO (see "Login provider preference" above). Token scope: `Marketplace > Manage` | `gh secret set VSCE_PAT -R <owner>/<repo>` + local `npx vsce publish --packagePath <vsix> --pat $VSCE_PAT` |
| `ovsx` (Open VSX Registry publisher) / issue Open VSX PAT for `ovsx publish` | ❌ UI-only | `https://open-vsx.org/user-settings/tokens` — sign in via the **GitHub** option (Open VSX is GitHub-SSO native) | `gh secret set OVSX_PAT -R <owner>/<repo>` + local `npx ovsx publish <vsix> -p $OVSX_PAT` |
| any / register a GitHub Secret | ✅ `gh secret set` | (not needed) | — |

## Note on GitHub PR image hosting (why R2)

GitHub renders inline images via a **Camo proxy** that fetches from GitHub's servers — it **cannot
reach internal hosts** (e.g., `10.0.0.x` MinIO, tailnet `*.ts.net`). A capture hosted on an internal
store will not render inline in a PR. **Cloudflare R2 with a public `r2.dev` / custom-domain URL is
publicly reachable**, so Camo can fetch it → the image renders inline. This is the canonical use of
`service: cloudflare-r2` for PR capture attachment.
