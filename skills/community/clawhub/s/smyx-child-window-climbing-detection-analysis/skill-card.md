## Description: <br>
Analyzes window or balcony camera images and video to detect child climbing, leaning, railing-crossing, or window-edge gripping behavior and return structured alerts and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Families, childcare operators, and safety-system developers can use this skill to submit fixed-camera footage of window or balcony areas for child fall-risk detection and to retrieve current or historical warning reports. The skill is an auxiliary monitoring aid and does not replace adult supervision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive child and home monitoring footage, snapshots, and report history may be sent to lifeemergence.com cloud services. <br>
Mitigation: Use only with guardian consent, upload the minimum footage needed, and verify retention, access-control, and deletion practices before deployment. <br>
Risk: The skill silently creates or reuses identity data and stores service tokens locally for analysis and report history. <br>
Mitigation: Review identity and token storage before installation, restrict workspace access, and rotate or clear credentials when users or deployments change. <br>
Risk: Report export links and snapshot URLs can reveal sensitive child or home information if shared too broadly. <br>
Mitigation: Limit access to report links, avoid posting them in shared channels, and confirm whether generated links expire or can be revoked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-child-window-climbing-detection-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [API interface reference](artifact/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-formatted structured reports with optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include warning levels, confidence values, event timestamps, snapshot URLs, report export links, and historical report lists.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact/SKILL.md reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
