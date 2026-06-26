## Description: <br>
Red Team Pro guides an agent through a Chinese adversarial review workflow that challenges plans, decisions, and arguments through logic, execution, and worst-case risk rounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and decision makers use this skill to stress-test proposals before execution, surface blind spots, and decide which risks must be addressed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally produces direct adversarial critique, which may be too blunt for some planning or decision-review contexts. <br>
Mitigation: Use it when aggressive challenge is desired, and review the output before sharing it with stakeholders. <br>
Risk: The skill defaults to Chinese output. <br>
Mitigation: Ask the agent for another output language when the review audience does not read Chinese. <br>
Risk: The marketplace metadata and README install command do not use the same package name. <br>
Mitigation: Install from the server-resolved ClawHub listing or verify the package name before deployment. <br>


## Reference(s): <br>
- [Attacker role guide](references/attackers.md) <br>
- [ClawHub skill listing](https://clawhub.ai/boboy-j/red-team-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style structured critique with risk ratings, prioritized issues, and optional remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Chinese and uses a direct adversarial tone.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
