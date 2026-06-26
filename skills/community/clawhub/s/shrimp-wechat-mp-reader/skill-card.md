## Description: <br>
Reads WeChat Official Account article pages from mp.weixin.qq.com URLs and extracts the page title and body text through a local Playwright browser flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyunting555](https://clawhub.ai/user/wuyunting555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when a user provides a WeChat Official Account article URL and asks to read, extract, quote, or summarize the article content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and running the skill can install npm dependencies and download a Playwright Chromium browser locally. <br>
Mitigation: Install only in an environment where local npm dependency installation and browser downloads are acceptable. <br>
Risk: The skill opens user-provided WeChat article links and needs network access from the local browser session. <br>
Mitigation: Use intended mp.weixin.qq.com article URLs and prefer a sandboxed workspace when the host environment has sensitive network access. <br>
Risk: WeChat risk-control pages, missing browser installation, or shell pages can produce empty or non-article output. <br>
Mitigation: Treat success as requiring a meaningful title and bodyText from the requested article, and report failures instead of summarizing empty output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuyunting555/shrimp-wechat-mp-reader) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON object with title and bodyText fields, with concise Markdown-style result reporting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a mp.weixin.qq.com article URL and a local Node.js environment that can install npm dependencies and Playwright Chromium; extracted body text is capped at 20000 characters by the artifact script.] <br>

## Skill Version(s): <br>
0.1.2 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
