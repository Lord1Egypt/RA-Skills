## Description: <br>
WenHub provides a three-court AI agent collaboration governance workflow for task assignment, task grading, quality control, reporting, knowledge reuse, security controls, and violation handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18505298102](https://clawhub.ai/user/18505298102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and team leads use this skill to establish a structured multi-agent governance process with separate planning, execution, and quality review roles. It is intended for workspaces that need repeatable task grading, quality scoring, reporting, security handling, and knowledge reuse practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages a persistent multi-agent governance process and workspace files that can influence future agent behavior. <br>
Mitigation: Install it only in projects where that persistent governance model is desired, and review the generated or referenced governance files before relying on them. <br>
Risk: SOUL.md, AGENTS.md, and .wenhub files may become places where users are tempted to store private project information. <br>
Mitigation: Do not place secrets, credentials, customer data, or other private data in those files; use existing secret-management and access-control practices instead. <br>
Risk: Optional templates are obtained from the referenced WenHub website rather than included in the release artifact. <br>
Mitigation: Review downloaded templates separately before adding them to a workspace. <br>


## Reference(s): <br>
- [WenHub ClawHub release page](https://clawhub.ai/18505298102/wenhub) <br>
- [Publisher profile](https://clawhub.ai/user/18505298102) <br>
- [WenHub official website](https://wenhub.huawen-inc.com) <br>
- [Three-court collaboration protocol](references/three-courts.md) <br>
- [Task grading and execution controls](references/task-grading.md) <br>
- [Quality scoring system](references/quality-system.md) <br>
- [Reporting and communication guidelines](references/reporting.md) <br>
- [Security rules](references/security-rules.md) <br>
- [Violation handling system](references/violation-system.md) <br>
- [Karpathy coding principles](references/karpathy-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance with file and process instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or use of persistent workspace governance files such as SOUL.md, AGENTS.md, and .wenhub rules.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
