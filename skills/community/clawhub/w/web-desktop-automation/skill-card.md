## Description: <br>
Use when the user wants browser automation, web scraping, form filling, clicking, or desktop GUI automation, including mixed workflows that move between web pages and local applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lurui808](https://clawhub.ai/user/lurui808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through browser automation, desktop GUI automation, and mixed workflows that move files or state between websites and local applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This is a disclosed browser and desktop automation helper, but it gives an agent powerful controls that users should apply only to specific tasks. <br>
Mitigation: Use the skill only for specific tasks, keep instructions narrow, and review planned actions before execution. <br>
Risk: Automation may perform sensitive actions such as logins, submissions, uploads, downloads, purchases, deletions, account changes, or edits to important local files. <br>
Mitigation: Install only if you want agents to control browsers and desktop apps. Keep tasks narrowly specified, review any dependency versions in your environment, and require explicit confirmation before logins, submissions, uploads, downloads, purchases, deletions, account changes, or edits to important local files. <br>


## Reference(s): <br>
- [Browser Workflows](references/browser-workflows.md) <br>
- [Desktop Workflows](references/desktop-workflows.md) <br>
- [Mixed Flows](references/mixed-flows.md) <br>
- [Real-World Mixed Example](references/mixed-example.md) <br>
- [Dependencies and Installation](references/dependencies.md) <br>
- [Minimal Python Requirements](requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python code templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Playwright and PyAutoGUI automation scripts or phased browser and desktop workflow plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
