---
name: safe-clawhub-publisher
description: Safely validate, dry-run, publish, and verify ClawHub skills and OpenClaw plugins. Use for versioning, changelogs, secret scans, fingerprint checks, authentication, and post-release verification; do not use to design a package.
metadata:
  version: "1.0.0" # x-release-please-version
---

# Safe ClawHub Publisher

Move an existing local package from release candidate to verified ClawHub release. Treat local inspection and dry-runs as reversible; treat login, publication, tag changes, and remote replacement as external mutations.

## Route the package

1. Resolve the exact package directory. Never publish a workspace root by inference.
2. Run `python3 scripts/validate_release_inputs.py <path> --format json` from this skill directory, or use its absolute path.
3. Record the validator's proposed publish file list, exclusions, per-file hashes, and fingerprint. Use them as evidence, not as a substitute for the installed CLI's validation:
   - `skill`: read [references/skill-release.md](references/skill-release.md).
   - `plugin-package`: read [references/plugin-release.md](references/plugin-release.md). Let the current ClawHub CLI determine whether it is a code or bundle package when local metadata is not explicit.
   - `ambiguous` or `unknown`: stop and explain which markers conflict or are missing. Do not guess a publish command.
4. Always read [references/security-checklist.md](references/security-checklist.md) before a dry-run or publication.

## Release workflow

1. Inspect the working tree, package files, ignore rules, generated artifacts, symlinks, and secret-scan findings. Preserve unrelated user changes.
2. Confirm the installed `clawhub` executable and capture its resolved path, version, and the relevant command's `--help`. Use the version flag shown by the installed help rather than assuming `--version`; the installed CLI help is authoritative when examples in this skill differ.
   - If `clawhub` is missing, tell the user that the release cannot proceed without it. Verify the official package identity, query an exact current version from an official source, and show the package manager, installation scope, and pinned install command.
   - Ask for explicit approval before running the installer. Disclose that a global install changes the user's toolchain and may run package lifecycle scripts. Do not install silently, install an unpinned version, or treat a validation/release request as installation permission.
   - After an approved installation, resolve `command -v clawhub`, capture the installed version and help output, and check for conflicting binaries on `PATH`. If installation is declined or unavailable, stop before dry-run and publication and report the missing CLI as the blocker.
3. Establish read-only ClawHub connectivity before requiring remote evidence. If DNS resolution or connection setup fails before any publication attempt, follow the pre-publication network procedure in [references/troubleshooting.md](references/troubleshooting.md). Do not declare a ClawHub outage from one sandboxed failure, and continue every local validation step that does not require the network.
4. Resolve the target owner/slug and inspect the remote package when it exists. Do not infer ownership from a local package name or authenticated handle alone.
5. Compare the remote release with local contents. Read [references/versioning.md](references/versioning.md), propose a version and changelog, and show the evidence behind the choice.
6. Run the package-specific local checks and ClawHub dry-run in machine-readable mode when supported. Capture the server-reported version, file count, status, and fingerprint. A successful local validator is not proof that the server will accept the release.
7. Compare the validator fingerprint with the CLI dry-run fingerprint. A mismatch is a blocker until the actual publish set and exclusion rules are understood.
8. Present a release plan containing target, authenticated account, detected type, proposed version, included files and hashes, exclusions, validation results, fingerprints, tag changes, changelog, and exact publish command.
9. Report every release-critical command result explicitly, especially the final `clawhub skill publish` command, ClawHub dry-run, account check, and remote verification. For any non-zero exit, stderr error, rate-limit notice, unexpected empty output, or missing machine-readable response from these commands, show the user the sanitized error text, exit status when available, command phase, and whether the state is rejected, unavailable, or unknown. Ordinary local helper commands may be summarized unless their failure affects the release decision. Never hide a release-critical error with `|| true`, discard stderr, or report only a generic failure. Redact credentials and token-like values, but preserve actionable server messages such as reserved topics and topic-count limits.
10. Ask for explicit confirmation immediately before publication. A request to prepare, validate, dry-run, install, or log in is not permission to publish. Confirmation applies only to the displayed account, target, version, command, file set, metadata, and fingerprint.
11. Run the pre-publication integrity gate below, then publish once. Never retry automatically. If ClawHub rejects the command, a user may explicitly request a retry after the exact corrected command is displayed and confirmed; every retry must repeat the integrity gate and use one new publication attempt. If the outcome is unclear, follow the fixed verification budget in [references/troubleshooting.md](references/troubleshooting.md): at most two non-mutating remote checks for that attempt, then stop and hand control back to the user.
12. Verify the remote version, metadata, file hashes, tags, changelog, owner, and security status. For an unclear publish response, check immediately and at most once more after the server's `Retry-After` delay, capped at two minutes. When machine-readable inspection remains unavailable or stale, give the user the canonical package page `https://clawhub.ai/<owner>/skills/<slug>` and stop automated work. Record user-visible confirmation separately from CLI/API verification.

