## Description: <br>
Recognizes human postures in images or videos, including fall and abnormal-posture detection, and returns structured monitoring reports for security and elder-care use cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit surveillance or care-setting media for human posture classification, fall detection, abnormal-posture alerts, and report/history retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted videos, image data, URLs, generated identity, report history, and locally stored session tokens are handled through the Life Emergence cloud service. <br>
Mitigation: Use only when that cloud service is trusted for the media and account-linked data; avoid sensitive surveillance or elder-care footage without consent and a retention plan. <br>
Risk: The skill silently creates or reuses user identity and can query cloud report history without clear user-facing control. <br>
Mitigation: Install only in trusted workspaces, protect local workspace data, and review account and history access before deployment. <br>
Risk: The authoritative security verdict is suspicious. <br>
Mitigation: Review carefully before installing and scan the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-human-posture-recognition-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON text, with shell command examples and optional saved result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can query cloud-hosted report history and can save analysis output to a local file when requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter declares 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
