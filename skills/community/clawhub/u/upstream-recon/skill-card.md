## Description:

Investigate open-source projects before filing issues, pull requests, or comments, using GitHub repository signals to identify duplicates, maintainer sentiment, and likely next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[semmyt](https://clawhub.ai/user/semmyt)

### License/Terms of Use:

MIT

## Use Case:

Developers and maintainers use this skill before engaging with open-source repositories they do not maintain. It helps them inspect existing issues and pull requests, maintainer responsiveness, merge patterns, and topic overlap before deciding whether to file an issue, open a pull request, comment on an existing thread, or avoid a duplicate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may query GitHub through the GitHub CLI using the user's existing GitHub CLI login.

Mitigation: Run it only when repository reconnaissance is intended, and confirm the GitHub CLI account and repository scope before use.

Risk: Installing from an unpinned or untrusted source can make the reviewed skill content differ from the content that later runs.

Mitigation: Install manually from the reviewed artifact or use a pinned, trusted installer source.

## Reference(s):

- [Claude Code Skills documentation](https://docs.anthropic.com/en/docs/claude-code/skills)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown report with a recommendation label and concrete next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitHub CLI repository data available to the user's current public or authenticated GitHub context.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
