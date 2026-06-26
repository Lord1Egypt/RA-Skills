# Kaleidoscope: Architecture and Repo Layout

**Date:** 2026-04-06
**Authors:** Parker Todd Brooks, cc-mini

## What Kaleidoscope is

The consumer product. "Every AI. One experience." The app layer on top of LDM OS.

- `wip.computer` = the company (like openai.com)
- `kaleidoscope.wip.computer` = the product (like chatgpt.com)

## Repo layout (multi-repo, Pattern 2)

Code lives in the repo that matches the platform. Plans and bugs are tracked centrally in wip-ldm-os-private.

### Where code lives

| Repo | What | Deploy target |
|---|---|---|
| `repos/ldm-os/apps/kaleidoscope-private/` | **Kaleidoscope product. All three platforms.** `web/` (Next.js), `ios/` (Swift), `macos/` (Swift). Login, pairing, approval, device management, agent view. The product. | Web: VPS (kaleidoscope.wip.computer). iOS: App Store. macOS: direct download. |
| `repos/ldm-os/wip-ldm-os-private/` | **LDM OS kernel.** CLI (`ldm pair`), backend API (WebAuthn, pairing, wallet, WebSocket), Bridge, hooks, installer. Demo prototype at `src/hosted-mcp/demo/`. | npm (CLI). VPS (API endpoints). |
| `repos/wip-web/wip-web-private/` | **Company website.** wip.computer homepage, /lume, /lume/connect. Marketing site. NOT the product. | VPS via GitHub Actions. |

### Where plans and bugs live

All in `repos/ldm-os/wip-ldm-os-private/ai/product/`:

```
ai/product/
  plans-prds/
    kaleidoscope/     Kaleidoscope product plans (this folder)
    bridge/           Bridge plans (pairing, push, relay)
    current/          Active work
  bugs/
    bridge/           Bridge bugs
    kaleidoscope/     Kaleidoscope bugs (create when needed)
    guard/            Guard bugs
    release-pipeline/ Pipeline bugs
```

One place for Parker to look. Code goes where the code belongs. Plans go where Parker looks.

## The split: kernel vs app

**LDM OS (kernel)** provides:
- `ldm pair` CLI command (shows code, waits for token)
- `/api/pair/request` and `/api/pair/approve` endpoints
- `/api/approve-intent` endpoint (agent-to-agent approval)
- WebSocket server for push notifications
- Bridge file inbox (`~/.ldm/messages/`)
- Session registry (`~/.ldm/sessions/`)
- Memory Crystal (search, remember, sync)
- `ldm install` (deploys everything)

**Kaleidoscope (app)** provides:
- `kaleidoscope.wip.computer/pair` ... pairing page (passkey auth, enter code)
- `kaleidoscope.wip.computer/` ... main app (agent view, approval flow, device management)
- iOS app ... mobile approval via Face ID, push notifications
- macOS app ... desktop agent management (future)

The kernel doesn't render web pages. The app doesn't manage the filesystem. They communicate via APIs.

## Kaleidoscope product: kaleidoscope-private

Kaleidoscope is a product with three platforms. All three live in one repo.

```
repos/ldm-os/apps/kaleidoscope-private/
  web/                 Next.js + Tailwind. kaleidoscope.wip.computer.
    src/app/
      page.tsx         main app
      login/page.tsx   login (passkey signup + signin)
      pair/page.tsx    device pairing
      approve/page.tsx agent-to-agent approval
      legal/           privacy policy, terms of use
    src/components/    shared components (KaleidoscopeIcon, Footer, StatusMessage)
    src/styles/        shared CSS (extracted from demo's design system)
    public/            sprites, assets
  ios/                 Swift, Xcode project (future)
  macos/               Swift, Xcode project (future)
  shared/              shared logic between platforms (future)
```

The web app deploys to VPS at `kaleidoscope.wip.computer`. Its own Next.js project, its own deploy pipeline, its own subdomain. NOT inside wip-web-private. Kaleidoscope is the product. wip.computer is the company marketing site.

The demo at `wip.computer/demo/` (in wip-ldm-os-private) is the preserved prototype. The design reference. Not the production app.

## Company website: wip-web-private

```
repos/wip-web/wip-web-private/
  src/app/
    page.tsx           wip.computer homepage (company)
    lume/page.tsx      LUME education page
    lume/connect/      connect/setup page
```

This is the marketing site. It does NOT contain Kaleidoscope. Different repo, different purpose, different deploy.

## API backend: wip-ldm-os-private

The hosted MCP server at `src/hosted-mcp/server.mjs` already handles:
- OAuth 2.0 + PKCE
- WebAuthn passkey registration + verification
- Wallet + Agent Pay
- Image generation proxy

New endpoints for Bridge Phase A-C:
- `POST /api/pair/request` ... CC calls this with a code, long-polls for approval
- `POST /api/pair/approve` ... web page calls this with code + user identity
- `POST /api/approve-intent` ... CC calls this to request agent-to-agent approval
- `WS /ws` ... WebSocket for push notifications to connected bridges

Same server. Same deploy. No new infrastructure.

## How the demo relates

The demo at `wip.computer/demo/` (`src/hosted-mcp/demo/` in wip-ldm-os-private) was the prototype:
- Proved passkey auth works
- Proved agent permission flow works
- Proved wallet + Agent Pay works
- Proved the chat UI works

Ideas from the demo migrate into Kaleidoscope (in wip-web-private) as production features. The demo stays preserved as a reference. It's not deleted, not modified, not evolved. It's the proof-of-concept.

## Cross-references

- `ai/product/plans-prds/bridge/2026-04-06--cc-mini--bridge-master-product-plan.md` ... Bridge product plan (pairing, push, approval, relay)
- `ai/product/product-ideas/vision-quest-01/architecture-spec.md` ... full product architecture
- `ai/product/product-ideas/vision-quest-01/kaleidoscope-executive-brief.md` ... one-page brief
- `ai/product/bugs/release-pipeline/2026-04-06--cc-mini--shared-universal-config-layer.md` ... shared as universal config layer
