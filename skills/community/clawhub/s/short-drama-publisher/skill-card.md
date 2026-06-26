## Description: <br>
Automates a short drama publishing workflow that downloads MoboBoost content, identifies highlight moments, clips 15-second vertical videos with text overlays, and publishes them to Facebook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ye4wzp](https://clawhub.ai/user/ye4wzp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and social media automation developers use this skill to prepare and publish short drama promotion clips from MoboBoost sources to Facebook. It supports automated downloading, highlight selection, vertical clipping, scheduling, and publishing workflows where credentials and content rights are managed by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses exported MoboBoost and Facebook cookies, which can expose account access if mishandled. <br>
Mitigation: Keep cookie files out of source control, provide them only after reviewing the implementation, and rotate or re-export credentials when access changes. <br>
Risk: The workflow can publish videos to Facebook unattended, creating account, brand, and content-rights risk. <br>
Mitigation: Add a manual approval step before posting and verify rights to use MoboBoost content before enabling scheduled publishing. <br>
Risk: The security review flags the release as suspicious because it combines automated posting with cookie-based authentication and limited user-control safeguards. <br>
Mitigation: Inspect or provide the missing scripts yourself and avoid enabling the cron job until the full workflow behavior is trusted. <br>


## Reference(s): <br>
- [MoboBoost content portal](https://ckoc.cdreader.com) <br>
- [ClawHub skill page](https://clawhub.ai/ye4wzp/short-drama-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent through video download, highlight detection, clipping, Facebook publishing, and cron-style scheduling steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
