## Description:

Helps developers turn a Rotifer-specific goal into an Agent by selecting Genes, composing a Genome, and guiding creation and testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to plan and create Rotifer Agents from Genes, select a composition strategy, and validate the result with the Rotifer CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI commands can install packages, change project or user files, and make outbound registry or Arena requests.

Mitigation: Review the proposed commands and their effects; follow the skill's approval step before installing, publishing, or overwriting, and inspect the target Genes and Agent configuration.

Risk: Security analysis had partial reference checks, so some local references were unresolved.

Mitigation: Treat the scan as incomplete evidence and review the unresolved references before installing or using the skill.

## Reference(s):

- [Rotifer Documentation](https://rotifer.dev/docs)
- [Rotifer Protocol](https://rotifer.dev)
- [Rotifer Protocol Specification](https://github.com/rotifer-protocol/rotifer-spec)
- [Rotifer Playground Repository](https://github.com/rotifer-protocol/rotifer-playground)
- [Rotifer Agent Release](https://clawhub.ai/xiaoba-dev/skills/rotifer-agent)
- [Rotifer Arena Skill](https://clawhub.ai/skill/rotifer-arena)
- [Rotifer Guide Skill](https://clawhub.ai/skill/rotifer-guide)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focused on Rotifer Agent creation; may include a Gene decomposition, Genome composition plan, and validation steps.]

## Skill Version(s):

1.2.13 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
