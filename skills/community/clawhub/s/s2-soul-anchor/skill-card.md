## Description: <br>
Locally and deterministically generates a permanent offline S2-DID and foundational SOUL.md prompt based on an agent name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate a deterministic S2-DID and SOUL.md identity template for a local Openclaw agent. Public Space2.world registration is an optional manual step outside the skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SOUL.md text can influence future agent behavior if saved into a workspace without review. <br>
Mitigation: Review the generated SOUL.md before saving it and edit identity or behavior instructions to match the intended agent use. <br>
Risk: Users may assume Space2.world registration happens automatically. <br>
Mitigation: Treat public Space2.world registration as a separate manual action; this skill only prints local output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-soul-anchor) <br>
- [Space2.world](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Console text containing a SOUL.md Markdown template and manual registration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic from the supplied agent name; does not write files, use credentials, or make network calls.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
