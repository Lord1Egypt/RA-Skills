## Description: <br>
Vemem helps agents remember and resolve visual entities such as faces, objects, and places across sessions by storing persistent identity references and related context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linville-charlie](https://clawhub.ai/user/linville-charlie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs persistent visual identity memory: recognizing previously introduced people, objects, or places, labeling new observations, correcting identity mistakes, or deleting stored identity data on request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for persistent visual identity memory and may involve sensitive biometric-style data. <br>
Mitigation: Install only when that behavior is desired, start with a dedicated test VEMEM_HOME, and use the documented privacy primitives for deletion, restriction, and export when handling stored identity data. <br>
Risk: Optional example recipes can combine vemem with remote vision or language APIs, which may send private images outside the local machine. <br>
Mitigation: Use local vision and language models for private images unless the user has accepted the remote provider data flow. <br>
Risk: The optional OpenClaw sidecar can automatically process every image attachment when separately installed and enabled. <br>
Mitigation: Keep the base skill on manual invocation unless automatic image recognition is explicitly required, and enable the sidecar only after reviewing that behavior. <br>
Risk: The runtime depends on an external Python package and first-use model weights. <br>
Mitigation: Pin and verify the vemem package version before deployment and account for the first-use InsightFace model download. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linville-charlie/vemem) <br>
- [vemem homepage](https://github.com/linville-charlie/vemem) <br>
- [MCP tool reference](references/mcp-tools.md) <br>
- [Examples](references/examples.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct an agent to invoke vemem tools that read user-provided images and maintain local identity memory.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
