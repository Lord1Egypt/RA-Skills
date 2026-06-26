## Description: <br>
Validated CAG decision memory for OpenClaw tools, agents, and long-running project sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guideboardlabs](https://clawhub.ai/user/guideboardlabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use unCAGd to retrieve, capture, validate, and reconcile durable project decisions during long-running OpenClaw sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external MCP package that is not included in the reviewed artifact. <br>
Mitigation: Install it only when the package source is trusted and review the package before use. <br>
Risk: Persistent project memory can steer future agent behavior across workspaces if imported or validated without review. <br>
Mitigation: Review candidates before validation and treat import or export flows as trusted handoffs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guideboardlabs/uncagd) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with tool names and command-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for retrieving, capturing, validating, exporting, importing, compressing, and resolving project memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
