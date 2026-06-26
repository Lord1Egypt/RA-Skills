## Description: <br>
Generates file-type-specific code review checklists covering security, performance, style, and testing best practices for pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and reviewers use this skill inside git repositories to produce pull request review checklists, findings summaries, and reusable review templates. It helps make security, performance, style, and test coverage review steps more consistent across common programming languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Bash script reads changed files and diffs in the local git repository. <br>
Mitigation: Run it only in the intended repository and review the selected base branch, head ref, and file filter before execution. <br>
Risk: The --output-file option writes the generated report or template to a provided path. <br>
Mitigation: Use explicit, reviewed output paths and avoid overwriting important files. <br>
Risk: The --files option is handled as a grep regular expression filter rather than a shell glob. <br>
Mitigation: Use regex-compatible patterns or omit the filter when unsure about the intended review scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryudi84/sovereign-code-review-helper) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, text, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, or plain text code review checklist/report; optional PR review template.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write output to a user-specified file and exits nonzero when critical findings are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
