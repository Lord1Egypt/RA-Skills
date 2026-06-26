## Description: <br>
Defines a unified file protocol that bundles data, logic, and views into a self-contained unit for human-agent and agent-agent collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozii](https://clawhub.ai/user/mozii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and external teams use this protocol reference to design Selfware packages, declare canonical data boundaries, and define consent-aware update, discovery, collaboration, memory, packaging, and publishing flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Implementers may treat the protocol reference as a complete runtime. <br>
Mitigation: Verify any Selfware implementation separately before use, including API binding, write scope, update behavior, and consent prompts. <br>
Risk: A runtime could expose APIs beyond localhost or write outside the declared content scope. <br>
Mitigation: Require loopback-only API binding by default and confirm that writes are limited to the declared canonical content scope. <br>
Risk: Remote updates, discovery requests, publishing, or context sharing could be applied or sent without informed user approval. <br>
Mitigation: Show summaries or diffs, create rollback points, and require explicit confirmation before applying remote changes or sending context externally. <br>


## Reference(s): <br>
- [Selfware release page](https://clawhub.ai/mozii/selfware) <br>
- [Release changelog](https://github.com/floatboatai/selfware.md) <br>
- [Protocol source](https://floatboat.ai/selfware.md) <br>
- [Protocol source repository](https://github.com/floatboatai/selfware) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown protocol guidance with example API shapes, metadata fields, and packaging rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Protocol/reference skill; no runtime is included in the release artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
