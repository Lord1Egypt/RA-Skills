# Proxy and Local Development — Whop

## When the Proxy Matters

Use the Whop development proxy when a local app must run inside a Whop iframe. This is the clean path for preserving local development while still testing the origin-bound auth behavior that Whop expects.

If the task is purely server-to-server REST or webhook handling, skip the proxy.

## Install the Official Proxy

Whop documents the proxy package as `@whop-apps/dev-proxy`.

```bash
pnpm add -D @whop-apps/dev-proxy
npm install --save-dev @whop-apps/dev-proxy
yarn add -D @whop-apps/dev-proxy
bun add -d @whop-apps/dev-proxy
```

The CLI binary is `whop-proxy`.

## Official Example Pattern

The proxy guide shows this exact script shape:

```json
{
  "scripts": {
    "dev": "whop-proxy --command 'next dev --turbopack'"
  }
}
```

This is the preferred path when the proxy should own startup of the upstream app.

## Two Useful Modes

### Command mode

Use `--command` when the proxy should launch the upstream server itself.

Use it when:
- The local app is a normal dev server
- You want one command to boot the proxy and upstream app together
- The team already relies on package scripts such as `npm run dev`

### Standalone mode

The docs describe `--standalone` as running the proxy as an independent process that proxies requests from one port to another and ignores command-related options.

Use it when:
- The upstream server is already running
- You need to attach the proxy to an existing process
- You want the proxy lifecycle separate from the app lifecycle

## Local Workflow Checklist

1. Start the upstream app on a known local port
2. Run `whop-proxy`
3. Load the app through the proxied Whop path, not raw localhost
4. Verify iframe requests reach the app origin through the proxy
5. Confirm auth, access checks, and UI interactions inside the embedded context

## Proxy Debugging Rules

- If `x-whop-user-token` never appears, check origin and proxy pathing before changing app code
- If only raw localhost works, the test is incomplete because it bypasses the real embedded path
- Keep proxy URLs in memory along with the app and company IDs used during testing
- Do not treat custom tunnels as a drop-in replacement for the official proxy unless there is a hard blocker

## What the Proxy Does Not Solve

- Missing app permissions
- Wrong company installation
- Invalid webhook signatures
- Production-only business logic

It only fixes the local embedded-app path. Keep the rest of the debugging tree separate.
