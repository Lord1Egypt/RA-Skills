## Description: <br>
Daily GitHub repo health check + safe Dependabot auto-merge. Outputs markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and repository maintainers use this skill to review GitHub repository health, summarize open PRs and issues, and optionally auto-merge eligible Dependabot PRs after configured gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can merge GitHub pull requests and change repositories. <br>
Mitigation: Run report-only mode first and use a fine-grained GitHub token limited to the intended repositories. <br>
Risk: Scheduled auto-merge can apply dependency updates without direct human review. <br>
Mitigation: Avoid scheduling --merge-dependabot until CI and severity gates are reviewed and match the repository policy. <br>
Risk: daily-ops.sh can push local workspace commits. <br>
Mitigation: Do not run daily-ops.sh unless workspace push behavior is explicitly intended and accepted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-github-daily-ops) <br>
- [Publisher profile](https://clawhub.ai/user/Zero2Ai-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report and console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a GitHub token for GitHub API operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
