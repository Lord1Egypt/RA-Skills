## Description: <br>
安全技能插座 is a unified security skill management and routing hub for choosing, invoking, combining, and extending security capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and agent operators use this skill to identify and call registered security skills for skill search, information collection, vulnerability scanning, IOC research, threat monitoring, malware checks, defensive monitoring, auditing, password hardening, and key management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hub can direct an agent toward downstream security skills, scans, monitoring, installs, and updates, but it is not evidence that every downstream skill or source is safe. <br>
Mitigation: Confirm the selected skill and target before scans or monitoring, and review third-party skills before installing or updating them. <br>
Risk: Bulk skill updates or broad ClawHub searches may introduce unreviewed third-party skill behavior into the local environment. <br>
Mitigation: Use bulk updates only for trusted sources and inspect new or changed skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caidongyun/security-skill-hub) <br>
- [Publisher profile](https://clawhub.ai/user/caidongyun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with security skill selection tables, routing examples, and ClawHub command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill routes users to downstream security skills; exact outputs depend on the selected downstream skill and target.] <br>

## Skill Version(s): <br>
2.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
