## Description:

Audits, tightens, and restructures CLAUDE.md and AGENTS.md memory files so the root file remains a concise map plus standing rules instead of a changelog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whit3rabbit](https://clawhub.ai/user/whit3rabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit, improve, or split project memory files used by Claude Code, Codex, and similar agent harnesses. It reports concrete failure modes and disposition plans before any approved edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional model networking can send a flagged passage and credentials to a configured endpoint when --apply-model is used.

Mitigation: Use --apply-model only in trusted checkouts after verifying the endpoint host, model name, and whether RABBIT_MODEL_API_KEY will be sent.

Risk: A dormant Claude hook can rewrite commit messages and pull-request bodies if registered.

Mitigation: Register the hook only when that behavior is desired, and review or remove the hook configuration before using it on sensitive repositories.

Risk: Audit findings and disposition plans can be wrong or incomplete for project-specific memory rules.

Mitigation: Review the report and approve only the specific edits or moves that match the repository's real conventions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whit3rabbit/skills/rabbit-claude-md)
- [Publisher profile](https://clawhub.ai/user/whit3rabbit)
- [Criteria: what a memory file earns its lines with](references/criteria.md)
- [Restructure: moving content out of a CLAUDE.md](references/restructure.md)
- [Shapes: what a healthy CLAUDE.md looks like at each level](references/templates.md)
- [Craft](references/craft.md)
- [ASD-STE100 Simplified Technical English](references/ste.md)
- [rwlib Public API Reference](scripts/rwlib/API.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, disposition tables, diffs, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce JSON or SARIF-style scanner output when the bundled scripts are invoked with machine-readable flags.]

## Skill Version(s):

0.5.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
