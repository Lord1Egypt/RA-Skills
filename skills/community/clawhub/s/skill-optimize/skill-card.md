## Description: <br>
Audits and improves existing Agent Skills (SKILL.md files) against the agentskills.io standard, including specification compliance, best-practices alignment, and description optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mebusw](https://clawhub.ai/user/mebusw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to audit, polish, and refine existing Agent Skills before publication or iteration. It produces severity-ranked findings and proposed edits for SKILL.md files, while deferring new-skill creation and eval-driven measurement to skill-creator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose changes to Agent Skill files that may affect future agent behavior. <br>
Mitigation: Review generated reports and diffs before approving edits or publishing an updated skill. <br>
Risk: Broad target discovery can inspect home skill folders or plugin caches when that scope is not intended. <br>
Mitigation: Provide an explicit SKILL.md or skill directory path and avoid broad searches unless the wider scope is deliberate. <br>


## Reference(s): <br>
- [agentskills.io Specification](https://agentskills.io/specification) <br>
- [agentskills.io Best Practices](https://agentskills.io/skill-creation/best-practices) <br>
- [agentskills.io Optimizing Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) <br>
- [OpenClaw skill-format](https://docs.openclaw.ai/clawhub/skill-format) <br>
- [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) <br>
- [Specification checklist](references/specification-checklist.md) <br>
- [Best practices checklist](references/best-practices-checklist.md) <br>
- [Description guide](references/description-guide.md) <br>
- [Common issues](references/common-issues.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, proposed diffs, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity-ranked findings, before-and-after edits, and validation results for Agent Skill files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
