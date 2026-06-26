## Description: <br>
Automatically reads the current day's video and title file from a configured local folder and publishes the content to a logged-in Xiaohongshu account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weishuai34-bit](https://clawhub.ai/user/weishuai34-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators or operators use this skill to automate posting prepared daily video and caption content to Xiaohongshu. It is intended for users who already maintain a logged-in Chrome session and want repeatable publishing from a fixed local content folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish to a live Xiaohongshu account without a final confirmation step. <br>
Mitigation: Review the dated video and title file before invoking the skill and use it only with accounts where direct publishing is intended. <br>
Risk: The skill depends on a Chrome debugging session connected to an authenticated browser profile. <br>
Mitigation: Use a dedicated Chrome profile where possible and close Chrome debugging after the publishing task is complete. <br>
Risk: Broad trigger phrases can initiate account-changing behavior. <br>
Mitigation: Avoid configuring broad or ambiguous invocations for this skill in shared or multi-user agent environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weishuai34-bit/xiaohongshu-publish-auto) <br>
- [Publisher profile](https://clawhub.ai/user/weishuai34-bit) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, browser automation] <br>
**Output Format:** [Console status text with screenshot files generated during the publishing flow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes directly to a live Xiaohongshu account through a logged-in Chrome session when invoked.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
