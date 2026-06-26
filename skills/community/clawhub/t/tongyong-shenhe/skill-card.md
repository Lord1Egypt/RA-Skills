## Description: <br>
A configurable content moderation skill for d.php-based admin sites that applies local rules and can optionally use an approved moderation API for a second review pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wulooongcha](https://clawhub.ai/user/wulooongcha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal moderation operators and site teams use this skill to configure and run automated review workflows for d.php-based backend sites. It reviews pending content with configurable rules, supports dry-run checks, and can submit approve or reject decisions when live mode is used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires admin credentials, TOTP seeds, and optional API keys. <br>
Mitigation: Use a least-privilege account, store config.json as a secret, and never commit or share TOTP seeds or API keys. <br>
Risk: Live mode can change moderation decisions on production backend sites. <br>
Mitigation: Run dry-run first, limit batches and modules, review rule changes carefully, and enable live submission only after the output matches policy expectations. <br>
Risk: External decision files and optional API integration can affect approve or reject outcomes. <br>
Mitigation: Use trusted decision files only and enable the external API only when the endpoint and data-handling policy are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wulooongcha/tongyong-shenhe) <br>
- [Publisher profile](https://clawhub.ai/user/wulooongcha) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, Python code, and runtime text logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce pending review JSON files and submit moderation decisions when configured for live operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
