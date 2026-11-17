---
name: discussing-builds
description: "Reads and joins the comment threads on a SnapVisor build, test, or media item: summarizes the discussion, replies, reacts, resolves or reopens threads, and follows builds, each change after confirmation. Use when the user asks to 'summarize the comments on build 42', 'show open review threads', 'reply to the open thread and resolve it', 'post a comment on this diff', 'reopen that thread', or 'follow this build'."
---

# SnapVisor build discussion

Summarize who said what on a build and act on the threads for the user. Comments exist on builds, on tests and on media items; each has its own set of operations.

## Connecting and calling the tools

Every operation in this skill comes from the `snapvisor` MCP server, the SnapVisor connector. The server defaults to Code Mode, so the operations below are written as the `external_*` functions you call inside `snapvisor:execute_typescript`. On a server set to the per-tool surface, the same operation is listed as `snapvisor:<name>` without the `external_` prefix, for example `snapvisor:listBuilds`.

- **Only `snapvisor:search_tools` and `snapvisor:execute_typescript` listed (Code Mode, the default):** call `snapvisor:search_tools` first, then call each tool inside `snapvisor:execute_typescript` as `external_<tool>` (for example `external_listBuilds`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **Operations listed by name:** call them directly, for example `snapvisor:listBuilds`.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `snapvisor:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects SnapVisor and approves that scope.
- **No `snapvisor` tools at all:** SnapVisor is not connected yet. Install the SnapVisor power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

The `snapvisor` MCP server has two tools: `snapvisor:search_tools` (call it first, for example with `comment`, to get the exact operation names and inputs) and `snapvisor:execute_typescript` (run a short program calling the declared `external_*` functions; the program must `return` its result).

If the connection lists the operations by name instead (the per-tool surface), call them directly without the `external_` prefix.

Operations this skill uses for builds (tests and media have matching `Test` and `Media` variants, such as `external_listTestComments`):

- `external_listBuildComments`: all comments and threads on a build.
- `external_createBuildComment`: post a comment; set `threadId` to reply, or `screenshotDiffId` to attach it to one screenshot.
- `external_updateBuildComment` and `external_deleteBuildComment`: edit or delete the user's own comment.
- `external_addBuildCommentReaction` and `external_removeBuildCommentReaction`: reactions.
- `external_resolveBuildCommentThread` and `external_unresolveBuildCommentThread`: close or reopen a thread.
- `external_subscribeBuild` and `external_unsubscribeBuild`: follow or unfollow a build.
- `external_getBuild`: the build's status, to open the summary.

## Workflow

1. Identify the build (the `reviewing-visual-builds` skill shows how to find it). Fetch `external_getBuild` and `external_listBuildComments` together in one program with `await Promise.all`.
2. Summarize: build status first, then open threads (author, the point made, the screenshot it is anchored to), then resolved threads in one line each.
3. To post or reply, draft the text, show it, and post it with `external_createBuildComment` after the user agrees. Use `threadId` for replies.
4. To resolve or reopen, name the thread by its first line, confirm, then call the resolve or unresolve operation.
5. Report what changed and the comment or thread id.

## Code Mode pattern

```ts
try {
  const [build, comments] = await Promise.all([
    external_getBuild({ owner, project, buildNumber }),
    external_listBuildComments({ owner, project, buildNumber }),
  ]);
  return { status: build.status, comments };
} catch (e) {
  return { error: String(e) }; // "<CODE>: <details>"
}
```

## Rules

- Post comments in the user's words or in a draft they approved. Never post on their behalf without showing the text first.
- Edit or delete only comments the user wrote, and only after a confirmation.
- Remove a reaction or unfollow a build only after the user confirms; the server marks both operations as destructive.
- Do not approve or reject the build from this skill; that is `reviewing-visual-builds`.
