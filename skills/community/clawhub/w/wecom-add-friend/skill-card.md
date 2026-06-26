## Description: <br>
Automates adding WeCom contacts in the Windows WeCom PC client from batches of phone numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whailon](https://clawhub.ai/user/whailon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or operators with authorized WeCom outreach workflows use this skill to parse phone-number lists and run Windows GUI automation that sends friend requests through the WeCom PC client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bulk-send WeCom friend requests through the user's logged-in corporate account. <br>
Mitigation: Use only authorized phone lists and an account where bulk outreach is permitted; require explicit user confirmation before sending requests. <br>
Risk: Unsafe GUI fallbacks may click or type in the wrong window or screen location. <br>
Mitigation: Run only when the WeCom window is visible and positively identified; prefer a version that fails closed when the target window cannot be verified. <br>
Risk: Rapid additions may trigger platform restrictions or anti-abuse controls. <br>
Mitigation: Use conservative add intervals, follow WeCom policy, and stop immediately if verification, captcha, or restriction signals appear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whailon/wecom-add-friend) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and concise execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, Python, the bundled bin/wecom_auto_add.py file, and a visible logged-in WeCom PC client.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
