# AGENTS.md — openmarlin-skill

## Workflow Rules

- Every commit should be associated with the relevant GitHub issue when one exists.
- Pure housekeeping or wording-only cleanups do not need a synthetic issue just to satisfy linkage.
- After landing meaningful progress, update the linked issue with implementation status and verification notes.
- When a scoped issue is fully implemented, close that issue instead of leaving it open as stale follow-up.
- For larger or riskier changes, prefer creating a dedicated branch with the `codex/` prefix and land the work through a pull request instead of pushing directly to `main`.
- For smaller, low-risk, or clearly scoped changes, it is fine to commit directly to the current branch and skip a pull request.
- When using `gh` commands with long or Markdown-heavy bodies, prefer `--body-file` with a temporary file over inline `--body`.
- Do not embed Markdown containing backticks, `$()`, or complex quoting directly inside `zsh -lc` command strings unless there is a strong reason.
- For generated pull request bodies or issue comments, default to writing Markdown to `/tmp/*.md` and passing it via `--body-file`.

## Skill-side Constraints

- Keep the UX OpenClaw-first by default.
- Treat `SKILL.md` frontmatter as both user-facing skill metadata and
  OpenClaw/ClawHub registry metadata.
- If the skill depends on required env vars, primary credentials, install-time
  binaries, or OpenClaw state access, keep `metadata.openclaw` aligned with the
  real runtime behavior.
- Do not remove or simplify required `metadata.openclaw` fields just to make
  frontmatter look smaller or more generic.
- Use browser handoff only for irreducible external steps such as WorkOS auth or Stripe checkout.
- Do not invent server contracts that do not exist.
- When balance or ledger state is only partially observable from public APIs, label the OpenClaw view as last-known or estimated instead of pretending it is authoritative.
- Do not store platform API keys in ordinary plain config when auth-profile storage is available.
