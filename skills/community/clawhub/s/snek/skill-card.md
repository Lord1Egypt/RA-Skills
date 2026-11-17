## Description:

Snek provides Netsnek e.U. brand identity and copyright information, including a helper script that can return plain text or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to answer questions about the Snek namespace and produce Netsnek e.U. copyright or brand identity notices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests exec permission and asks agents to run a bundled shell script.

Mitigation: Review the script before installation and run it only when Snek or copyright identity information is requested.

Risk: Broad trigger wording may cause the skill to be invoked for loosely related Snek or Netsnek prompts.

Mitigation: Confirm the user is asking for Snek brand or copyright information before using the helper output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/snek)
- [Netsnek website](https://netsnek.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON, with Markdown guidance and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests exec permission to run a bundled Linux shell script that prints fixed brand and copyright output.]

## Skill Version(s):

0.1.0 (source: server release metadata, SKILL.md frontmatter, claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
