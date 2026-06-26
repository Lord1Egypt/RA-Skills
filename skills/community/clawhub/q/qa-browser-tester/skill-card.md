## Description: <br>
Launches a real headless Chromium browser to perform end-to-end QA testing of a web application by navigating pages, clicking controls, filling forms, and reporting results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[melnikdavid](https://clawhub.ai/user/melnikdavid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to automate browser-based checks against authorized web applications, including navigation, button behavior, forms, screenshots, and a final QA report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can click controls, submit forms, create accounts, and trigger workflows when pointed at a target site. <br>
Mitigation: Run it only against authorized staging or test environments, or against production only with explicit approval for automated interaction. <br>
Risk: Screenshots captured during QA can expose sensitive page content if saved or published in an unsafe location. <br>
Mitigation: Store screenshots in a disposable local directory and review them before sharing or moving them to a web-served path. <br>
Risk: The setup steps install browser automation dependencies and run Chromium in a server or container environment. <br>
Mitigation: Review install commands before execution and prefer a disposable container or isolated test host. <br>


## Reference(s): <br>
- [Docker Setup Reference](references/docker-setup.md) <br>
- [Test Phases - Full QA Script](references/test-phases.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/melnikdavid/qa-browser-tester) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with shell commands, Python code, test findings, and screenshot file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshots to a local temporary directory during test execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
