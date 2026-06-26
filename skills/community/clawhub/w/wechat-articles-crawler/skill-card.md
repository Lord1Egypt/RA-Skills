## Description: <br>
Locally crawls recent articles from a WeChat public account from a supplied article link and saves Markdown, HTML, and articles.json outputs for later analysis or archiving. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[DazhuangJammy](https://clawhub.ai/user/DazhuangJammy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and local automation agents use this skill to authenticate to a WeChat public-platform account, fetch recent articles from a target public account, and prepare local files for corpus building, style analysis, fact checking, or archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler uses persistent local WeChat login state and QR-code login artifacts, which can expose account access if copied or shared. <br>
Mitigation: Run only on a trusted local machine; do not share .playwright-profile, login_artifacts, cookies, tokens, or QR codes, and run clear-login before handing off the project or machine. <br>
Risk: The skill performs local browser automation against WeChat using the user's public-platform account. <br>
Mitigation: Confirm the target article, intended batch size, platform rules, and authorization before running a fetch. <br>
Risk: The launcher can create a virtual environment and install runtime dependencies before execution. <br>
Mitigation: Review requirements and installation behavior first when using a hardened or reproducible environment. <br>


## Reference(s): <br>
- [Crawler documentation](references/抓取器说明.md) <br>
- [WeChat public platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, HTML, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status/output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated article files are written locally under the configured output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
