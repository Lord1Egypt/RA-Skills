## Description: <br>
Automates Toutiao creator publishing workflows for micro-posts and articles, including topic selection, drafting, image handling, browser upload, and publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wtl01](https://clawhub.ai/user/wtl01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, social media operators, and marketing teams use this skill to prepare and publish Toutiao micro-posts and articles through an authenticated browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post or schedule real Toutiao content from the user's logged-in account. <br>
Mitigation: Require preview and explicit user confirmation before each publish or scheduled post. <br>
Risk: Broad triggers could activate the publishing workflow when the user intended only drafting or planning. <br>
Mitigation: Narrow activation to Toutiao-specific publishing requests and confirm the target action before browser automation starts. <br>
Risk: Automated operation may affect a production social-media account. <br>
Mitigation: Use a dedicated or test account where possible and stop for manual login whenever the browser reaches an authentication page. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wtl01/toutiao-article-publish) <br>
- [Publisher Profile](https://clawhub.ai/user/wtl01) <br>
- [Toutiao Micro-post Publish Page](https://mp.toutiao.com/profile_v4/weitoutiao/publish) <br>
- [Toutiao Article Publish Page](https://mp.toutiao.com/profile_v4/graphic/publish) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with browser automation commands and publication drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled publishing cadence, browser upload steps, content drafts, image handling instructions, and post-publication status checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
