# Ticket 21: Link login footer brand line to WIP Computer home

**Date:** 2026-05-21
**Filed by:** Codex, with Parker
**Status:** archived, implemented. Hosted-mcp PR #1058 linked the login footer brand line.
**Master:** `ai/product/plans-prds/comms/website/tickets/website-launch-masterticket.md`
**Related:** Ticket 20 footer brand home link
**Surface:** hosted Kaleidoscope login footer only

## Problem

Archived 2026-05-21: `/login` footer brand link implementation landed in hosted-mcp PR #1058.

Ticket 20 linked the footer brand line on the homepage, live wall, and legal pages. The `/login` footer was intentionally out of scope, so it still shows an unlinked `WIP Computer, Inc.` brand line.

Parker now wants the same footer-brand link behavior on login.

## Scope

Make only the login footer brand link change.

Target URL:

```text
https://wip.computer/
```

Pages in scope:

- `https://wip.computer/login`
- any hosted login HTML file that renders that same footer instance

Expected source surface:

```text
repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/kaleidoscope-login.html
```

If the current `/login` route is served from a different hosted-mcp HTML file, update that exact footer instance instead and report it in the PR.

## Requirements

- Link only `WIP Computer, Inc.`.
- Keep `Learning Dreaming Machines` as plain text.
- Keep `Made in California.` as plain text.
- Link target must be `https://wip.computer/`.
- Preserve the existing footer visual layout.
- Preserve existing login behavior and all auth flows.
- Preserve existing footer taxonomy and all other footer links.

## Explicitly Out Of Scope

- Do not change WebAuthn.
- Do not change QR login.
- Do not change Local passkeys behavior.
- Do not change passkey creation or passkey sign-in.
- Do not change `next` routing.
- Do not change Remote Control, pair/relink, relay, daemon, E2EE, wallet, image generation, demo chat, server behavior, nginx, API keys, or legal body copy.
- Do not redesign the footer.
- Do not start the shared footer/template refactor in this ticket.
- Do not deploy.

## Acceptance Criteria

- On `/login`, `WIP Computer, Inc.` links to `https://wip.computer/`.
- `Learning Dreaming Machines` remains unlinked text.
- `Made in California.` remains unlinked text.
- Footer visual layout is unchanged except for link behavior.
- Login, create-account, sign-in, QR, Local passkeys, and `next=/demo` behavior are unchanged.

## Validation

Minimum expected checks:

- `git diff --check`
- inline script parse if the edited login file contains inline JavaScript
- parser check that the `/login` footer brand text is wrapped in a link to `https://wip.computer/`
- parser check that `Learning Dreaming Machines` and `Made in California.` remain plain text
- grep or changed-file check showing no server, wallet, WebAuthn, QR, relay, nginx, demo chat, legal body, footer JS, app JS, CSS, or API-key files changed

## Review Notes For Coder

Use a fresh worktree.

Stop at PR. Do not deploy.

Report:

- exact file changed
- confirmation that only `WIP Computer, Inc.` became linked
- confirmation that login/auth behavior files and server behavior were not changed
