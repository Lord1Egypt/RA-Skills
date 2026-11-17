## Description:

Generate a 30-second standup update from yesterday's git activity: commits, PRs opened, merged, or reviewed, and Jira tickets touched.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rabgpt](https://clawhub.ai/user/rabgpt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before daily standup to gather recent GitHub and Jira activity and turn it into a concise Slack-ready yesterday, today, and blockers update.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires connected tools with access to GitHub and Jira activity.

Mitigation: Install only when that access is acceptable and review the generated standup before sharing it.

Risk: The artifact includes optional curl-to-bash installer guidance.

Mitigation: Do not run the installer unless it has been independently trusted and inspected.

Risk: The artifact mentions Personal Access Token fallback for GitHub authentication.

Mitigation: Prefer OAuth where possible and use only the minimum token access needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rabgpt/skills/standup-from-yesterday-commits)
- [Implexa homepage](https://implexa.ai)

## Skill Output:

**Output Type(s):** [markdown, text, API calls, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Slack-ready standup text with brief yesterday, today, and blockers sections.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
