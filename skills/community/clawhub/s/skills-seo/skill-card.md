## Description:

Analyze and optimize a skill for discoverability on ClawHub, skills.sh, and similar skill directories. Use when you need to improve naming, slug choice, SKILL.md descriptions, query coverage, examples, listing conversion, or search visibility before publication, while keeping the skill broadly compatible with OpenClaw, Claude Code, Codex, and Cursor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwwdn](https://clawhub.ai/user/fwwdn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this agent skill to audit and improve a skill package's listing discoverability, search recall, metadata, examples, and conversion copy before publication on ClawHub, skills.sh, or similar directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose changes to listing text or metadata that overstate what the target skill actually does.

Mitigation: Review proposed copy changes for accuracy and preserve the target skill's real capability boundary before publishing.

Risk: The analyzer is a static discoverability heuristic and can miss runtime defects or end-to-end behavior issues.

Mitigation: Use separate implementation tests or a follow-up quality pass when the concern is functional correctness rather than listing discoverability.

Risk: The skill can edit a target skill when asked, which may alter public-facing publication material.

Mitigation: Review diffs and rerun the analyzer before release; do not publish unreviewed metadata or first-screen rewrites.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/fwwdn/skills/skills-seo)
- [Platform Signals](references/platform-signals.md)
- [Optimization Patterns](references/optimization-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with optional rewritten skill metadata, SKILL.md copy, analyzer commands, and prioritized action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON when the bundled analyzer is run with --json.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
