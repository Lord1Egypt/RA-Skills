---
name: clawhub-publish
description: Publish a skill to ClawHub, check visibility and moderation, evaluate monetization options. Use when publishing, verifying, or earning from ClawHub skills.
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(clawhub *)", "Bash(curl *)", "Bash(python *)", "Bash(exec *)"]
---

# Publish Skill to ClawHub

Publish an OpenClaw skill to ClawHub, verify its publication and moderation status, and evaluate monetization options.

## Steps

### 1. Verify ClawHub login

Run `clawhub whoami` to confirm the token is valid and the handle is correct.

Check: output shows the logged-in handle (e.g., `147258xuan`). If not logged in, run `clawhub login` and complete browser auth within 15 minutes per device code.

### 2. Publish the skill

```bash
clawhub skill publish <path> --slug <slug> --name "<name>" --owner <handle> --version <semver> --tags "latest"
```

Required flags: `--slug`, `--name`, `--owner`, `--version`. The skill folder must contain a valid `SKILL.md`.

Check: command exits 0 and prints the published skill ID.

### 3. Verify publication and moderation status

```bash
clawhub inspect <slug>
```

Check: output shows `Moderation: CLEAN` and no "not publicly visible" warning. If moderation shows `pending.publication`, the skill is hidden until checks pass.

### 4. Evaluate monetization options

ClawHub has no built-in skill pricing or payment system. Verify by checking:

- `clawhub skill publish --help` — no `--price` flag exists
- Skill API JSON — no `price`, `payment`, or `earnings` fields
- API routes `/api/v1/earnings`, `/api/v1/wallet` — return "No matching routes found"
- Publishing docs — no mention of pricing or revenue sharing

If you need to charge for a service, use the x402 protocol ecosystem instead:

- **Build a paid API**: use the `monetize-service` skill (Express + x402-express middleware, USDC on Base network, per-request pricing)
- **Discover paid services**: use the `search-for-service` skill (`npx awal@latest x402 bazaar search/list/details`)
- **Make paid requests**: use the `pay-for-service` skill (automatic USDC payment on x402 endpoints)
- **Browse the bazaar**: visit `x402.direct` — the search engine for x402 paid APIs

## Standing preferences

- Skills on ClawHub are free to install (MIT-0 license). Monetization requires a separate paid API endpoint, not a paid skill download.
- The user prefers not to use crypto-based monetization in China due to legal concerns.
- Published skills may take a few minutes for moderation to clear (`pending.publication` → `CLEAN`).
