## Description: <br>
Sage Coo is an AI COO partner for 1-30 person startup teams that helps founders turn team operations, delivery, hiring, performance, and business reviews into clear operating rhythms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billzhuang6569](https://clawhub.ai/user/billzhuang6569) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders, operators, and agents working with small startup teams use this skill to bootstrap and maintain a COO-style operating workspace, capture durable company facts, and turn organizational questions into judgments, risks, next steps, and selected memory updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initialize ~/.sage, store company facts for future sessions, and alter workspace instruction files such as AGENTS.md, CLAUDE.md, SOUL.md, and related files. <br>
Mitigation: Review the scripts and planned file changes before installation or execution; run setup scripts manually when working in confidential business workspaces. <br>
Risk: The security scan reports that the skill asks agents to maintain shared long-term company memory without enough explicit user control. <br>
Mitigation: Require user confirmation before promoting uncertain, private, financial, credential, customer, or personal information into durable company memory. <br>


## Reference(s): <br>
- [Sage Coo ClawHub release page](https://clawhub.ai/billzhuang6569/sage-coo) <br>
- [COO identity](references/coo-identity.md) <br>
- [COO operating system](references/coo-operating-system.md) <br>
- [COO scenarios](references/coo-scenarios.md) <br>
- [Onboarding](references/onboarding.md) <br>
- [OpenClaw workspace bootstrap](references/openclaw-workspace-bootstrap.md) <br>
- [Sage DNA protocol](references/sage-dna-protocol.md) <br>
- [Write routing](references/write-routing.md) <br>
- [Review cadence](references/review-cadence.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file/configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initialize or update workspace instruction files and the user's ~/.sage company memory when run by an agent with filesystem access.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
