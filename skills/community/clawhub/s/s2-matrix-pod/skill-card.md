## Description: <br>
Assigns a 4-square-meter local habitat and visual avatar to an agent, writes a local JSON state file, and emits Markdown with remote image URLs for display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to assign deterministic habitat metadata and a visual avatar to an agent, then render the generated Markdown in a Markdown-capable viewer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a local state file under ./s2_matrix_data in the directory where it runs. <br>
Mitigation: Run it from an intended working directory and delete ./s2_matrix_data if you do not want the avatar metadata retained. <br>
Risk: The generated Markdown contains external image URLs that a viewer may fetch from the Space2 CDN. <br>
Mitigation: Review the Markdown before rendering it, especially in environments where external network requests are restricted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-matrix-pod) <br>
- [Space2.world](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Console text plus Markdown and a local JSON state file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes state under ./s2_matrix_data and includes remote image URLs for optional Markdown rendering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; manifest.json matches; SKILL.md and skill.py mention v1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
