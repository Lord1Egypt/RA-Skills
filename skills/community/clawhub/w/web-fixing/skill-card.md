## Description: <br>
Guides agents through structured diagnosis and repair of web and frontend issues, including UI bugs, CSS problems, responsive layout failures, JavaScript errors, broken interactions, and post-generation page checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aqbjqtd](https://clawhub.ai/user/aqbjqtd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to diagnose frontend defects, form root-cause hypotheses, implement minimal fixes, and verify results across browsers, screen sizes, console output, and performance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to modify frontend project files while debugging. <br>
Mitigation: Give write access only in projects intended for modification, review proposed code changes, and verify fixes with the skill's browser, console, responsive, and regression checks. <br>
Risk: Optional npm or npx setup commands may install project dependencies or browser test tooling. <br>
Mitigation: Run dependency installation only in trusted project environments and review package changes before committing them. <br>


## Reference(s): <br>
- [Web Fixing Skill Page](https://clawhub.ai/aqbjqtd/web-fixing) <br>
- [Detailed Workflow](references/workflows.md) <br>
- [Repair Checklist](references/checklist.md) <br>
- [Repair Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose code edits, browser checks, Playwright setup commands, Lighthouse checks, or dependency installation guidance depending on the project.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
