## Description:

Agent Skills builder, auditor, and improver for cross-platform LLM agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorukardahan](https://clawhub.ai/user/dorukardahan)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent maintainers use Skeall to create, improve, scan, and health-check Agent Skills for cross-platform LLM coding agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health check mode can read sensitive agent configuration, private skill repository, or local session data.

Mitigation: Review the skill before installing in sensitive environments, prefer scan-only mode for untrusted skills, and avoid broad healthcheck-all runs unless local inspection is acceptable.

Risk: Runtime URL validation can make network requests to destinations found in audited skills.

Mitigation: Review destination URLs before active validation and avoid running URL checks on untrusted artifacts until the destination list is understood.

Risk: Generated or proposed skill changes can introduce incorrect guidance or weaken existing safeguards.

Mitigation: Review proposed edits and run a scan before deploying generated or modified skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dorukardahan/skills/skeall)
- [Agent Skills open standard](https://agentskills.io)
- [Anti-patterns in Agent Skills](references/anti-patterns.md)
- [Health Check Reference](references/healthcheck.md)
- [Testing your skill](references/testing.md)
- [SKILL.md template](references/template.md)
- [Scoring methodology](references/scoring.md)
- [Advanced patterns](references/advanced-patterns.md)
- [Anthropic skills guide](https://claude.com/blog/complete-guide-to-building-skills-for-claude)
- [OpenAI Codex skills documentation](https://developers.openai.com/codex/skills/)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, audit reports, inline code blocks, and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits and commands; healthcheck modes may inspect local skill directories and validate URLs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
