## Description: <br>
Automated GitHub PR review governance and repository maintenance automation for pull request consensus reviews, merge gates, approved auto-merges, and scheduled repository triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corbin-breton](https://clawhub.ai/user/corbin-breton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use Repo Guardian to delegate GitHub pull request review, merge gating, optional auto-merge, and issue triage for a specified repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically merge pull requests based on AI approvals when configured with a write-capable GitHub token. <br>
Mitigation: Start with --dry-run or GUARDIAN_AUTO_MERGE=false, and require GitHub branch protection plus CI checks before permitting unattended runs. <br>
Risk: A broad GH_TOKEN could grant the automation more repository access than needed. <br>
Mitigation: Use a fine-grained GitHub token limited to the target repository and the minimum permissions needed for the chosen operating mode. <br>
Risk: Dual-review consensus is weaker if both reviewers use the same configured agent. <br>
Mitigation: Configure GUARDIAN_REVIEWER_B_AGENT as a genuinely separate reviewer before relying on automated merge decisions. <br>


## Reference(s): <br>
- [Repo Guardian ClawHub Skill Page](https://clawhub.ai/corbin-breton/repo-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and bash commands; the runtime script emits terminal logs and GitHub review comments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GH_TOKEN, openclaw, python3, curl, and target repository configuration; can run manually or on a cron schedule.] <br>

## Skill Version(s): <br>
1.4.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
