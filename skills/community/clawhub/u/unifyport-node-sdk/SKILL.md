---
name: unifyport-node-sdk
description: Use when maintaining or using the UnifyPort Node.js SDK; covers the Device API client, public contract, generated code, errors, retries, and the new API workflow.
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    primaryEnv: UNIFYPORT_DEVICE_API_KEY
    envVars:
      - name: UNIFYPORT_DEVICE_API_BASE_URL
        required: false
        description: Required only when executing a live UnifyPort Device API request.
      - name: UNIFYPORT_DEVICE_API_KEY
        required: false
        description: Required only when executing an authenticated live Device API request.
    homepage: "https://www.npmjs.com/package/@unifyport/sdk-node"
---

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

# UnifyPort Node.js SDK

## When to use this skill

Use this skill when a task involves any of the following:

- calling the UnifyPort Device API from Node.js or TypeScript;
- adding, updating, or troubleshooting an `@unifyport/sdk-node` operation;
- updating the public contract, fixing generation drift, or reviewing public types;
- changing authentication, timeout, retry, pagination, errors, or JavaScript integer boundaries.

This is a development and integration skill. Installing it does not expose Device API operations as
OpenClaw tools, install an MCP server, or provide credentials.

Choose one mode before taking action:

- **Project usage**: install or use the public `@unifyport/sdk-node` package in an application.
- **Repository maintenance**: modify the SDK repository, its public contract, generated code, or tests.

When working inside the SDK repository on MCP-only behavior, also use its repository-local
`unifyport-mcp` skill. That MCP skill is not part of the ClawHub publication boundary.

## Preparation for every task

1. Confirm whether the task is project usage or repository maintenance.
2. Inspect the current project and package manager before installing or changing dependencies.
3. Confirm the actual package exports and operation names from installed types or public documentation.
4. Do not request, print, or persist a real API key. Live requests require credentials supplied through
   the runtime environment by the user or deployment system.

## Project usage workflow

1. Confirm Node.js `>=22.12.0`.
2. Install the SDK with the package manager already used by the target project. For npm:

   ```bash
   npm install @unifyport/sdk-node
   ```

3. Import `UnifyPortDeviceClient` and public types from the package root.
4. Read the base URL and API key from the runtime environment. Do not place them in source, generated
   files, logs, tool inputs, or committed configuration.
5. Use typed operation methods instead of manually assembling paths, query strings, or authentication
   headers.
6. Run the target project's existing tests and type checker after integration.

Minimal configuration:

```ts
import { UnifyPortDeviceClient } from "@unifyport/sdk-node";

function requiredEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

const device = new UnifyPortDeviceClient({
  baseUrl: requiredEnv("UNIFYPORT_DEVICE_API_BASE_URL"),
  apiKey: requiredEnv("UNIFYPORT_DEVICE_API_KEY")
});
```

Do not execute a live request merely to validate installation. Prefer type checking and mocked transport
tests unless the user explicitly requests a live call and supplies an approved test environment.

## Repository maintenance preparation

Apply this section only when the workspace contains the SDK repository markers `AGENTS.md`,
`contracts/device.openapi.yaml`, and the root `package.json` for `unifyport-sdk-node-workspace`.

1. Read the repository-root `AGENTS.md`.
2. Read `docs/architecture.md` and `docs/security.md`. For API changes, also read `docs/contract-maintenance.md`.
3. Use `rg` to confirm the actual operationId, client exports, and existing tests. Do not guess API names.
4. Inspect the worktree and preserve changes made by the user or other agents.
5. Confirm that protocol changes are backed by an approved public API schema and release notes.

## Public contract and scope

Code generation accepts only one in-repository contract:

- Device API: `contracts/device.openapi.yaml`.

Update the contract only from approved public API schemas and release notes. Do not infer fields, status codes, authentication, or security rules that public material does not define.

The `/v1/accounts/...` paths in the contract represent provider account resources within the Device API. Account management, authorization, and runtime operations remain in SDK scope and must not be confused with a separate authentication service.

## Choose the client

- Use `UnifyPortDeviceClient` for the Device API. Its configuration type is `DeviceClientConfig`, and it authenticates with `X-Api-Key`.

Do not pass an API key or base URL as a normal operation parameter. Passwords, codes, or session payloads required for provider account authorization may be passed only through the corresponding typed operations and must be treated as sensitive input.

## Shared usage rules

### Using an existing operation

1. Import the client and types from the package root.
2. Use typed operation methods instead of manually assembling paths or headers.
3. Catch the SDK's public error type and record only the status, server code, and request ID. Do not log the complete request, response, or configuration.
4. Prefer the provided pagination helper for cursor traversal. Otherwise, set an explicit limit and handle repeated cursors.
5. Do not convert a `uint64`-style ID to `number` unless the contract explicitly guarantees a safe range.

### Adding or changing an API in the SDK repository

1. Review the approved public API schema and release notes.
2. Update `contracts/device.openapi.yaml`.
3. Run `pnpm contracts:lint`.
4. Explicitly classify authentication, side effects, retry behavior, secrets, destructive behavior, and MCP policy for the operation.
5. Run `pnpm generate` and review the generated diff. Do not edit generated files directly.
6. Add boundary tests, then run `pnpm generate:check` and `pnpm check`.
7. Run `pnpm public:check` to verify public content and release boundaries.

## Security decisions

- Automatic retries use an explicit allowlist. Ordinary writes, verification-code/password/session submissions, and one-time-secret operations are not retried by default.
- The client injects authentication headers; operation-level headers must not override them.
- HTTPS is the default. Loopback HTTP is allowed only when the caller explicitly opts in.
- Return API key create or rotate secrets only to the direct SDK caller. Do not cache, log, or send them to MCP.
- A webhook signature protocol must be fully defined by an approved public API schema and release notes; do not infer it.
- Error parsing must handle empty bodies, non-JSON bodies, and non-standard envelopes while preserving the HTTP status. A raw cause may contain a sensitive URL or request value and must not be exposed directly.

## Change standards

- Keep the diff minimal and avoid unrelated refactors.
- Use brief Chinese code comments to explain why, compatibility boundaries, or risks, and update comments when behavior changes.
- Generate operation paths and types; do not maintain a duplicate handwritten type set.
- A new convenience API must not hide important wire semantics such as `204` or a one-time secret.
- For public API changes, evaluate the semver impact and verify ESM exports and declaration files.
- When public user documentation changes, update the complete Simplified Chinese counterpart in the same change.

## Verification and delivery

Full verification:

```bash
pnpm clawhub:check
pnpm check
pnpm public:check
```

Run individual checks as needed:

```bash
pnpm contracts:lint
pnpm generate:check
pnpm lint
pnpm format:check
pnpm test
pnpm typecheck
pnpm build
pnpm package:check
```

Lead the delivery note with the outcome, then list the approved public API schema or release notes used, changed files, authentication/retry/MCP classification changes, commands actually run, and uncovered risks. Do not claim that an unexecuted command passed.
