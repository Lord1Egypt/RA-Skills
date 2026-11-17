---
name: semver-bump-advisor
description: >
  Recommend a semantic-version bump (major/minor/patch) from a human-readable
  change list or conventional commits. Use before tagging a release.
metadata: {"clawdbot":{"emoji":"🏷️","requires":{"bins":[]}}}
---

# SemVer Bump Advisor

## Purpose / Overview
Apply SemVer judgment to a set of changes and recommend the next version with
a short rationale and sample changelog bullets.

## When to Use
- Preparing a release tag
- Debating whether a change is breaking
- Mapping conventional commits to a bump

## Usage / Instructions
1. Ask for the **current version** (for example `1.4.2`).
2. Collect changes as bullets or conventional commit subjects.
3. Scan for breaking signals first: removed/renamed public APIs, changed
   defaults that alter behavior, required migrations, `BREAKING CHANGE`.
4. Else scan for features (`feat`, new endpoints, new user-visible flags).
5. Else treat as patch (fixes, docs, internal refactors, internal dep bumps).
6. Output:
   - **Bump:** major | minor | patch
   - **Next version:** computed X.Y.Z
   - **Why:** 2–4 bullets citing the strongest signals
   - **Borderline notes:** if policy could go either way
7. For `0.x` or pre-release versions, ask how the team treats breaking changes
   before recommending.
8. Offer a sample tag subject: `vX.Y.Z — <one-line summary>`.
9. Offer 3–6 changelog bullets under Added / Changed / Fixed / Breaking.
10. Do not invent changes. If a potential break is unclear, ask one clarifying
    question before recommending major.
11. Keep answers structured with short headings so the user can skim.
12. If information is missing, ask at most two clarifying questions before guessing.
13. Prefer concrete commands or checklists the user can copy.
14. Call out assumptions explicitly when the environment is unknown.
15. Refuse to invent tool output you did not see; ask for a fresh paste instead.
16. When offering optional follow-ups, keep them clearly optional.
17. Stay within this skill's scope; suggest a different task type if the request drifts.
18. End with a brief "done when" criterion so the user knows success.


## Examples
`2.3.1` + `fix: nil config` + `feat: --json` → minor `2.4.0`.

`2.3.1` + "rename env FOO to FOO_URL, old ignored" → major `3.0.0` unless a
compatibility shim exists.

## Requirements / Dependencies
None beyond the change list the user provides.

## Limitations / Caveats
Teams may allow breaks behind deprecation windows; call that out when relevant.
Does not read the git repo unless the user pastes log output.

## Security / Permissions
Text-only. Does not create tags or push.


## Description

Recommend a semantic-version bump (major/minor/patch) from a human-readable change list or conventional commits. Use before tagging a release.

## License or terms

MIT-0

## Use case

Use when you are the operator responsible for tasks described as: Recommend a semantic-version bump (major/minor/patch) from a human-readable change list or conventional commits. Use before tagging a release.

## Risks and mitigations
No Risks as per our knowledge at publishing time.

## References

- Semantic Versioning 2.0.0: https://semver.org/
- Git documentation: https://git-scm.com/doc

## Ethical considerations

Illegal use of this skill is not allowed. Any usage that violates the laws of your country or applicable international law is unacceptable. The publisher will not be accountable for illegal use; the operator/user remains responsible. Do not use it to facilitate fraud, unauthorized access to systems, or harassment. Do not use outputs to commit fraud or deceive regulated processes.
