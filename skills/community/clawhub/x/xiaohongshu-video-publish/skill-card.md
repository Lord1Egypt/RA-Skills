## Description: <br>
Guides an agent through publishing video posts on the Xiaohongshu creator web platform with browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnyxu820](https://clawhub.ai/user/Johnnyxu820) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and operators use this skill to publish prepared video notes to a logged-in Xiaohongshu creator account, including upload, title, topic tags, cover selection, location selection, publish confirmation, and post-publish verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content from the currently logged-in Xiaohongshu account. <br>
Mitigation: Require manual confirmation of the account, video, title, body, tags, cover, and final publish action before posting. <br>
Risk: The skill includes a fixed location selection of Suzhou Center. <br>
Mitigation: Confirm, remove, or change the location before publishing unless that location is intentionally required. <br>
Risk: Repeated execution could duplicate a published video note. <br>
Mitigation: Check local logs and the Xiaohongshu content management page before retrying, and stop once publishing succeeds. <br>


## Reference(s): <br>
- [Xiaohongshu creator video publish page](https://creator.xiaohongshu.com/publish/publish?source=official&from=tab_switch&target=video) <br>
- [ClawHub skill page](https://clawhub.ai/Johnnyxu820/xiaohongshu-video-publish) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, browser automation steps] <br>
**Output Format:** [Markdown instructions and checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw Chrome extension access and a logged-in Xiaohongshu creator account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