## Authentication interaction

1. Check the current account with `clawhub whoami` before starting a login flow. Do not log in again when the existing authenticated account matches the intended owner. If the user has not supplied an owner, present the authenticated handle only as a candidate and obtain confirmation before targeting a dry-run or publication.
2. If authentication is missing or belongs to the wrong account, explain the mismatch and obtain explicit approval before starting login because login changes the local credential store.
3. Prefer the CLI's device flow in a persistent interactive session. When supported by the installed CLI, use `clawhub login --no-browser`, show the verification URL and one-time code to the user, and keep the process alive while authorization is pending.
4. Never ask the user to paste an API token into chat and never expose, print, or relay a stored token. The verification URL and short-lived device code are the only authentication details that may be shown.
5. Wait in bounded intervals and keep the user informed without restarting an unchanged login process. If the code expires or the session ends, report that clearly and obtain approval before starting a fresh device flow.
   - If the environment cannot preserve an interactive session, ask the user to run the same device-flow command in their own terminal and return after it succeeds. Do not request a token as a fallback.
6. After the CLI reports success, run `clawhub whoami` and show the authenticated handle. If it does not match the intended owner, stop; do not switch accounts, transfer ownership, or change the release target by inference.
7. After account verification, repeat remote inspection and dry-run because authentication can change owner resolution or server behavior.
8. Authentication approval is not publication approval. Present or refresh the exact release plan and obtain a separate explicit confirmation for the final publish command.

## Pre-publication integrity gate

Immediately before publishing, without editing or rebuilding the package:

1. Re-run the bundled validator with `--expect-fingerprint <confirmed-fingerprint>` and repeat the exact ClawHub dry-run.
2. Require the package path, owner/slug, version, included file list, file count, and fingerprints to match the confirmed plan.
3. Inspect the remote target again and confirm that the immutable version is still absent and the expected prior version and tags have not changed.
4. Re-run `clawhub whoami` and require the authenticated handle to match the confirmed owner.
5. If any value differs, do not publish. Explain the change, refresh the release plan, and obtain new confirmation.

Use [assets/release-report.md](assets/release-report.md) for a reusable report. For CI-only dry-runs, adapt [assets/github-actions.yml](assets/github-actions.yml); keep publication in an explicitly dispatched job with protected secrets.

## Safety invariants

- Never print, echo, copy into arguments, or persist authentication tokens. Use the CLI's supported authentication flow or preconfigured CI secrets.
- Never publish from an unreviewed temporary directory, archive extraction, or path containing unresolved symlinks.
- Never run package lifecycle scripts, builds, installers, or unrelated network probes merely to validate metadata unless the user approves their effects. A required read-only ClawHub inspection may be retried once through the execution environment's network approval or escalation mechanism; never bypass a denial or treat that approval as authorization to log in or publish.
- Never install a missing ClawHub CLI automatically. Present the official package identity and a pinned installation command, disclose its scope, and obtain explicit approval immediately before running it.
- Do not edit versions, changelogs, manifests, tags, or ignore files unless the user asks to prepare those changes. Prefer a recommendation and patch preview.
- Do not add broad ignore rules to silence a secret finding. Remove the secret from the release candidate and rotate it when exposure is plausible.
- Do not use `npx` to fetch an unpinned ClawHub CLI during a release. Prefer an already installed, identified executable.
- Do not claim machine-verified completion until authoritative remote evidence confirms the intended immutable version. A canonical ClawHub page may serve as authoritative UI evidence; when confirmation comes only from the user viewing that page, label it `user-confirmed in ClawHub UI` rather than CLI/API-verified.
- Use a publication attempt boundary: never issue a retry automatically. A retry is permitted only after authoritative rejection/failure evidence, a corrected exact command, a fresh user confirmation, and a repeated integrity gate. Do not retry an ambiguous outcome without remote verification; stop and hand control back to the user after the bounded checks for that attempt.

## Failure handling

Read [references/troubleshooting.md](references/troubleshooting.md) for pre-publication network failures, authentication failures, duplicate versions, type ambiguity, rejected manifests, pending scans, and uncertain publish outcomes. Stop when the next action would require different credentials, a changed target, destructive cleanup, or a broader release scope.
