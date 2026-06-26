## Description: <br>
Fetches WeChat Official Account articles from mp.weixin.qq.com with Playwright and returns the title, body text, and final URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[write31bug](https://clawhub.ai/user/write31bug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content workflows use this skill to extract article text from WeChat Official Account links for archiving, note-taking, research collection, writing reference, or content repurposing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens a user-supplied WeChat article URL in a local headless browser. <br>
Mitigation: Use trusted mp.weixin.qq.com article links and run the skill in an isolated local environment when processing untrusted content. <br>
Risk: The skill requires npm dependencies and an installed Chromium browser. <br>
Mitigation: Install dependencies from trusted registries, keep Playwright and Chromium updated, and scan the package before deployment. <br>
Risk: URL validation is basic. <br>
Mitigation: Restrict execution to expected WeChat article links and review the resolved final URL for sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/write31bug/wechat-mp-fetch) <br>
- [GitHub Project Homepage](https://github.com/write31bug/wechat-mp-fetch) <br>
- [npm Package](https://www.npmjs.com/package/wechat-mp-fetch) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown returned by a command-line Node.js script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes success status, extracted title, extracted content, final URL, or an error message.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
