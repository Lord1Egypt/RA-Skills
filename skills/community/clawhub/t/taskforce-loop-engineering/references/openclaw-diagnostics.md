# OpenClaw Multi-IM Diagnostics

## Compatibility and scope

This procedure requires package version 0.16.2 or newer; 0.16.1 does not
include these capabilities. Until a compatible release is installed, use a reviewed
source candidate for validation and report installed diagnostics as unchanged. Do not
pass new flags to an old binary or claim that updating the skill upgrades code.
This procedure applies to OpenClaw; it does not change Hermes diagnostics.

1. Identify the installed package, managed workspace, worker and queue. Check
   `loop-engineering-openclaw-doctor --help` and
   `loop-engineering-openclaw-smoke --help` for all three source flags below.
   Help alone is not acceptance: verify discovery and dry-run report results.
2. Select the intended OpenClaw CLI/profile environment. `--root` selects a
   workspace, not an OpenClaw profile. Both commands accept `--openclaw-bin`
   for the selected executable; retain that profile's normal environment.
   Inspect `openclaw channels list --json` using that same CLI/environment.
   Doctor resolves executable aliases and requires the same executable as the
   install manifest, plus unchanged manifest hashes for notifier/dispatcher.
   A missing/incomplete manifest, different CLI, or caller drift fails
   `diagnostic_runtime`: no notification probe or smoke worker runs. Choose
   the installed CLI or repair the integration within the authorized scope;
   `--openclaw-bin` does not rewrite installed callers.
   Never print channel credentials to diagnose selection.
3. Run doctor. Without source filters, it discovers channel/account pairs from
   the inventory and dry-runs each through the installed notifier. Inspect
   `notificationSources` and the per-account `notification_dry_run` checks.
   A configured inventory is not proof of a connected channel.
4. Run smoke only within the authorized worker-execution scope. It first
   requires doctor to pass, then uses the first returned source for the isolated
   task's routing and terminal notification dry-run. It executes a real worker,
   so it is not merely a read-only notification probe and may consume model
   resources. It removes its temporary queue/config/runtime unless
   `--keep-artifacts` is requested; verify cleanup and required task artifacts.
5. For acceptance across multiple IMs/accounts, repeat smoke with explicit
   channel/account pairs. One default smoke does not cover every configured
   route. Report tested pairs, failures, retained evidence and cleanup status.

## Explicit selection

Both doctor and smoke accept:

- `--source-channel`: filter to an actual configured IM channel.
- `--source-account`: filter to an actual account ID. Pair with a channel to
  avoid matching the same account name across different IMs.
- `--source-target`: override the synthetic dry-run destination when a plugin
  requires a particular target format. This does not enable real sending or
  change channel/account discovery.

For a configured Telegram account named `personal` (replace all placeholders
and select its actual profile environment first):

```bash
loop-engineering-openclaw-doctor --root /path/to/workspace --queue agent-tasks --worker-agent main --source-channel telegram --source-account personal --source-target 1 --json
loop-engineering-openclaw-smoke --root /path/to/workspace --queue agent-tasks --worker-agent main --source-channel telegram --source-account personal --source-target 1 --json
```

Targets are synthetic by default. Discovery failure, malformed/empty channel
inventory or unmatched filters must fail closed; never fall back to Feishu or
silently drop the account. Within the selected channels, malformed account
lists or non-string/blank account entries fail even alongside valid entries
and even when an account filter would exclude them. An explicit channel filter
excludes unrelated channels from validation. Empty account arrays are valid,
but fail selection if no matching accounts remain. Correct the profile or selection instead of editing
a temporary test script to hardcode another IM.

## Evidence boundaries

Notification probes remain dry-run even with an explicit target. Passing them
proves only the tested routing/argument path, not real outbound delivery,
inbound reception, or trusted approval callback transport. Real end-to-end
messaging requires separate authorization and observed delivery/receipt.
Do not infer universal IM support from Feishu, Telegram and Slack mock tests;
other configured plugins need their own acceptance evidence. Keep diagnostic
coverage distinct from production notification and human-gate support.

### Diagnostic invocation and environment isolation

After checking executable identity and managed caller hashes, doctor uses the
exact CLI invocation recorded by installation for version, agent, channel and
notification checks. PATH/symlink aliases remain accepted when they resolve to
the same executable, but their invocation names are not used to select a second
profile. To change the installed profile, explicitly repair the integration.
Equal realpaths alone do not establish profile equivalence for name-sensitive
wrappers.

Doctor notification probes and smoke subprocesses discard inherited
`LOOP_HUMAN_INPUT_SOURCE` and `LOOP_NOTIFICATION_SOURCE` before supplying their
own discovered/task source. Production human-gate source precedence is unchanged.
Regression checks compare reported channel/account/target against captured
message arguments (including `--dry-run`), with conflicting inherited sources,
multiple accounts, and invocation-name-sensitive wrappers.
