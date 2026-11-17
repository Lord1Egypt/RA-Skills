## Description:

Skill Reader helps agents interpret an installed skill, ClawHub or GitHub skill URL, or SKILL.md file and produce a structured usage guide covering features, use cases, commands, dependencies, API-key needs, version, and caveats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenwang-dev](https://clawhub.ai/user/kenwang-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and team members use this skill to turn a skill name, install URL, or SKILL.md document into a practical usage manual before installing, evaluating, or reusing a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local skill files or remote skill repositories supplied by a user.

Mitigation: Use it only with sources you intentionally selected, and review the exact source and revision before allowing access.

Risk: The documented workflow encourages trying unfamiliar skills, which can expose the agent to unsafe instructions or side effects.

Mitigation: Run unfamiliar skills only after explicit approval and in a disposable, credential-free sandbox.

## Reference(s):

- [ClawHub Skill Reader page](https://clawhub.ai/kenwang-dev/skills/skill-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Structured Markdown usage guide]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quick-read summaries, conversational examples, dependency notes, cost notes, recommendation tables, and caveats.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
