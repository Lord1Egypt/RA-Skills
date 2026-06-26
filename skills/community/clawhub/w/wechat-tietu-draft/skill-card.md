## Description: <br>
WeChat Tietu Draft helps an agent create simplified WeChat Official Account image-text draft posts from UTF-8 .txt files through a logged-in Chrome session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[punkin6](https://clawhub.ai/user/punkin6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation developers use this skill to turn simple UTF-8 text files into WeChat Official Account tietu-style drafts for image-led posts. It is intended for fast draft creation after the user has prepared Chrome and a logged-in WeChat Official Account session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a logged-in WeChat Official Account session. <br>
Mitigation: Use a dedicated Chrome profile and review every generated draft before publishing. <br>
Risk: The skill can force-kill local processes on the configured Chrome debugging port. <br>
Mitigation: Run it on a dedicated port and avoid sharing the machine or port with unrelated browser automation. <br>
Risk: Local logs, screenshots, or temporary Chrome profile directories may contain sensitive WeChat session details. <br>
Mitigation: Delete generated logs, screenshots, and temporary profile directories after use. <br>


## Reference(s): <br>
- [WeChat Official Account Platform](https://mp.weixin.qq.com) <br>
- [ClawHub skill page](https://clawhub.ai/punkin6/wechat-tietu-draft) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal status messages, logs, and WeChat draft content created from text input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts UTF-8 .txt input and reports staged execution status for environment setup, login readiness, draft creation, and failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
