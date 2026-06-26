## Description: <br>
Drafts Zhihu answers by selecting eligible hot questions, calling a documented AI endpoint, and saving generated Chinese answers as drafts without publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joly123456](https://clawhub.ai/user/joly123456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to prepare Zhihu draft answers from hot or keyword-filtered topics while keeping manual control over account login and final publishing. <br>

### Deployment Geography for Use: <br>
Global, subject to Zhihu account access and service availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a Chrome session logged into Zhihu. <br>
Mitigation: Use a dedicated browser profile when possible, disable browser host control after use, and review all drafts before publishing. <br>
Risk: Selected Zhihu page context is sent to the documented third-party AI endpoint. <br>
Mitigation: Use a revocable API key, avoid sensitive topics or private content, and verify the endpoint and model configuration before running. <br>
Risk: Generated answers may be incorrect, unsafe, or unsuitable for the account holder's voice. <br>
Mitigation: Keep the workflow draft-only, require manual review before publishing, and rely on the skill's validation and safety skip rules as a first-pass filter. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joly123456/zhihu-draft-writer) <br>
- [Publisher Profile](https://clawhub.ai/user/joly123456) <br>
- [Setup](artifact/references/setup.md) <br>
- [Runtime Options](artifact/references/runtime-options.md) <br>
- [Answer Generation Prompt](artifact/references/answer-generation.md) <br>
- [Answer Schema](artifact/references/answer-schema.json) <br>
- [Manual Test Checklist](artifact/references/manual-test-checklist.md) <br>
- [Zhihu Hot List](https://www.zhihu.com/hot) <br>
- [zhihuiapi Chat Completions Endpoint](https://cc.zhihuiapi.top/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status reports, JSON API payloads, shell commands, and drafted Chinese answer text saved through the browser.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates draft-only Zhihu answers, appends local deduplication history, and reports successes, skips, and failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
