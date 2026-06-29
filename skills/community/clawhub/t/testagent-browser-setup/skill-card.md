## Description: <br>
Sets up a new OpenClaw environment with Chromium, browser dependencies, Chinese fonts, a local Chrome CDP launcher, Playwright MCP registration, and optional browser-use tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyin717](https://clawhub.ai/user/wangyin717) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to initialize browser automation in new OpenClaw environments, including Chromium discovery or download, CDP launch setup, Playwright MCP registration, font setup, and practical browser-tool selection guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent CDP access can provide broad control over a browser session. <br>
Mitigation: Keep CDP bound to local-only access and start it only for intentional browser automation work. <br>
Risk: Optional browser-use installation pulls and enables additional third-party tooling with proxy, tunnel, cloud browser, and session capabilities. <br>
Mitigation: Skip the optional installer unless the publisher and source are trusted and those capabilities are required. <br>
Risk: Profile and session reuse can expose credentials or authenticated browser state. <br>
Mitigation: Avoid reusing a personal Chrome profile unless explicitly needed, and treat credentials entered through the examples as sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyin717/skills/testagent-browser-setup) <br>
- [Artifact setup guide](artifact/SKILL.md) <br>
- [Artifact browser tools guide](artifact/TOOLS.md) <br>
- [browser-use project](https://github.com/browser-use/browser-use) <br>
- [browser-use CLI installer](https://browser-use.com/cli/install.sh) <br>
- [WenQuanYi Micro Hei font source](https://github.com/anthonyfok/fonts-wqy-microhei/raw/master/wqy-microhei.ttc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, JSON, and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local setup files and launch browser automation helpers when users run the provided commands.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata; artifact frontmatter reports 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
