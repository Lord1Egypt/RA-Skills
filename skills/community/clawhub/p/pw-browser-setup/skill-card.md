## Description: <br>
PW Browser Setup installs, checks, and verifies a Playwright plus Chromium browser automation environment with optional Xvfb-backed headed browser support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to prepare a local or server workspace for Playwright browser automation, confirm host compatibility, install Chromium dependencies, and capture a verification screenshot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup scripts can make broad host changes by installing system packages, global npm packages, and browser binaries. <br>
Mitigation: Run the skill only in a disposable workspace, VM, or container where those changes are acceptable. <br>
Risk: Browser verification launches Chromium with relaxed sandbox-related arguments and can run in headed mode through Xvfb. <br>
Mitigation: Avoid running the browser as root and prefer an isolated environment with no sensitive local data. <br>
Risk: The verification script accepts a screenshot path and the documented Feishu commands can send screenshots to an external service. <br>
Mitigation: Use trusted screenshot paths only and review screenshots before intentionally sending them through Feishu. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxn/pw-browser-setup) <br>
- [Baidu verification target](https://www.baidu.com) <br>
- [Feishu image upload API](https://open.feishu.cn/open-apis/im/v1/images) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create helper shell scripts, install npm packages, download browser binaries, install system packages, and write verification screenshots when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
