## Description: <br>
简历生成技能（W工作室） guides users through structured resume information collection and produces Reactive Resume v2 JSON that can be imported into aicv.weinuo.work to create a polished resume PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xk103295870-alt](https://clawhub.ai/user/xk103295870-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and job seekers use this skill to provide resume details in a guided flow, choose a resume theme, and generate Reactive Resume v2 JSON, a PDF preview, and a markdown information backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users for sensitive resume information and later directs them to upload generated resume JSON to an external website, despite a local-only privacy statement in the artifact. <br>
Mitigation: Review before installing if real personal details will be entered, minimize or use placeholder data when appropriate, and delete local JSON, PDF, and markdown backup files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xk103295870-alt/resume-gen-ws) <br>
- [AI resume platform](https://aicv.weinuo.work) <br>
- [Reactive Resume schema](https://rxresu.me/schema.json) <br>
- [Reactive Resume Schema v2.0 reference](references/schema.md) <br>
- [Resume generation template reference](references/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, guidance] <br>
**Output Format:** [Guided text plus generated Reactive Resume v2 JSON, PDF preview, and markdown backup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated resume content can contain sensitive personal details and may be imported into an external resume website.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
