## Description: <br>
AI-powered automated QA for web apps. Smoke tests, accessibility, visual regression. Works with Cursor, Claude, ChatGPT, Copilot. Vibe-coding ready. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NextFrontierBuilds](https://clawhub.ai/user/NextFrontierBuilds) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and QA engineers use this skill to run browser-based smoke tests, accessibility checks, visual regression checks, scripted web test suites, and QA reports for web applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted test inputs or report options can reach unsafe shell commands and potentially run local commands. <br>
Mitigation: Install and run only with trusted test suites, URLs, selectors, report paths, and company/output values until shell execution is replaced with argument-vector execution and input validation. <br>
Risk: Screenshots, console logs, generated reports, and authenticated browser sessions may expose sensitive application data. <br>
Mitigation: Treat QA artifacts and browser sessions as sensitive, restrict access to outputs, and avoid running the skill against untrusted or unnecessary authenticated sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NextFrontierBuilds/web-qa-bot) <br>
- [GitHub project page](https://github.com/NextFrontierBuilds/web-qa-bot) <br>
- [npm package](https://www.npmjs.com/package/web-qa-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON, Files] <br>
**Output Format:** [Markdown guidance with CLI commands, YAML/JSON test suite examples, and generated Markdown, PDF, or JSON QA reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots, console logs, test reports, and browser automation output that can contain sensitive application data.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
