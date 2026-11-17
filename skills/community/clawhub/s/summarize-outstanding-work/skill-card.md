## Description:

Summarize all outstanding work not merged into main/default branch (including unmerged branches, open PRs, uncommitted changes, and stashes)

This skill is ready for commercial/non-commercial use.

## Publisher:

[homostellaris](https://clawhub.ai/user/homostellaris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a Git repository for unmerged branches, open pull requests, local work-in-progress, stashes, and default-branch sync status, then summarize the outstanding work and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect repository metadata such as branch names, uncommitted file names, stash descriptions, commit summaries, PR status, and small diff stats.

Mitigation: Run it only in repositories where that metadata may be shared with the agent, and review the generated report before distributing it.

Risk: If GitHub CLI is installed and authenticated, read-only pull request checks may query GitHub using existing credentials.

Mitigation: Use an appropriate GitHub account and permissions, or skip GitHub CLI checks when remote queries are not desired.

## Reference(s):

- [Server-resolved source import](https://github.com/homostellaris/dotfiles/tree/master/agents/skills/summarize-outstanding-work)
- [ClawHub skill page](https://clawhub.ai/homostellaris/skills/summarize-outstanding-work)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown report with repository overview, work-in-progress lists, pull request table, unmerged branch summary, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reflect local or cached repository state when remote fetches or GitHub CLI queries are unavailable.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
