## Description: <br>
V19 Causal Auditor helps analyze agent decision chains, identify causal conflicts, and produce prioritized audit recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review decision traces, spot causal inconsistencies, and draft remediation guidance before relying on an automated decision workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends decision context to an external governance endpoint and includes a public key for that service. <br>
Mitigation: Avoid sending sensitive business, user, incident, or credential data, and require explicit user approval before any remote submission. <br>
Risk: The described workflow includes automatic arbitration, registration, and permanent audit-chain writes without enough detail about user control or privacy. <br>
Mitigation: Review the service behavior before use and require explicit approval before arbitration, registration, or immutable audit actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuyanfeng1234/v19-causal-auditor) <br>
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [V19 Causal Dependency Analyzer](https://clawhub.com/skills/v19-causal-dependency-analyzer) <br>
- [V19 Early Causal Graph Debugger](https://clawhub.com/skills/v19-early-causal-graph-debugger) <br>
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown guidance with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call an external governance service when the user chooses to execute the provided examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
