## Description:

Monitors GitHub Trending and tech communities to track and analyze emerging tools in CLI, AI/ML, automation, and developer categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guogang1024](https://clawhub.ai/user/guogang1024)

### License/Terms of Use:


## Use Case:

Developers and technical teams use this skill to monitor GitHub Trending for emerging CLI, AI/ML, memory/context, automation, and learning projects, generate trend reports, and optionally bookmark projects for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts GitHub when run, so results depend on external network availability and the current GitHub Trending page structure.

Mitigation: Review generated recommendations before acting on them and verify important repositories directly when accuracy matters.

Risk: The bookmark helper keeps project data locally.

Mitigation: Use the bookmark feature only where local storage of repository metadata is acceptable, and review or remove stored bookmarks as needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guogang1024/skills/trend-watcher)
- [Publisher profile](https://clawhub.ai/user/guogang1024)
- [GitHub Trending](https://github.com/trending)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Console report or JSON trend analysis with project summaries, insights, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locally stored bookmark data when the bookmark helper is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
