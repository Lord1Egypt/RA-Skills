# Tool contracts

All tools are local and deterministic. Unless a section says otherwise they are
read-only; `run_checks`, `verify_change` and `run_adapter` require
`allow_execute=true` for their explicit execution paths, and `scaffold_skill` /
`workflow_state` require `apply=true` before writing.

## repo_map

Input:

- `path` (required): repository or source directory.
- `max_files` (optional, default 2000): source file limit.

Output: `root`, `modules`, `imports`, `entrypoints`, `truncated`.

Python imports include absolute, `from .X import Y`, `from . import X`,
`as` aliases, packages and multi-name forms. Temporary / agent-state
directories (`.workflow`, `.codex`, `.cursor`, `.claude`, `.agents`,
`scratch`, `_probe`, `probe`, `sandbox`, `debug`, `.tmp`) and probe/temp
file names are ignored by default.

## system_model

Input:

- `path` (required): repository or source directory.
- `max_files` (optional, default 2000): source file limit.
- `contract_file` (optional): contract path relative to the repository root
  (default `.yotta/architecture.json`).

Output: `status` (`PASS` / `FAIL` / `UNKNOWN`), `contract`, `model` (`modules`,
`layers`, `imports`, `entrypoints`, `tests`, `configs`, `data_stores`),
`unknowns`, `unknowns_truncated`, `unverified_claims`, `evidence`, `truncated`
and `model_digest`.

Contract schema, glob rules, finding codes and import kinds are documented in
`references/architecture-contract.md`.

## architecture_review

Input:

- `path` (required): repository or source directory.
- `max_files` (optional, default 2000): source file limit.
- `contract_file` (optional): contract path relative to the repository root
  (default `.yotta/architecture.json`).

Output: `status` (`PASS` / `FAIL` / `UNKNOWN`), `contract`, `checked`
(`rules` / `boundaries` / `data_stores` / `invariants`, each with a per-item
`status` of `PASS` / `WARN` / `FAIL` / `UNKNOWN`), `violations`, `blocking_findings`,
`advisory_findings`, `unknowns`, `unverified_claims`, `evidence`, `truncated` and
`model_digest`.

`critical` / `high` findings fail the review; `medium` / `low` stay advisory.
Anything the model cannot decide becomes `UNKNOWN`; declared invariants that this
tool cannot evaluate are listed in `unverified_claims` instead of being reported
as passing. Read-only.

## impact_analysis

Input:

- `path` (required): repository or source directory.
- `changed_files` (optional): repository-relative changed files.
- `diff` (optional): unified diff text; changed files and line numbers are parsed
  from it, deleted files keep their declared layer.
- `symbols` (optional): target symbols; their definition sites become the change.
- `depth` (optional, default 3, 1-10): reverse-dependency depth.
- `max_files` (optional, default 2000): source file limit.
- `contract_file` (optional): contract path relative to the repository root.

At least one of `changed_files`, `diff` or `symbols` is required.

Output: `status`, `inputs`, `changed`, `direct_consumers`, `cone` (`nodes` with
`depth` / `via` / `layer` / `is_test`, `max_depth`, `limit`, `truncated`),
`affected_layers`, `affected_boundaries`, `affected_data_stores`,
`affected_invariants`, `relevant_tests`, `architecture` (`status`,
`violations_total`, `violations_in_scope`, `unknowns`), `blast_radius`
(`level`, `score`, `capped`, `reasons`), `rollback_probes`, `unknowns`,
`unverified_claims`, `evidence`, `truncated` and `model_digest`.

`status` is `FAIL` when a blocking architecture violation sits inside the cone,
`UNKNOWN` while anything is undecided, otherwise `PASS`. Read-only; no command is
executed.

## verify_change

Input:

- `path` (required): repository or source directory.
- `changed_files` / `diff` / `symbols` (at least one): the same change inputs as
  `impact_analysis`.
- `depth` (optional, default 3, 1-10): reverse-dependency depth.
- `levels` (optional): additional execution levels `L2`, `L3`, `L4` or manual `L5`.
  L0 and L1 always run.
- `allow_execute` (optional, default false): required before any L2-L4 check runs.
- `timeout` (optional, default 120, 1-600): upper bound for each policy check.
- `max_files` / `contract_file` (optional): model limit and contract override.
- `policy_file` (optional, default `.yotta/verification.json`): policy override.

