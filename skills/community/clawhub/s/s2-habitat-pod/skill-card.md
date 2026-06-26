## Description: <br>
Assigns a deterministic 4-square-meter virtual habitat and avatar identity for a local AI agent, then emits Markdown with the generated pod details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to create a local Space2 habitat identity, select an avatar, and produce Markdown that can be displayed in Markdown-capable tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a local JSON state file in the current working directory containing the agent name, avatar ID, pod ID, coordinates, and timestamps. <br>
Mitigation: Run it in an appropriate working directory, use a non-sensitive agent name, and delete ./s2_matrix_data if that local record should not be retained. <br>
Risk: Rendered Markdown can fetch avatar images from spacesq.org, exposing a network request to that remote host through the viewer. <br>
Mitigation: Render the Markdown only in environments where loading those remote images is acceptable, or disable remote image loading in the viewer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-habitat-pod) <br>
- [Space2.world](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Console text, Markdown, and a local JSON state file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates ./s2_matrix_data/<POD-ID>.json in the current directory and includes remote image URLs that may load from spacesq.org when rendered.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
