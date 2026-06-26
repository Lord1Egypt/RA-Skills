# SSO Verification

Automatically verify the Authentik SSO login flow using Playwright.

## When to Use

- After deploying Authentik + dt app to dev/integration server
- To confirm redirect target after changing an OAuth Source URL
- To test the entire login flow end-to-end

## Verification Checklist

| # | Item | Success Criteria | Failure Signal |
|---|------|-----------------|----------------|
| 1 | Authentik accessibility | Login page loads (heading "Login" or form element present) | "authentik starting", blank page |
| 2 | Redirect target | URL navigates to the intended server | Redirect to different server IP/port (Blueprint drift) |
| 3 | OAuth authorize | dt app's authorize endpoint responds normally | `unauthorized_client`, 404, 405 |
| 4 | Login complete (initial) | Dashboard redirect after login | Infinite redirect, error page |
| 5 | **Re-login (post-logout)** | **Auto-completes to dt dashboard OR Authentik `/if/user/` WITHOUT re-showing the Authentik login form** | **`/if/flow/default-authentication-flow/` (Authentik login form) re-appears = duplicate-login regression** |

## Re-login (post-logout) success criterion (HARD STOP — do not conflate with initial login)

**Initial login and re-login have DIFFERENT success criteria.** During **initial** login the Authentik login form (`default-authentication-flow`) is the normal entry point (Step 4 below). During **re-login** (the user already authenticated once, logged out, and logs in again while a valid dt session can be re-established), the SSO source flow MUST auto-complete — re-showing the Authentik login form is a **duplicate-login regression**, NOT a dashboard.

| State | `default-authentication-flow` (Authentik login form) | Verdict |
|-------|------------------------------------------------------|---------|
| Initial login (no prior auth) | Expected entry point — enter credentials | ✅ Normal |
| **Re-login** (logout → log in again) | **Re-appears = the user is asked to log in AGAIN after already logging in = duplicate-login screen** | ❌ **Regression (FAIL)** |

### Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Treat "dashboard eventually reachable after manually clicking a source button (e.g. 'Continue with …')" as a re-login pass | A re-login that lands on `default-authentication-flow` is a FAIL even if a manual source-button click later reaches the dashboard. Manual interaction = not auto-complete = duplicate login |
| 2 | Evaluate only the END state ("did it reach the dashboard?") | Evaluate the FULL path: re-login must reach dashboard/`if/user/` **without** an intermediate Authentik login form |
| 3 | Offer "pass / mark test plan [x]" when the re-login showed the login form | The intermediate `default-authentication-flow` is the regression. Do not offer "pass" — report it as FAIL |
| 4 | `default-authentication-flow` URL == "dashboard" or "valid endpoint" | `default-authentication-flow` = Authentik login form (duplicate-login screen). Success endpoints are dt dashboard (`integrated-dashboard`) or Authentik `/if/user/` |

### Self-check (every time before reporting a re-login verdict)

1. Is this an **initial** login or a **re-login** (post-logout)? — different criteria
2. For re-login: did the URL pass through `/if/flow/default-authentication-flow/` (Authentik login form) at any point requiring user interaction? → If yes, **FAIL** (duplicate login)
3. Did the flow auto-complete to `intergrated-dashboard` or `/if/user/` **without** a manual auth-form/source-button click? → Only then is it a PASS
4. Do not offer "pass" / "mark test plan [x]" to the user when (2) is yes

## Procedure

### Step 1: Environment Detection + Setup

Run **SKILL.md Step 0** first to detect `$WMUX` / `$CMUX_SESSION`.

| Environment | Setup | Commands below use |
|-------------|-------|-------------------|
| wmux/cmux (`$WMUX` or `$CMUX_SESSION` set) | Ready immediately | `wmux browser open/snapshot/click/type` via Bash |
| Plain / tmux | Register Playwright (SKILL.md Step 1-2) | `mcp__playwright__*` or `code-mode call_tool_chain` |

### Step 2: Navigate to Authentik Login Page

**wmux:**
```bash
wmux browser open "http://<host>:9000/if/flow/default-authentication-flow/"
# wait a few seconds for page load
wmux browser snapshot
```

**Playwright:**
```typescript
playwright.playwright_browser_navigate({ url: 'http://<host>:9000/if/flow/default-authentication-flow/' });
playwright.playwright_browser_wait_for({ time: 5 });
const snapshot = playwright.playwright_browser_snapshot();
```

### Step 3: Confirm Redirect Target

Analyze the **Page URL** from the snapshot:

| URL Pattern | Meaning | Action |
|-------------|---------|--------|
| `http://<same-host>:<dt-port>/deps_emc/api/oauth/authorize?...` | Normal — redirected to dt app on same server | Go to Step 4 |
| `http://<different-host>/deps_emc/api/oauth/authorize?...` | Blueprint drift — redirected to a different server | DB UPDATE required (see below) |
| `http://<host>:9000/...` (self) | OAuth Source not configured or not connected to flow | Check Authentik admin |
| "authentik starting" or blank page | Server is starting up | Wait and retry |

### Step 4: Check OAuth Authorize Response

Detect errors from the snapshot of the redirected page:

| Response | Cause | Fix |
|----------|-------|-----|
| `{"error":"unauthorized_client"}` | The `client_id` is not registered in the dt app | Check dt app env var `OAUTH_SOURCE_CLIENT_ID` or add the client to the allowed list in code |
| 404 Not Found | `/api/oauth/authorize` endpoint missing | Rebuild dt app image (OAuth Provider code not included) |
| 405 Method Not Allowed | GET not supported | OAuth authorize requires GET; check route handler |
| Login form displayed | Normal — dt app redirecting unauthenticated user to login | Proceed to login |

### Step 5: Login Test (Optional)

If a login form is displayed:

**wmux:**
```bash
wmux browser snapshot                          # find @eN refs for username/password fields
wmux browser type @eN akadmin                  # enter username
wmux browser type @eM <PASSWORD>               # enter password
wmux browser click @eK                         # click submit button
wmux browser snapshot                          # verify result
```

**Playwright:**
```typescript
playwright.playwright_browser_type({ ref: '<username_ref>', text: 'akadmin' });
playwright.playwright_browser_type({ ref: '<password_ref>', text: '<PASSWORD>', submit: true });
playwright.playwright_browser_wait_for({ time: 3 });
playwright.playwright_browser_snapshot();
```

## When Blueprint Drift is Detected

If the redirect points to a different server, fix it with ansible:

```bash
# dry-run
make -C ansible blueprint-<env>-diff

# apply (includes DB UPDATE)
make -C ansible blueprint-<env>-deploy
```

Or manual DB UPDATE:

```bash
ssh <host> "docker exec authentik-postgres psql -U authentik -d authentik -c \"
  UPDATE authentik_sources_oauth_oauthsource
  SET authorization_url='http://<DT_HOST>/deps_emc/api/oauth/authorize',
      access_token_url='http://<DT_HOST>/deps_emc/api/oauth/token',
      profile_url='http://<DT_HOST>/deps_emc/api/oauth/userinfo';
\""
```

Details: `.ralph/docs/generated/authentik-blueprint-drift.md`

## Report Format

```md
## SSO Verification Result

**Server:** <host>:<port>
**Authentik:** <authentik_url>

| # | Item | Result |
|---|------|--------|
| 1 | Authentik access | OK / FAIL |
| 2 | Redirect target | <actual URL> (normal/drift) |
| 3 | OAuth authorize | OK / unauthorized_client / 404 |
| 4 | Login complete | OK / FAIL |

### Issues Found
- [describe if any]

### Actions Taken
- [describe if any]
```
