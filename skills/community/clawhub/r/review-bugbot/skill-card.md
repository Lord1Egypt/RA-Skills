## Description:

Review code changes with Bugbot subagent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to request a Bugbot review of branch, pull request, or local working tree changes and receive a concise issue summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: For pull request or branch reviews, the workflow may need to change the checked-out branch in the active repository.

Mitigation: Confirm the target branch is checked out before review, and ask before stashing local changes if checkout is blocked.

Risk: The workflow passes the active repository path to a Bugbot review subagent.

Mitigation: Install and run this skill only when repository contents are appropriate for review by that subagent.

Risk: Review findings may be incomplete or incorrect and are not applied automatically.

Mitigation: Review findings before taking action; the skill instructs the agent not to fix findings unless explicitly asked.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eohmig/skills/review-bugbot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary or markdown table of review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity, file:line location, and finding text for each reported issue.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
