## Description:

Red Team Pro is a Chinese adversarial plan review workflow that challenges plans, decisions, and arguments through rounds focused on logic flaws, execution risks, and worst-case scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

External users and decision makers use this skill to pressure-test plans, product ideas, strategy, technical proposals, and arguments before acting on them. It guides the agent through background intake, adversarial role selection, three rounds of critique, optional remediation, and a concise resilience assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README recommends an unpinned npx install command that can execute mutable remote code.

Mitigation: Install from a verified ClawHub release or pin the package and version before running installation commands.

Risk: Broad activation wording may cause the skill to apply an adversarial critique style when a neutral review is expected.

Mitigation: Confirm that the user wants a red-team critique before applying the workflow, and make any remediation step explicit and optional.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/boboy-j/skills/red-team-pro)
- [Attackers Reference](references/attackers.md)
- [Example Startup Plan](examples/example-startup-plan.md)
- [Test Cases](tests/test-cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured critique sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language adversarial review with optional targeted remediation.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
