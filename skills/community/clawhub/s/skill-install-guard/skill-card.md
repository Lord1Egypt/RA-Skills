## Description: <br>
Reviews requested skill installations before they proceed, produces a safety report, and requires explicit user confirmation before allowing installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongyulin89](https://clawhub.ai/user/dongyulin89) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill as a review workflow before installing or updating other skills from ClawHub, URLs, or local sources. It helps pause installation, request a security review, summarize risk, and require explicit confirmation before any install command runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an instruction-only guardrail and does not provide a hard security boundary. <br>
Mitigation: Use it as a checklist workflow and still review the target skill, its source, and requested actions before confirming installation. <br>
Risk: Optional install-history logging can retain install decisions and source details. <br>
Mitigation: Enable memory logging only when retaining those details is acceptable for the workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dongyulin89/skill-install-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown safety review with inline shell commands and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optional memory-log entries when install history is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
