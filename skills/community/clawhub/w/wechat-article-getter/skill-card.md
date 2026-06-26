## Description: <br>
Extracts full text and metadata from WeChat Official Account article URLs for reading, summarization, analysis, or archiving, using headless Chromium with a mirror-search fallback when browser rendering is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PPPPanda](https://clawhub.ai/user/PPPPanda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a user provides an mp.weixin.qq.com article link and needs the article text or metadata for summarization, analysis, or archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python packages and a Chromium browser binary during setup or first run. <br>
Mitigation: Review and approve setup before running, prefer pinned preinstalled dependencies, and run the skill in an isolated environment. <br>
Risk: Fetching articles contacts WeChat and mirror or aggregator sites, which may disclose article URLs or query terms externally. <br>
Mitigation: Use only with URLs safe to send to those services, and ask before enabling mirror fallback for sensitive links. <br>
Risk: The evidence security review notes undeclared permissions and recommends separating setup from runtime. <br>
Mitigation: Prefer a release that declares permissions clearly and keeps dependency installation as an explicit setup step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PPPPanda/wechat-article-getter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [JSON by default, with optional Markdown or plain text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write extracted article output to a user-specified file path; includes title, author, publish time, content, word count, source, URL, and error fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
