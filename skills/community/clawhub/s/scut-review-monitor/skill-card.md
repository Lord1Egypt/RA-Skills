## Description: <br>
Check or monitor the SCUT thesis blind-review status page through the graduate portal and refresh cookies through a local Python helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songxf1024](https://clawhub.ai/user/songxf1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to help SCUT graduate students check the thesis blind-review status page, refresh portal cookies through a local helper, and monitor watched status text for changes when continuous monitoring is explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores university portal session data locally. <br>
Mitigation: Protect or delete cookies.json after use and avoid sharing the skill directory or generated login artifacts. <br>
Risk: Login QR codes may be uploaded to a third-party image host by default. <br>
Mitigation: Set image_upload.enabled to false unless uploading the QR code to the configured host is explicitly intended. <br>
Risk: Notification endpoints and keys can expose portal status or credentials if configured carelessly. <br>
Mitigation: Use only trusted notification endpoints, keep notification keys private, and remove placeholder values before use. <br>
Risk: Continuous monitoring can create a long-lived local process against the portal. <br>
Mitigation: Run monitor mode only when explicitly requested and use an external supervisor if persistent operation is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songxf1024/scut-review-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/songxf1024) <br>
- [SCUT graduate affairs portal](https://yjsjw-443.webvpn.scut.edu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and plain-text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local cookies and login QR-code artifact files during login workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