Output: `status`, `inputs`, `required_levels`, `ledger`, `unverified_claims`,
`policy`, `evidence`, `ledger_digest`, `model_digest` and `impact_status`.

Every ledger entry has `id`, `level`, `claim`, `status` (`PASS` / `FAIL` / `UNKNOWN` /
`UNVERIFIED`), `severity`, `check`, `confidence`, `evidence`, `next_step` and
`command`. Static checks keep `command` as `null`; executed checks record the
whitelisted kind, relative cwd, exit code, timeout flag and `output_hash`.

The default ladder runs L0 (changed-file syntax, contract schema) and L1 (architecture
rules and boundaries inside the change cone). L2-L4 are skipped unless both a policy
check is declared and `allow_execute=true`; they never accept arbitrary commands.
L5 is always manual and stays in `unverified_claims`. The ledger intentionally has no
wall-clock timestamp: its digest and the command output hashes are the reproducible
evidence anchors.

## self_test

Input:

- `path` (required): source checkout or installed skill directory.
- `mode` (optional, default `auto`): `auto`, `source` or `installed`.
- `allow_execute` (optional, default false): run the target test suite.
- `timeout` (optional, default 120, 1-600).

Source mode checks required files, version alignment across `package.json` /
`SKILL.md` / `CHANGELOG.md` / `server.json` / engine `VERSION`, the SKILL.md
current-version body, protocol tool names and
`inputSchema.additionalProperties=false`, fail-closed defaults for every write or
execute gate, and counterexamples. Installed mode runs three checks: files,
skill-version and verifier-counterexamples; source-only checks are out of scope.

The counterexample suite is in-process and deterministic: a seeded forbidden
dependency must be `FAIL`, removing the rule must stop the failure, an invalid
contract must be `FAIL` or `UNKNOWN`, a missing contract must be `UNKNOWN`, a seeded
credential must be found, and a seeded version mismatch must fail readiness. These
probes prove the verifier is not a rubber stamp.

## run_adapter

Input:

- `action` (required): `list` probes optional adapters without executing them;
  `run` executes exactly one adapter.
- `path` (required): repository root.
- `adapter` (required when `action=run`): `import-linter`,
  `dependency-cruiser` or `repomix`.
- `allow_execute` (optional, default false): required for `action=run`.
- `timeout` (optional, default 120, 1-600).
- `max_chars` (optional, default 120000, 1000-1000000): Repomix output cap.
- `token_budget` (optional): Repomix token budget; over-budget output fails.
- `target` (optional, default `.`): repository-relative adapter target.

`action=list` returns `status`, `adapters` with `available` / `ready` /
`executable` / `executable_source` / `config` / `reason`, plus `unknowns`.

`action=run` returns `status` (`PASS` / `FAIL` / `UNKNOWN`), the selected
`adapter` metadata, a fixed `command` record with `output_hash`, normalized
`findings`, Repomix `content` metadata when applicable, `next_step` and
`unknowns`. Missing tools, missing configs, invalid output and timeouts are
`UNKNOWN`, never silent passes.

Adapters are optional enhancements: no package is installed or downloaded, no
arbitrary argv is accepted, and adapter findings do not silently change the
status of the core architecture tools. See `references/adapters.md`.

## find_code

Input:

- `path` (required): repository, directory or file.
- `query` (required): symbol or text.
- `extensions` (optional): file extensions such as `.py`.
- `max_results` (optional, default 100).
- `context_lines` (optional, 0-5).

Output: `query`, `matches` (`path`, `line`, `kind`, `text`, `context`), `truncated`.

## compress_output

Input:

- `text` or `file` (one required).
- `max_chars` (optional, default 4000).
- `head_lines` / `tail_lines` (optional).

Output: text plus `original_lines`, `kept_lines`, `error_lines`, `truncated`.

## review_code

Input:

- `path` or `text` (one required).
- `max_findings` (optional, default 200).

Rules: bare-except, eval-exec, shell-true, debug-print, todo-comment,
mutable-default.

Each finding contains `path`, `line`, `rule`, `severity`, `evidence`, `suggestion`.

## review_diff

Input:

