## Description: <br>
Reviews recent code changes, checks for bugs and security issues, and provides actionable feedback for staged or unstaged git diffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jagger-zxz](https://clawhub.ai/user/jagger-zxz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review local git changes before committing, with findings grouped by file and focused on bugs, security, performance, and code quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags the release as suspicious because unrestricted nested review execution may be enabled by default. <br>
Mitigation: Install only in a trusted maintainer environment and prefer running autoreview with --no-yolo or AUTOREVIEW_YOLO=0 unless unrestricted nested review is explicitly required. <br>
Risk: Security evidence notes staff moderation commands that could affect unintended targets if misused. <br>
Mitigation: Use moderation commands only with the intended staff account, explicit targets, and documented reasons. <br>
Risk: Diff review workflows may expose secrets or sensitive code to fallback external reviewers. <br>
Mitigation: Check diffs for secrets before allowing fallback external reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jagger-zxz/zxz-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review findings grouped by file, with inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should cite exact diff line numbers and end with a one-sentence summary.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
