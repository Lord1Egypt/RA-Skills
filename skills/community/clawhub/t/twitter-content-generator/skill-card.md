## Description: <br>
AI-powered Twitter/X content generator. Generate engaging tweets, threads, and content strategies using Sloan agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icepopma](https://clawhub.ai/user/icepopma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, marketers, and social media managers use this skill to generate Twitter/X tweets, multi-post threads, and content strategies with configurable style, tone, hashtags, and emojis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The billing flow is inconsistent and can make real SkillPay calls with an embedded merchant key. <br>
Mitigation: Confirm which merchant key and account are used before generation, use test mode for evaluation, and avoid running npm test with real payment credentials. <br>
Risk: Server security guidance flags package-lock provenance issues. <br>
Mitigation: Verify dependency sources and lockfile integrity before installing or running the skill in a trusted environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icepopma/twitter-content-generator) <br>
- [Publisher profile](https://clawhub.ai/user/icepopma) <br>
- [GitHub support repository](https://github.com/icepopma/twitter-content-generator) <br>
- [SkillPay payment provider](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text output with generated social posts and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate a single tweet, a numbered thread, or a 7-day content strategy; normal runs may initiate a 0.002 USDT SkillPay charge before generation.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata and SKILL.md frontmatter; package.json reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
