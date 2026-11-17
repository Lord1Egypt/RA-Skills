## Description:

Automated GitHub PR review governance and repository maintenance automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corbin-breton](https://clawhub.ai/user/corbin-breton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use Repo Guardian to review open pull requests with dual-model consensus, gate merges, post review comments, and triage repository issues on a scheduled or manual run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended repository write actions can merge pull requests based on model decisions over untrusted PR content.

Mitigation: Use human approval for merges, set GUARDIAN_AUTO_MERGE=false or pass --no-merge by default, and keep branch protections and CI checks enforced.

Risk: A broad GitHub token increases the impact of mistaken or compromised automation.

Mitigation: Use a fine-grained GH_TOKEN limited to the specific repository and only the permissions required for the chosen review or merge mode.

Risk: Dual-review consensus is weaker if both reviewers use the same or poorly separated model configuration.

Mitigation: Configure two genuinely separate reviewer agents and monitor disagreement or low-confidence outcomes before allowing write actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/corbin-breton/skills/repo-guardian)
- [Artifact homepage](https://clawhub.ai/corbin-breton/repo-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown review comments, JSON review verdicts, and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GH_TOKEN, openclaw, python3, curl, and a configured target repository; may write GitHub comments, labels, merge actions, and audit traces depending on configuration.]

## Skill Version(s):

1.4.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
