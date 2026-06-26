## Description: <br>
Checks Huawei AppGallery for the current version of the 一日记账 app and returns the version, source link, and check timestamp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taobaoaz](https://clawhub.ai/user/taobaoaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation agents use this skill to answer questions about the latest 一日记账 app version by checking Huawei AppGallery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Playwright and Chromium to open a public Huawei AppGallery page when triggered. <br>
Mitigation: Install and run it only in an environment where browser automation and outbound access to the listing are expected, and narrow trigger phrases or confirm intent for automated chats. <br>
Risk: The version check depends on the AppGallery page content and can fail or return a missing version if the page or selector changes. <br>
Mitigation: Treat failed checks as transient, review the returned URL and timestamp, and update the selector if AppGallery changes its page structure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taobaoaz/yiri-app-monitor) <br>
- [Huawei AppGallery listing for 一日记账](https://appgallery.huawei.com/app/detail?id=com.ericple.onebill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Concise text summary or JSON object with app name, app ID, version, URL, and timestamp.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, Playwright, and Chromium; may return an error field if the page check fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
