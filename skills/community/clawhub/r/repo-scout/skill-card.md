## Description:

Discover, evaluate, and rank GitHub repositories in any ecosystem or domain. Produces a structured ranking document with star counts, languages, issue health, and contribution friendliness scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sliverp](https://clawhub.ai/user/sliverp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical evaluators use this skill to scout open-source GitHub projects for contribution targeting, technology evaluation, competitive analysis, and ecosystem exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub authentication and broad token access may expose private repository access or sensitive credentials during repository scouting.

Mitigation: Prefer unauthenticated public searches when possible; when authentication is necessary, use interactive gh auth login with minimum required permissions and do not paste GitHub tokens into chat.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with repository rankings, skipped repositories, and detailed profiles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is written as {workspace}/ecosystem-top{N}.md.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
