---
name: reviewing-visual-builds
description: "Reviews a SnapVisor visual regression build: shows what changed in the screenshot diffs for a branch or commit and approves or rejects the build after the user confirms. Use when the user asks 'what changed in the latest build', 'show the screenshot diffs', 'review the visual changes on this branch', 'approve build 42, the nav restyle is intentional', 'reject this build', or asks about visual testing or UI regression results."
---

# Review a SnapVisor build

Walk the user through the visual changes SnapVisor detected in a build, then approve or reject it on their say-so. An approval is a real decision for the whole team: the build is accepted and its changed screenshots become the new baseline.

## Connecting and calling the tools

Every operation in this skill comes from the `snapvisor` MCP server, the SnapVisor connector. The server defaults to Code Mode, so the operations below are written as the `external_*` functions you call inside `snapvisor:execute_typescript`. On a server set to the per-tool surface, the same operation is listed as `snapvisor:<name>` without the `external_` prefix, for example `snapvisor:listBuilds`.

- **Only `snapvisor:search_tools` and `snapvisor:execute_typescript` listed (Code Mode, the default):** call `snapvisor:search_tools` first, then call each tool inside `snapvisor:execute_typescript` as `external_<tool>` (for example `external_listBuilds`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **Operations listed by name:** call them directly, for example `snapvisor:listBuilds`.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `snapvisor:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects SnapVisor and approves that scope.
- **No `snapvisor` tools at all:** SnapVisor is not connected yet. Install the SnapVisor power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

The `snapvisor` MCP server has two tools. Everything below goes through them.

- `snapvisor:search_tools`: find the operations you need and their exact input shape. Call it before your first `snapvisor:execute_typescript`, for example with the queries `build`, `diff`, `review`.
- `snapvisor:execute_typescript`: run a short program that calls the `external_*` functions `snapvisor:search_tools` declared. They are already in scope; never import or redeclare them. The program must `return` its result.

If the connection lists the operations by name instead (the per-tool surface), call them directly without the `external_` prefix.

Operations this skill uses (confirm names and inputs with `snapvisor:search_tools`):

- `external_getMe`: the signed-in user and the accounts (with `slug`) this connection can reach.
- `external_listProjects`: projects in an account.
- `external_listBuilds`: builds of a project, newest first; filter by branch (`head`), commit (`headSha`) or `search`.
- `external_getBuild`: one build with status, conclusion, stats, branch and commit.
- `external_listBuildDiffs`: one entry per screenshot with `name`, `status` (`added`, `changed`, `removed`, `failure`, `ignored` and more), and base and head image links. Pass `needsReview` to see only what needs a decision.
- `external_listReviews`: reviews already filed on the build.
- `external_createReview`: file a review with `event` `APPROVE` or `REJECT` and an optional `body`.

## Workflow

1. If you do not know the account and project, run one program: `external_getMe({})`, then `external_listProjects` for the account the user means. Ask once if more than one project fits.
2. Find the build. With no build number given, take the newest from `external_listBuilds` (or the newest on the branch the user named).
3. In one `snapvisor:execute_typescript` call, fetch `external_getBuild`, `external_listBuildDiffs` and `external_listReviews` together with `await Promise.all([...])` and return a compact summary.
4. Present the build number, branch, commit and status, then the changed screenshots grouped by status (changed, added, removed, failed). Give each its before and after links. Mention reviews already on the build.
5. If the user wants a decision, restate it ("Approve build 42 in project web; 6 changed screenshots become the baseline") and wait for a clear yes.
6. Call `external_createReview` with `event: "APPROVE"` or `event: "REJECT"` and the user's reason as `body`. Report the new review, and confirm the build's status with `external_getBuild`.

## Code Mode pattern

```ts
const [build, diffs, reviews] = await Promise.all([
  external_getBuild({ owner, project, buildNumber }),
  external_listBuildDiffs({ owner, project, buildNumber, needsReview: "true" }),
  external_listReviews({ owner, project, buildNumber }),
]);
return { build, diffs: diffs.results.map((d) => ({ name: d.name, status: d.status })), reviews };
```

Wrap a call in `try { ... } catch (e) { return String(e) }` when it may fail. Errors read `<CODE>: <details>`; relay the code and details instead of guessing.

## Rules

- Never file a review without the user's explicit confirmation in this conversation, and never approve or reject several builds in a loop. One build, one confirmation.
- Always show the diffs before asking for a decision.
- Image links are signed and expire after about an hour. Hand them over; do not store or archive them.
- A 403 saying MCP access requires a paid plan means the account is on the Free plan. Say so plainly and do not retry.
- SnapVisor compares screenshots the user's CI uploaded. Do not offer to capture, upload or edit a screenshot; no operation on this surface can.
