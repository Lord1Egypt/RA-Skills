# Host evidence and degradation

Load this when reporting on any host other than Claude Code, or when a field
comes back unavailable and you need to explain why.

The rule behind every entry below: **each field uses only evidence that host
actually exposes.** Unsupported fields degrade to "not available". Never
substitute install time or file mtime for a missing trigger count. A report
without the trigger column is still useful; a report with a fabricated one is not.

## What each host can prove

| Check | Claude Code | Codex | OpenClaw | WorkBuddy | Hermes |
|---|---|---|---|---|---|
| Context cost, structure, overlap, security | ✅ | ✅ | ✅ | ✅ | ✅ |
| Description budget (SV001/SV002) | configurable estimate | official 2% / 8k fallback | configurable cap | unavailable | unavailable |
| Loaded vs. on disk | `enabledPlugins` | app-server catalog | eligible runtime catalog | manifest + welcome mode | filesystem only |
| Scope / dependencies | partial | runtime metadata | runtime eligibility metadata | package metadata | unavailable |
| Trigger data (SV201/SV202) | `skillUsage` | unavailable | unavailable | unavailable | unavailable |

When a row reads "unavailable", `doctor` emits **SV901 CAPABILITY_UNAVAILABLE**
rather than a zero. Report that as a gap in evidence, not as a finding about the
skills.

## Claude Code

Plugin state and lifetime per-skill usage come from `~/.claude.json`.

`skillUsage` is **lifetime** data, not a rolling 30-day window. Say so when
quoting it — users routinely read a low number as "unused recently".

Bundled skills shipped inside the CLI may not exist as standalone files, so
actual description budget use can be higher than the filesystem estimate.
State that caveat whenever you report a budget percentage.

## Codex

Use the app-server runtime catalog for enabled state, scope, interface, and
dependencies.

Its 2% / 8,000-character budget is an **official estimate, not measured prompt
usage**. Label it as policy, not measurement.

Codex runtime evidence is *additive*: it can reveal skills the filesystem scan
did not find, and those are merged into the inventory.

## OpenClaw

Use `openclaw skills list --eligible --json` for per-instance eligibility, model
visibility, source, disabled/allowlist state, and missing dependencies. Include
workspace, plugin, shared, and npm-bundled roots.

`openclaw_instances` is the **grouping authority**. Never report a cross-instance
duplicate as a shadowing conflict — conflicts hold only inside one
`conflict_domain`.

OpenClaw runtime evidence is *exclusive*: if the CLI succeeds, only records it
returns as model-visible count as loaded. If the CLI fails or times out, fall
back to filesystem candidates and do **not** call them loaded.

Runtime visibility means the compact metadata is eligible and model-visible. It
does not prove the full `SKILL.md` body was loaded.

## WorkBuddy

Derive active top-level skills from the builtin manifest, the installed cache
version, and the welcome mode. Do not promote plugin internals or connector
catalog entries to top-level skills.

Activity is inferred from manifest/cache/mode evidence, never from invocation
records — WorkBuddy exposes none.

## Hermes

Use configured `external_dirs` and filesystem roots. Mark runtime state and
trigger counts unavailable unless the host exposes stronger evidence.

## Last-resort trigger evidence

For hosts with no native usage source only:

```bash
python3 scripts/probe_logs.py --host openclaw --deep
```

It deduplicates observed `read` calls to `SKILL.md`. Those reads may come from
inspection or debugging rather than automatic activation. Report them as
indirect `observed_skill_reads`. Never copy them into `usage_count`, and never
decide a zombie verdict from them alone.
