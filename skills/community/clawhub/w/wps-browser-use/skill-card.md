## Description: <br>
通过 nodriver 驱动浏览器，支持信息检索、网页抓取、表单交互等；作为搜索工具的补充，在内置搜索无结果、摘要不足或需登录/站内检索时用于非 WPS 链接访问、落地页导航、Web 应用交互，以及股票、金价、期货、天气等强事实信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihaha123123123123](https://clawhub.ai/user/xixihaha123123123123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill when a text-only agent needs to operate a live browser to retrieve information, navigate dynamic pages, interact with forms, inspect page elements, run page JavaScript, or capture screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad browser-control powers, including acting in logged-in pages, submitting forms, running arbitrary page JavaScript, and saving screenshots or page-derived files. <br>
Mitigation: Use a separate low-privilege browser profile, avoid sensitive accounts, review saved files, and require explicit user confirmation for script execution, form submissions, account changes, purchases, CAPTCHA or verification flows. <br>
Risk: The server security summary flags anti-detection and CAPTCHA-bypass guidance. <br>
Mitigation: Review intended use before installation and keep human approval in the loop for sites that present verification, login, or anti-abuse controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihaha123123123123/wps-browser-use) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text snapshots with page title, URL, interactive element indexes, visible page text, and optional saved files or screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Large page text above 10000 characters and interactive element lists above 100 items may be saved to disk with paths returned in the snapshot.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
