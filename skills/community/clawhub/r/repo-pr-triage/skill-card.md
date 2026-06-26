## Description: <br>
Triage GitHub PRs and issues using vision-based scoring for prioritizing, scoring, reviewing, de-duplicating, or batch-processing open pull requests and issues against a project's mission and values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrob](https://clawhub.ai/user/patrob) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to onboard a repository, scan open GitHub pull requests or issues, score them against a project-specific rubric, and generate review queue reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository and pull request metadata through the user's authenticated gh CLI session. <br>
Mitigation: Use a least-privilege GitHub account or token and run it only against repositories the user intends to triage. <br>
Risk: Repository README, issue, and PR text can be untrusted input that may influence generated triage guidance. <br>
Mitigation: Review generated scores and reports before taking action on pull requests or issues. <br>
Risk: The optional cron and Telegram workflow can send recurring triage summaries outside the local workspace. <br>
Mitigation: Enable scheduled or messaging delivery only when the destination, cadence, and repository sensitivity are explicitly acceptable. <br>


## Reference(s): <br>
- [Repo PR Triage ClawHub Page](https://clawhub.ai/patrob/repo-pr-triage) <br>
- [Scoring Rubric Template](references/rubric-template.md) <br>
- [Example Vision Framework](references/example-vision.md) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON scan results, interview prompts, rubric files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated gh CLI session for repository and pull request reads; writes local triage configuration and report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