- `diff_text` or `path` (one required).
- `base` (optional git revision when `path` is used). It is resolved to a commit SHA
  before `git diff` runs; option-like, whitespace-containing, oversized or
  unresolvable revisions are rejected.
- `max_findings` (optional).

Only added lines are reviewed. Output: `files`, `findings`, `truncated`.

`review_code` uses the same default ignore set as `repo_map`: agent state
directories, scratch / probe / sandbox / debug directories and probe/temp
file names do not flood the result. `review_diff` only reviews added lines,
so it is unaffected by directory traversal.

Optional `.review-allowlist.json` (or `.yotta/review-allowlist.json`) suppresses
known-intentional findings by exact path + rule + line. No wildcards are
supported; `reason` is required. The root-level file is copied by the installer,
so installed copies keep the same exemptions.

```json
{
  "version": 1,
  "entries": [
    {"path": "scripts/example.py", "rule": "debug-print", "line": 12, "reason": "CLI help output"}
  ]
}
```

Output adds `suppressed`, `suppressed_findings` and `allowlist_errors`.
An invalid allowlist fails closed: findings are not suppressed.

## mcp_doctor

Input:

- `skills_dirs` (optional array).
- `config_paths` (optional array).
- `include_defaults` (optional boolean): when `config_paths` is supplied, also
  scan the built-in host registry instead of explicit-only scope.

Output: `skills`, `mcp_configs`, `coverage`, `skills_coverage`, `issues`,
`coverage_gaps`, `unknown_hosts`, `summary`, `scope`, `checked_skills`,
`checked_configs`, `checked_hosts`.

Discovery is tiered and environment-aware: verified hosts include Codex
(`$CODEX_HOME/config.toml`, JSON fallbacks), Cursor, WorkBuddy
(`~/.workbuddy/mcp.json` plus `connectors/*/mcp.json`), OpenCode
(`$XDG_CONFIG_HOME/opencode/opencode.jsonc|json`), Claude Code, Windsurf,
Continue, Gemini, Qwen, Trae, Comate, CodeBuddy, Kimi, Kiro, VS Code and Zed;
additional hosts are best-effort candidates and are reported as
`unverified` when absent. JSON, JSONC and a narrow TOML `[mcp_servers.*]`
subset are parsed; YAML is reported as `unsupported`, never silently skipped.
Only server names are returned; commands, args and env values are never
included. `summary.all_clear` is true only for a fully covered, issue-free
default scan; always read `coverage_confidence` before treating it as
all-clear.

## scan_secrets

Input: `path` or `text`, optional `max_findings`, optional `include_git_history`
(bounded, default false).

Output: `findings` with `path`, `line`, `rule`, `severity`, redacted `evidence`,
`suggestion`; `truncated`.

High-entropy findings apply a narrow noise filter for absolute paths,
URL / `file://` percent-encoded paths, common binary/source/document
suffixes and hash-context hex values (SHA-1/256/512, MD5, checksum, digest,
integrity). Credential-name, AWS-key and private-key rules are not relaxed.

## scan_dependencies

Input: `path`.

Output: `manifests`, `lockfiles`, `issues` (`missing-lockfile`,
`unpinned-dependency`, `insecure-source`, `local-dependency`,
`typosquat-suspicion`), and counts. Offline heuristics only.

## check_publish_readiness

Input: `path`.

Output: `ok`, `files`, `versions` (package / skill / changelog / engine when
present), `issues`.

## run_checks

Input: `kind` (`python-unittest` / `pytest` / `python-compile` / `npm-test` /
`npm-lint`), `cwd`, optional `timeout`, explicit `allow_execute=true`.

Output: `exit_code`, `passed`, bounded `summary`, compressed `output`,
`timed_out`.

## scaffold_skill

Input: `name`, `output_dir`, optional `description`, explicit `apply=true`.

Output: `target`, `files`, `applied`. Default is dry-run; existing non-empty
targets are rejected.

## workflow_state

Input: `root`, `action` (`read` / `append-log` / `append-file`), optional
`date`, `text`, `file`, explicit `apply=true`.

Output: `ok`, `files`, `missing`, `excerpts` for read; `target`, `applied`,
`preview` for writes. Writes use a random exclusive temporary file plus
`os.replace`, keep a `.bak` of an existing file, and reject target or ancestor
paths that are symlinks, junctions or other reparse points.
