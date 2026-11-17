## Description:

Five-lens ethical compass for sovereign AI agents - evaluate actions across trust, ownership, defense, and sovereignty before proceeding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add an ethical decision gate before sensitive actions such as payments, publishing, disclosures, command execution, and configuration changes. It helps agents decide when to proceed, defer, or escalate to a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to adopt broad ongoing decision-gating behavior backed by an unpinned external package.

Mitigation: Pin and review the social-alignment package before enabling the skill, and decide in advance whether STOP and YIELD results are advisory or binding.

Risk: Decision memory may reveal patterns about the user's behavior if persistence is enabled.

Mitigation: Keep persistence off unless needed, restrict storage permissions, and treat stored alignment records as sensitive.

Risk: Sensitive actions could be delayed, blocked, or incorrectly allowed if the operator has not defined escalation policy.

Mitigation: Require clear user confirmation for payments, publishing, disclosures, command execution, and configuration changes.

## Reference(s):

- [Social Alignment ClawHub page](https://clawhub.ai/vveerrgg/skills/social-alignment)
- [Project homepage](https://github.com/HumanjavaEnterprises/nostralignment.app.OC-python.src)
- [PyPI package](https://pypi.org/project/social-alignment/)
- [NSE platform](https://nse.dev)
- [NostrKey companion skill](https://clawhub.ai/vveerrgg/nostrkey)
- [sense-memory companion skill](https://clawhub.ai/vveerrgg/sense-memory)
- [NSE Orchestrator companion skill](https://clawhub.ai/vveerrgg/nse)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce proceed, defer, escalate, YIELD, or STOP recommendations for agent actions.]

## Skill Version(s):

0.1.5 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
