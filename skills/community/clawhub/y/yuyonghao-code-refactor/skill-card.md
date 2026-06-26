## Description: <br>
Code Refactor analyzes JavaScript code quality issues, proposes refactoring plans, and can apply selected changes with dry-run, rollback, and test validation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect JavaScript files for maintainability issues, generate refactoring plans, preview changes, apply supported edits, and validate results with tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applied refactoring can modify local project files and may produce incorrect or incomplete changes. <br>
Mitigation: Run on trusted codebases under version control, start with dry-run previews, and review generated changes before using apply mode. <br>
Risk: Validation can run project test commands with the user's local permissions. <br>
Mitigation: Review the configured test command and run validation only in projects and environments where those commands are trusted. <br>


## Reference(s): <br>
- [Code Refactor on ClawHub](https://clawhub.ai/yuyonghao-123/yuyonghao-code-refactor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON analysis results, Markdown reports, CLI output, and file changes when apply mode is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews, diff-style reports, backup-based rollback for applied edits, configurable analysis thresholds, and project test execution during validation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
