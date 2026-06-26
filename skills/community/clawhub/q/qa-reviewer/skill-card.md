## Description: <br>
Provides code review, test execution, issue tracking, and quality report workflows for C++, Python, and JavaScript projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SamuelPang](https://clawhub.ai/user/SamuelPang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and QA engineers use this skill to review local project code, discover and run tests, track quality issues, and produce Markdown review and test reports before acceptance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included shell scripts scan local project files and the test script may execute the target project's build and test commands. <br>
Mitigation: Inspect the scripts before use and run them only on trusted codebases or in an isolated workspace. <br>
Risk: Generated review and test reports may be incomplete or misleading if treated as final QA decisions. <br>
Mitigation: Use generated reports as review aids and have a qualified reviewer verify findings, test results, and acceptance status. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SamuelPang/qa-reviewer) <br>
- [Skill Documentation](SKILL.md) <br>
- [Workflow Documentation](docs/workflow.md) <br>
- [Checklist Documentation](docs/checklist.md) <br>
- [Best Practices Documentation](docs/best_practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports, Markdown templates, shell command guidance, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When scripts are run, they may create CODE_REVIEW_*.md and TEST_RESULT_*.md files in the target project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
