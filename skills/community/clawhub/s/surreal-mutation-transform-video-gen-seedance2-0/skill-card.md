## Description: <br>
Generates surreal, short-form text-to-video or single image-to-video clips with WeryAI Seedance 2.0, using expanded cinematic prompts and fixed model constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and agent operators use this skill to turn short creative briefs or a single image into surreal Seedance 2.0 video generations with confirmation before paid API execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WeryAI API key and sends prompts, public image URLs, or explicitly selected local images to WeryAI. <br>
Mitigation: Install and run only when comfortable sharing those inputs with WeryAI, and never store the API key in skill files or logs. <br>
Risk: Local image paths can be read and uploaded by the bundled script when the user deliberately chooses that flow. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after reviewing the selected file and confirming consent to upload it. <br>
Risk: Paid generation runs can consume credits, and the script does not enforce the skill's SEEDANCE_2_0-only policy in code. <br>
Mitigation: Confirm paid settings before execution and verify the request JSON uses model SEEDANCE_2_0. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/surreal-mutation-transform-video-gen-seedance2-0) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with confirmation tables, inline video links, and shell command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WeryAI video task submissions and returns playable video URLs or clear failure details.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
