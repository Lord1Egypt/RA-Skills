## Description: <br>
Automatically generate daily or weekly work reports from Git commits, calendar events, and task lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1989tianlong](https://clawhub.ai/user/1989tianlong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to create concise work reports from recent repository activity, with configurable date ranges and Chinese or English output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted project configuration or date arguments could cause unintended local shell commands while collecting Git logs. <br>
Mitigation: Install and run only in trusted project directories, review any .reportrc.json before execution, and replace shell-string Git execution with argument-based calls before use on untrusted repositories. <br>
Risk: The documentation describes calendar and task sources, but the reviewed implementation behaves as a Git-based report generator. <br>
Mitigation: Treat generated reports as Git commit summaries unless the maintainer updates the implementation and documentation to match. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1989tianlong/ytlong-daily-report) <br>
- [Publisher Profile](https://clawhub.ai/user/1989tianlong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report text printed to stdout and saved as a report-<date>.md file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports today, week, and custom date ranges; output language and statistics can be configured through .reportrc.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
