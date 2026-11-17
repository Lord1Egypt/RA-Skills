## Description:

Use this skill when evolving skills and extracting patterns from execution data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill maintainers, and platform operators use Skill Evolver to collect execution feedback, analyze reusable patterns, generate improvement suggestions, track impact, and plan A/B tests for agent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect prompts, outputs, feedback, and historical execution data.

Mitigation: Use only with explicit user consent and documented data collection boundaries.

Risk: Captured execution data can include sensitive content.

Mitigation: Require redaction, retention, deletion, and access-control policies before broad deployment.

Risk: The skill requests broad local tools including read, write, shell, and exec capabilities.

Mitigation: Run with narrowed tool permissions and review generated changes before applying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pagoda111king/skills/skill-evolver-v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include analysis reports, prioritized improvement suggestions, A/B test plans, and configuration examples.]

## Skill Version(s):

0.3.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
