## Description: <br>
Generates Xiaohongshu-style post assets including title, body copy, hashtags, a cover prompt, and posting strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArthuronAI](https://clawhub.ai/user/ArthuronAI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators and marketers use this skill to draft Xiaohongshu-style posts from a topic, including copy, hashtags, a cover-image prompt, and posting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the topic and generated context to external services for content generation, keyword lookup, and billing. <br>
Mitigation: Avoid sensitive topics or confidential campaign details, and use scoped OpenAI and SkillPay credentials. <br>
Risk: Each execution can incur a 0.05 USDT SkillPay charge, and SKILLPAY_ENDPOINT can change the billing destination. <br>
Mitigation: Confirm the per-call cost before use, and keep SKILLPAY_ENDPOINT unset unless the endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ArthuronAI/xhs-viral-post) <br>
- [Datamuse keyword API endpoint](https://api.datamuse.com/words) <br>
- [SkillPay billing endpoint](https://api.skillpay.me/v1/charges) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON object with title, content, hashtags, coverPrompt, and strategy] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a topic input; billing succeeds before content generation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact SKILL.md and package.json report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
