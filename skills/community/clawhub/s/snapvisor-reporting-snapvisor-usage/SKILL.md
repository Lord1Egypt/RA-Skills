---
name: reporting-snapvisor-usage
description: "Reports SnapVisor account activity and access: builds and screenshots per period, busiest projects, daily, weekly, or monthly trends, members, and pending invites. Use when the user asks 'how many builds did we run this month', 'how many screenshots did we use', 'which projects are busiest', 'show usage trends', 'who is on the team', or 'which invites are pending'. Read-only."
---

# SnapVisor usage report

Turn the account's analytics and membership into a short, factual report.

## Connecting and calling the tools

Every operation in this skill comes from the `snapvisor` MCP server, the SnapVisor connector. The server defaults to Code Mode, so the operations below are written as the `external_*` functions you call inside `snapvisor:execute_typescript`. On a server set to the per-tool surface, the same operation is listed as `snapvisor:<name>` without the `external_` prefix, for example `snapvisor:listBuilds`.

- **Only `snapvisor:search_tools` and `snapvisor:execute_typescript` listed (Code Mode, the default):** call `snapvisor:search_tools` first, then call each tool inside `snapvisor:execute_typescript` as `external_<tool>` (for example `external_listBuilds`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **Operations listed by name:** call them directly, for example `snapvisor:listBuilds`.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `snapvisor:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects SnapVisor and approves that scope.
- **No `snapvisor` tools at all:** SnapVisor is not connected yet. Install the SnapVisor power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

The `snapvisor` MCP server has two tools: `snapvisor:search_tools` (call it first, for example with `analytics`, `member`, `project`) and `snapvisor:execute_typescript` (run a short program calling the declared `external_*` functions; the program must `return` its result).

If the connection lists the operations by name instead (the per-tool surface), call them directly without the `external_` prefix.

Operations this skill uses (confirm with `snapvisor:search_tools`):

- `external_getMe`: the accounts this connection can reach, with their `slug` and whether MCP access is included.
- `external_getAccountAnalytics`: build and screenshot counts for an account, `from` a date (optional `to`), grouped by `day`, `week` or `month`, optionally for named projects.
- `external_listProjects`: the account's projects.
- `external_listAccountMembers` and `external_listAccountInvites`: members with their level, and pending invites. These need the `account:admin` scope.

## Workflow

1. Call `external_getMe` to get the account slug. If the connection reaches several accounts, ask which one.
2. Agree the window (default: the current calendar month, grouped by `week`).
3. In one program, fetch `external_getAccountAnalytics` and `external_listProjects` with `await Promise.all`. Add the member and invite lists if the user asked about the team.
4. Report totals for the window, the trend per period in a small table, and the per-project split when available. For the team, list members by level and pending invites with their dates.

## Code Mode pattern

```ts
const me = await external_getMe({});
const accountSlug = me.accounts[0].slug;
const [analytics, projects] = await Promise.all([
  external_getAccountAnalytics({ accountSlug, from: "2026-09-01", groupBy: "week" }),
  external_listProjects({ accountSlug }),
]);
return { analytics, projects };
```

If a call throws `SCOPE_MISSING` or a 403, the connection lacks that scope (member lists need `account:admin`). Say which scope is missing and that the user can reconnect with it.

## Rules

- Report only numbers the operations returned. Do not estimate costs or compare against other teams.
- This skill only reads. Never call `external_updateAccount`, `external_setAccountMemberLevel`, `external_removeAccountMember`, `external_createAccountInvites`, or `external_cancelAccountInvite` from it. Do not invite, remove, or change members from here; those changes belong in the SnapVisor app or in an explicit request the user confirms.
