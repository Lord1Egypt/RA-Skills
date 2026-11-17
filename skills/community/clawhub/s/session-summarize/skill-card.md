## Description:

Summarize helps Codex produce evidence-first task summaries, compact checkpoints, handoffs, and risk-aware recommendations from the current visible session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtbwpkwjnb-alt](https://clawhub.ai/user/gtbwpkwjnb-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to summarize active Codex work, preserve verified status and unknowns, prepare handoffs, and save project-local handoff reports only when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published one-line installers can execute mutable remote GitHub scripts at install time.

Mitigation: Install from the reviewed local package or a pinned, checksum-verified release instead of piping remote installer output directly into a shell.

Risk: The Unix updater can remove an existing installation before a replacement is validated.

Mitigation: Back up the existing summarize skill directory before updating and prefer an update path that preserves the current installation until the replacement is validated.

Risk: Saved handoff reports may write project-local files when explicitly requested.

Mitigation: Use the default read-only modes unless persistence is intended, and review the target project path before running a save workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gtbwpkwjnb-alt/skills/session-summarize)
- [README](README.md)
- [Changelog](references/CHANGELOG.md)
- [Recommendations](references/recommendations.md)
- [Operations](references/operations.md)
- [History Diagnostics](references/history-diagnostics.md)
- [Layered Handoff](references/layered-handoff.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries, handoff prompts, checkpoints, diagnostics, and optional saved handoff files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; project-local handoff persistence is used only after an explicit save request.]

## Skill Version(s):

11.0.0 (source: server release metadata, VERSION, manifest.json, and changelog, released 2026-07-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
