# Bug: `updateToolsAllow is not defined` ReferenceError during `ldm install`

**Date:** 2026-04-11
**Reporter:** Parker + CC Mini (surfaced during inbox-check-hook installer work)
**Component:** `ldm install` (`lib/deploy.mjs`)
**Severity:** Medium (silently fails to register one extension; does not block overall install)
**Related:**
- `ai/product/bugs/installer/2026-04-08--cc-mini--tools-allow-not-updated-on-plugin-install.md` (introduced the `updateToolsAllow` function as the fix)
- `ai/product/bugs/bridge/2026-04-06--cc-mini--bridge-async-inbox-plan.md` (unrelated; surfaced this during the alpha.27/.28 release work)

## Symptom

During `ldm install`, the `wip-file-guard` / `wip-ai-devops-toolbox` install step prints:

```
x updateToolsAllow is not defined
x Failed to update wip-ai-devops-toolbox: Command failed: ldm install /Users/lesa/wipcomputerinc/repos/ldm-os/devops/wip-ai-devops-toolbox-private
```

The install continues (subsequent extensions still process) but `wip-ai-devops-toolbox` does not complete its update. This has been reproduced on at least `@wipcomputer/wip-ldm-os@0.4.73-alpha.27` and `alpha.28`. It is almost certainly present on earlier alphas as well; the error message was simply obscured by the `ok is not defined` crash upstream that we fixed in alpha.28.

## Root cause

**`updateToolsAllow()` is nested inside `resolveOcPluginName()`** in `lib/deploy.mjs`. It is a JavaScript scope mistake introduced during an earlier edit ... the opening brace of `resolveOcPluginName` is left unclosed when the `updateToolsAllow` function definition is written, and then the rest of the `resolveOcPluginName` body continues after the nested function.

Concretely, the current shape is:

```javascript
function resolveOcPluginName(repoPath, toolName) {
  // OpenClaw matches plugins by directory name, not plugin id.
  // Check openclaw.json for existing references to this plugin.
/**
 * Update tools.allow in openclaw.json to include a newly deployed plugin.
 */
function updateToolsAllow(pluginName) {   // <-- nested inside resolveOcPluginName
  const ocConfigPath = join(OC_ROOT, 'openclaw.json');
  if (!existsSync(ocConfigPath)) return;
  // ...
}

  const ocConfigPath = join(OC_ROOT, 'openclaw.json');   // <-- continuation of resolveOcPluginName body
  const ocConfig = readJSON(ocConfigPath);
  if (!ocConfig?.extensions) return toolName;
  // ...
}   // <-- actual close of resolveOcPluginName
```

Because `updateToolsAllow` is defined inside `resolveOcPluginName`, it is only in lexical scope within that function's body. The call site that matters ... the install handler at line 1097 ... lives in a different outer function. From that scope, `updateToolsAllow` is undefined, hence the ReferenceError.

The fact that `resolveOcPluginName` itself still works is what keeps this bug from being immediately obvious: the outer function's plugin-name resolution logic runs fine, and the nested function is simply dead code from the caller's perspective.

## Reproducer

1. Check out `wip-ldm-os-private` at any commit from 2026-04-08 onward (after the April 8 ticket introduced `updateToolsAllow`).
2. Have `wip-ai-devops-toolbox-private` installed locally as an extension.
3. Run `ldm install` (or `ldm@alpha install` with the latest alpha).
4. Observe: `x updateToolsAllow is not defined` in the `wip-ai-devops-toolbox` install step. The extension is not updated. Subsequent extensions still process.

## Proposed fix

Trivial structural refactor. **Move `updateToolsAllow` out of `resolveOcPluginName` and up to module top level**, alongside the other deploy helpers in `lib/deploy.mjs`. The function has no closure dependencies on `resolveOcPluginName`'s locals (it only uses module-level imports like `OC_ROOT`, `join`, `existsSync`, `readFileSync`, `writeFileSync`, and the `log` helper), so the hoist is safe.

### Specific steps

1. In `lib/deploy.mjs`, cut the `/** ... */` jsdoc plus `function updateToolsAllow(pluginName) { ... }` block out of the inside of `resolveOcPluginName`.
2. Paste it at module top level, somewhere near the other helpers (above or below `deployExtension` works).
3. Verify `resolveOcPluginName`'s body still parses cleanly: its opening `{` at line 537, its body (which previously continued after the nested definition), and its closing `}`.
4. `node --check lib/deploy.mjs` to catch any structural errors before running `ldm install`.
5. Run `ldm install` with `wip-ai-devops-toolbox-private` available and confirm the `x updateToolsAllow is not defined` message is replaced with `+ Added "<pluginName>" to openclaw.json tools.allow` (or no message at all, if the plugin name is already present in the allowlist).

## Impact if left unfixed

- `wip-ai-devops-toolbox` fails to install cleanly on every `ldm install` run.
- Any other extension that traverses the same install path (`deployExtension → updateToolsAllow`) loses its `tools.allow` entry, which in OpenClaw 2026.4.8+ means the plugin is silently blocked at runtime.
- The April 8 fix that was meant to resolve the first `tools-allow-not-updated-on-plugin-install` bug is effectively a no-op, so the original symptom from that ticket can reappear under the right conditions: install a new OpenClaw plugin, see it copied to `~/.openclaw/extensions/` and registered in `plugins.entries`, but notice that `tools.allow` still doesn't list it, and the agent can't call its tools.

## Detection

Add a smoke test to `ldm doctor` or the install self-test that confirms:

1. `updateToolsAllow` is defined at module top level of `lib/deploy.mjs` (statically, via import check or a dry-run).
2. For every plugin currently registered in `plugins.entries` in `~/.openclaw/openclaw.json`, its name appears in `tools.allow` (or the plugin is explicitly exempt).

The first check would have caught this at release time. The second check would catch the downstream tools-allow drift that the April 8 ticket already documented as a silent failure mode.

## Discovered how

Noticed during the `ldm install` verification pass for `wip-ldm-os@0.4.73-alpha.27` and `@0.4.73-alpha.28`, when the inbox-check-hook installer wire-up (see PRs #566 and #568) was being validated on a clean install. The `updateToolsAllow is not defined` line appeared in the install output and was traced back to the nested-function scope issue in `lib/deploy.mjs:545` by reading the surrounding code.

## Related work shipped this same day

The two hooks we were originally working on (`syncBootHook` and the new `syncInboxCheckHook`) had the *same class* of bug ... they called a `ok(...)` helper from `bin/ldm.js` that was defined in `lib/deploy.mjs` and never imported into `bin/ldm.js`. Latent in the `syncBootHook` call site since it was written, became reachable when `syncInboxCheckHook` shipped in alpha.27. Fixed in alpha.28 by replacing both calls with `console.log('  + ...')` to match the rest of `bin/ldm.js`. Referencing it here because both bugs share a theme: **helper functions defined in the wrong scope, surfaced only when a new call path exercises the latent error.** Might be worth a pass on other `ok`, `skip`, `fail`, `log`, and `updateToolsAllow`-style helpers to audit for scope misuse across the installer codebase.

## Status

**Filed:** 2026-04-11.
**Fixed:** 2026-04-11 in the same PR that filed this ticket. `updateToolsAllow` is now defined at module top level in `lib/deploy.mjs` (immediately before `resolveOcPluginName`), with a comment block explaining why it must not be nested again. The fix is in the same branch as this ticket and ships as `@wipcomputer/wip-ldm-os@0.4.73-alpha.29`.
