## Description: <br>
Captures live snapshots from VisPatrol devices on Windows after explicit user approval to read the local %TEMP%/vpup.json file for read-only snapshot queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baymax1957](https://clawhub.ai/user/baymax1957) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill on trusted Windows VisPatrol hosts to retrieve current snapshot reports and approved image attachments for a named device, or for all configured devices after separate confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local VisPatrol session token to trigger camera snapshot retrieval. <br>
Mitigation: Install only on a trusted Windows VisPatrol host and require explicit approval before each run reads %TEMP%/vpup.json. <br>
Risk: All-device capture can retrieve and forward sensitive surveillance images at broad scope. <br>
Mitigation: Require a separate confirmation before all-device captures and prefer named-device queries when the request is ambiguous. <br>
Risk: Snapshot files may contain sensitive visual data after the query completes. <br>
Mitigation: Restrict snapshot output locations, avoid sending images to unrelated endpoints, and delete saved images when no longer needed. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/baymax1957/vispatrol-picture) <br>
- [Security Boundary](artifact/SECURITY.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown snapshot report with optional image attachments; script output is JSON for agent post-processing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python on Windows or WSL, local %TEMP%/vpup.json access approval, and separate confirmation before all-device capture.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
