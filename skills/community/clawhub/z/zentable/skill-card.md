## Description: <br>
Render structured table data as high-quality PNG images using Headless Chrome for chat interfaces, reports, and social media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[con2000us](https://clawhub.ai/user/con2000us) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use zenTable to turn raw text, structured JSON, or OCR-assisted table data into readable visual table outputs for chat, reporting, and sharing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to fetch runnable code from an external GitHub release. <br>
Mitigation: Review the downloaded release contents, pin an exact version or hash when possible, and install in a controlled environment. <br>
Risk: OCR and API behavior may process sensitive table, screenshot, or photo data. <br>
Mitigation: Avoid granting broad local file or execution access unless OCR or service features are required and the processed data is appropriate for that environment. <br>
Risk: The skill runs local scripts and depends on local runtime binaries. <br>
Mitigation: Require explicit confirmation for first-time execution and prefer a sandbox, virtual machine, or container in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/con2000us/zentable) <br>
- [Pinned runtime release](https://github.com/con2000us/zenTable/releases/tag/skillhub-zentable-beta-2026-03-01) <br>
- [Runtime repository](https://github.com/con2000us/zenTable) <br>
- [Support issues](https://github.com/con2000us/zenTable/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Guidance] <br>
**Output Format:** [PNG table images with optional TXT side output and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports CSS and PIL rendering paths, sorting, filtering, pagination, themes, and threshold highlighting.] <br>

## Skill Version(s): <br>
0.9.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
