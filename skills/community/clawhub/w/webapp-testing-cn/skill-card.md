## Description: <br>
Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to test local static and dynamic web applications with Playwright, inspect rendered pages, capture screenshots and console logs, and manage local server lifecycles during browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server commands are executed locally when using the lifecycle helper. <br>
Mitigation: Review each --server command before running it and avoid passing generated or untrusted strings into that option. <br>
Risk: Screenshots, DOM dumps, and console logs may contain sensitive application data. <br>
Mitigation: Store captured outputs carefully and redact or delete them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/webapp-testing-cn) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [with_server.py](artifact/scripts/with_server.py) <br>
- [element_discovery.py](artifact/examples/element_discovery.py) <br>
- [static_html_automation.py](artifact/examples/static_html_automation.py) <br>
- [console_logging.py](artifact/examples/console_logging.py) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots, DOM inspection output, and console log files when the generated Playwright automation is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
