# Chrome QR Code Login + Footer Dot Toggle

**Date:** 2026-04-07
**Authors:** Parker Todd Brooks, cc-mini
**Status:** building

## Context

WebAuthn `authenticatorAttachment: "cross-platform"` shows a native QR code in Safari but "Insert security key" in Chrome on macOS. We need a custom server-generated QR code flow for Chrome so users can create passkeys on their phone from any desktop browser. Also replacing the "Turn on/off local passkeys" text with a colored dot indicator.

## Files to modify

1. **`src/hosted-mcp/server.mjs`** ... add 4 new endpoints (same pattern as agent auth)
2. **`src/hosted-mcp/demo/login.html`** ... Chrome detection, QR view, phone-side session handling, footer dot

## Server changes (server.mjs)

**New in-memory store** (near line 184, next to `agentAuthChallenges`):
```
qrLoginSessions = {}  // sessionId -> { qrBuffer, status, agentId, apiKey, handle, expires }
QR_LOGIN_EXPIRY_MS = 5 * 60 * 1000
```

**4 new endpoints** (reuse exact patterns from agent auth at lines 1035-1373):

| Endpoint | Pattern source | What it does |
|---|---|---|
| `POST /api/qr-login` | `handleAgentAuthStart` (line 1036) | Creates session, generates QR PNG encoding `wip.computer/login?s=SESSION_ID&h=HANDLE` |
| `GET /api/qr-login/qr?s=XXX` | `handleAgentAuthQR` (line 1058) | Serves QR PNG |
| `GET /api/qr-login/status?s=XXX` | `handleAgentAuthStatus` (line 1071) | Poll: returns pending or approved. One-time use (deletes after approved read) |
| `POST /api/qr-login/approve` | `handleAgentAuthApprove` (line 1353) | Phone calls after passkey created. Sets status=approved with agentId + apiKey |

Add cleanup to existing `cleanupExpiredChallenges()` at line 314.

Note: endpoints under `/api/` not `/demo/api/` since this is production, not demo.

## Login page changes (login.html)

**1. Browser detection:**
```javascript
function isSafariDesktop() {
  if (isMobileDevice()) return false;
  return /Safari\//.test(navigator.userAgent) && !/Chrome\//.test(navigator.userAgent);
}
// needsCustomQR = !mobile && !isSafariDesktop() && !localPasskeysOn
```

**2. QR view HTML** (new div between signup-view and success-view):
- "Scan with your phone to create a passkey."
- QR code `<img>` loaded from `/api/qr-login/qr?s=XXX`
- "Waiting for phone..." status text
- Cancel button to go back to signup-view

**3. Modified doCreateAccount flow:**
- If `needsCustomQR`: call `startQrLogin(handle)` instead of WebAuthn
- `startQrLogin`: POST `/api/qr-login`, show QR image, poll every 2s
- `pollQrLogin`: GET `/api/qr-login/status`, on approved show success view
- `cancelQrLogin`: stop polling, return to signup view
- Safari/mobile/localOn: unchanged (existing WebAuthn flow)

**4. Phone-side detection:**
- On page load, check `URLSearchParams` for `?s=SESSION_ID`
- If present + mobile: set `window.qrSessionMode = true`, pre-fill handle from `?h=`
- After successful passkey creation (register or sign-in), call `POST /api/qr-login/approve`
- Clean URL with `history.replaceState`

**5. Footer dot:**
- Replace "Turn on/off local passkeys" text with: `<span>` dot (8px circle) + "Local passkeys" text
- Red dot (opacity 0.4) = off (default)
- Green dot (opacity 1) = on
- Click toggles, updates localStorage + dot color

## Flow summary

**Chrome desktop (local passkeys off):**
1. Click "Look Inside" -> POST `/api/qr-login` -> show QR code
2. Phone scans QR -> opens `wip.computer/login?s=XXX`
3. Phone: Face ID -> passkey created -> POST `/api/qr-login/approve`
4. Desktop poll detects approved -> shows "Welcome"

**Safari desktop (local passkeys off):**
Native WebAuthn cross-platform (unchanged)

**Mobile (any browser):**
Face ID directly (unchanged)

**Any desktop (local passkeys on):**
Native OS dialog with all options (unchanged)

## Nginx

Need to add `/api/qr-login` proxy rules to mcp-oauth.conf (same as `/api/pair/`).

## Verification

1. Chrome desktop: "Look Inside" shows QR code, phone scan completes registration
2. Safari desktop: native QR dialog still works
3. Mobile: Face ID directly, no QR
4. Footer dot: red when off, green when on, persists across refresh
5. Local passkeys on: Chrome shows native OS dialog
6. QR session expires after 5 minutes

## Cross-references

- `ai/product/plans-prds/kaleidoscope/2026-04-07--cc-mini--features-to-preserve-from-demo.md`
- `ai/product/plans-prds/kaleidoscope/2026-04-06--cc-mini--kaleidoscope-architecture.md`
- Demo agent auth: `src/hosted-mcp/demo/agent.html` + server `/demo/api/agent-auth`
- Demo approve page: server `handleApprovePage` (line 1088)
