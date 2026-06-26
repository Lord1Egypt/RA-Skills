# wip-release v1.9.75

## Fix: publishNpm now captures stderr so the "already published" swallow check works

`publishNpm` and `publishNpmWithTag` used `execFileSync(..., stdio: 'inherit')`. That sends npm's stderr straight to the parent tty but leaves the thrown error's `.message` as just `Command failed: npm publish ...`. None of the npm-specific text (including "cannot publish over the previously published versions") ever lands in `e.message`.

Phase 5 of `release()` (and the alpha/beta sub-tool loop) substring-matches `e.message` against `previously published` and `cannot publish over` to silently swallow idempotent re-publish errors. Because `.message` never contained those strings, **every** repeat publish was logged as a real failure, and re-running `wip-release alpha` on a repo whose sub-tools were already on npm looked like 10 failures even though nothing was wrong.

More concerningly, real first-time publish failures were indistinguishable from benign re-publishes in the error text, which is part of why during today's PR 2 alpha run `wip-branch-guard@1.9.77` silently failed to publish (the real error was lost in the noise).

## Change

New helper `runNpmPublish(args, cwd)` uses `spawnSync` with `stdio: ['inherit', 'inherit', 'pipe']`:

- stdout still inherits -> tarball listing streams to tty as before.
- stderr is captured AND echoed to process.stderr -> user still sees errors, callers get the text.
- On non-zero exit, throws `new Error(msg)` where `msg = "Command failed: npm ${safe_args}\n${stderr.trim()}"`. Also attaches `err.stderr` and `err.status` for structured consumers. Auth token is redacted from the reproduced command.

`publishNpm` and `publishNpmWithTag` thin-wrap `runNpmPublish` with their respective args. Behavior identical on success; on failure, callers can now match on `.message` or `.stderr` as they always intended to.

## Test

Direct probe after change:

```
$ node -e "import('../wip-release/core.mjs').then(m => { try { m.publishNpm(process.cwd()) } catch (e) { console.log(/cannot publish over/.test(e.message) ? 'SWALLOW_OK' : 'MISSED: ' + e.message.slice(0, 100)) } })"
npm error You cannot publish over the previously published versions: 1.9.79.
SWALLOW_OK
```

Before this change the last line was `MISSED: Command failed: npm publish...`.

## Files

- `tools/wip-release/core.mjs`: +26 lines (spawnSync import, runNpmPublish helper, publishNpm / publishNpmWithTag wrappers).
- `tools/wip-release/package.json`: 1.9.74 -> 1.9.75.

## Related

Surfaced during the wip-branch-guard 1.9.77 -> 1.9.79 cascade on 2026-04-20. Manual `publishNpm` calls worked; `wip-release alpha`'s Phase 5 sub-tool loop silently ate the publish error for 1.9.77 and none of us noticed until `ldm install` couldn't find it on npm.
