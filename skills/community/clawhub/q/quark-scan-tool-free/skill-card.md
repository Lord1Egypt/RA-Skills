## Description: <br>
夸克扫描-免费版 helps agents guide single-image document scanning and enhancement tasks such as improving clarity, removing handwriting, watermarks, shadows, screen patterns, and background color, and extracting sketches or line art. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal users, students, and creative users can use this skill to prepare single images for Quark scan enhancement workflows, including exam paper cleanup, document archiving, old-photo improvement, and line-art extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The trigger language and permissions are broader than the stated single-image scanning purpose. <br>
Mitigation: Use the skill only for explicit single-image scan or enhancement requests and narrow trigger language before routine deployment. <br>
Risk: Documents or images may be uploaded to Quark's service during processing. <br>
Mitigation: Avoid processing arbitrary or sensitive files unless the user has accepted the upload and data-handling implications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/quark-scan-tool-free) <br>
- [Quark Scan business API](https://scan.quark.cn/business) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides single-image processing and describes returned status, result paths, logs, and errors.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
