## Description: <br>
Analyzes pet monitoring videos for anxiety, howling, loneliness, and related behaviors, then reports whether soothing actions such as calming audio or laser-toy activation should be triggered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet owners and smart home developers use this skill to evaluate uploaded or URL-based pet monitoring videos, identify likely anxiety or isolation signals, and review analysis or historical soothing-trigger reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive credentials and asks for an open-id that may be a phone number or user identifier. <br>
Mitigation: Do not use an API key as the open-id, avoid providing a phone number unless the backend service is trusted, and prefer credentials that can be revoked. <br>
Risk: Pet videos and report queries are sent to remote cloud endpoints for analysis and history retrieval. <br>
Mitigation: Upload only videos and report data that are acceptable to share with the listed service, and review the service's account, storage, and retention behavior before production use. <br>
Risk: Evidence reports suspicious identity handling, remote report access, and silent local token persistence. <br>
Mitigation: Review the skill carefully before installing, use an isolated account for evaluation, and prefer a revised release that separates credentials from identity and clearly discloses token storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-pet-calming-trigger-analysis) <br>
- [Pet calming trigger API reference](artifact/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown reports and tables with JSON analysis content and command-line invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local video path or public video URL plus an open-id/user identifier; may also use an API key, API URL, output path, and detail level.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
