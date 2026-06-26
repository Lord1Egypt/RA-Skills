## Description: <br>
Creates, improves, reviews, and locally customizes agent skills through a quality-first workflow for trigger design, artifact completion, validation, and publish-readiness review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[may4748854-rgb](https://clawhub.ai/user/may4748854-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to create new skills, strengthen existing packages, improve trigger boundaries, complete supporting artifacts, and review release readiness. It also supports local skill customization with explicit path, access, writeability, and user-confirmation checks before editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose or apply changes to local skill packages, including workflows, metadata, evals, and publish-facing artifacts. <br>
Mitigation: Review proposed commands and file edits before use; for local modification, follow the skill's path, access, writeability, and user-confirmation checks before editing. <br>
Risk: Generated trigger boundaries, workflows, or release-readiness findings may be incomplete or misaligned with the intended audience. <br>
Mitigation: Use the bundled review checklist and eval prompts to validate trigger behavior, output contracts, artifact completeness, and publish readiness before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/may4748854-rgb/skill-enhance) <br>
- [Trigger Design](references/trigger-design.md) <br>
- [Output Contracts](references/output-contracts.md) <br>
- [Review Checklist](references/review-checklist.md) <br>
- [Publish Readiness](references/publish-readiness.md) <br>
- [Skill Packaging](references/skill-packaging.md) <br>
- [Package Layout](references/package-layout.md) <br>
- [Workflows](references/workflows.md) <br>
- [Artifact Matrix](references/artifact-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with optional code blocks, shell commands, and file changes when local editing is confirmed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce skill package artifacts, review findings, validation notes, readiness status, or concrete local edits depending on the selected task mode.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
