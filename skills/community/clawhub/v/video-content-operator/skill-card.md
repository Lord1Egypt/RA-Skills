## Description: <br>
Helps creators decide what video or social content to make, how to package it for platforms, which source materials to use, and what content move to make next. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, founder-builders, operator creators, and small teams use this skill to clarify creator state, choose source material, package content for platforms, draft content directions, and prepare handoffs for video execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personalization may use local OpenClaw memory/profile files that contain sensitive creator context. <br>
Mitigation: Review MEMORY.md and USER.md before use, pass only the intended workspace path, and avoid saving extracted context to shared or insecure locations. <br>
Risk: Content recommendations are strategic drafts and may be incomplete or misaligned with the creator's real goals. <br>
Mitigation: Review the recommended direction and draft packages before handing them off to a video execution tool. <br>


## Reference(s): <br>
- [Video Content Operator MVP](references/mvp.md) <br>
- [Sparki Content Operator MVP Spec](references/mvp-spec.md) <br>
- [Input Schema](references/input-schema.md) <br>
- [Output Examples](references/output-examples.md) <br>
- [Implementation Notes](references/implementation-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown recommendations and JSON execution briefs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local OpenClaw memory/profile files when an explicit workspace path is provided.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
