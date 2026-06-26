## Description: <br>
Automates browsing the X home timeline to find technology and BTC-related posts and publish short contextual replies without liking posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, or social media account owners use this skill to have an agent select technology or BTC-related posts from an authenticated X account and publish concise, topic-matched replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous public replies from a logged-in X account can publish unwanted or reputationally risky comments. <br>
Mitigation: Use a dedicated low-risk account and require draft review before sending replies. <br>
Risk: Optional follow-up tracking can retain interaction history. <br>
Mitigation: Enable follow-up tracking only when needed and keep a clear deletion process for stored state. <br>
Risk: The skill relies on text and DOM extraction, so image-only post context may be missed. <br>
Mitigation: Skip posts whose meaning depends on images or other unavailable media context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mars82311111/x-comment) <br>
- [X home timeline](https://x.com/home) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status report with generated X reply text and browser-action guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Replies are designed to stay within 280 characters and may be posted from a logged-in X account without per-reply approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
