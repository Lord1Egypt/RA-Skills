## Description:

Helps Chinese-speaking users refine skill descriptions, profile projects, and generate evidence-based skill and plugin recommendations while staying read-only by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtbwpkwjnb-alt](https://clawhub.ai/user/gtbwpkwjnb-alt)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent users use this skill to audit local skill/plugin ecosystems, refine Chinese UI descriptions, profile projects, and prepare evidence-backed recommendations for keeping, upgrading, replacing, introducing, coexisting with, or archiving tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local skill/plugin directories, MCP config metadata, and session transcripts when the usage-signal collector is explicitly run.

Mitigation: Limit scans to the paths and clients needed for the task, avoid broad all-client scans unless necessary, and review reports before acting on recommendations.

Risk: Recommendations may be mistaken for completed install, update, archive, or uninstall actions.

Mitigation: Treat reports as read-only advice, require explicit user approval for follow-up changes, and verify any action through the appropriate agent or tool before considering it applied.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtbwpkwjnb-alt/skills/skills-summarize-audit)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Output contract](references/output-contract.md)
- [Report template](references/report-template.md)
- [Actions schema](references/actions-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown reports with optional JSON output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only recommendations by default; exported reports require an explicit output request.]

## Skill Version(s):

9.2.2 (source: changelog, package.json, VERSION, released 2026-09-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
