## Description: <br>
Zero-trust AI agent governance for OpenClaw. Adds ORGA runtime, Cedar policy enforcement, SchemaPin tool verification, ClawHavoc skill scanning, and cryptographic audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaschadub](https://clawhub.ai/user/jaschadub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add local governance workflows to OpenClaw projects, including Cedar policy authoring, MCP tool schema verification, skill scanning, audit log review, and governed agent scaffolding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external Symbiont runtime package that was not included in the reviewed artifact files. <br>
Mitigation: Review or pin the external symbi package before relying on it for security or compliance decisions. <br>
Risk: Local governance policy may block agent actions according to deny rules or Cedar policies. <br>
Mitigation: Inspect generated .symbiont policy files and explain policy decisions before treating blocks as authoritative. <br>
Risk: Local audit logs may contain operational history from tool usage. <br>
Mitigation: Review retention and access controls for .symbiont audit files before using the skill in sensitive workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jaschadub/symbiont) <br>
- [Symbiont Homepage](https://symbiont.dev) <br>
- [Release Metadata Repository](https://github.com/thirdkeyai/symbi-openclaw) <br>
- [Symbiont Documentation](https://docs.symbiont.dev) <br>
- [SchemaPin](https://schemapin.org) <br>
- [AgentPin](https://agentpin.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, generated configuration snippets, and JSON audit or scan summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or inspect local Symbiont configuration, policy, DSL, and audit files when the user asks for governed project workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
