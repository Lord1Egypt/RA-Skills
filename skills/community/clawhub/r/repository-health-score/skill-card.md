## Description:

Scores a repository's health across code quality, testing, documentation, CI/CD, security, dependencies, community, and maintainability, then produces a letter grade with specific improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and technical evaluators use this skill to assess repository maturity, maintenance quality, and adoption risk. It supports quick audits, dependency due diligence, repository comparisons, and improvement planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects repository files, git history, and optional public GitHub community metrics.

Mitigation: Run it only on repositories where local structure, history, and remote repository identity are acceptable inputs for a health score.

Risk: Static scoring can overstate or understate maturity because different project types have different baselines.

Mitigation: Treat the grade as a triage signal and review the dimension findings against the repository's purpose before making adoption or investment decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable scorecard, JSON report, Markdown report, or badge URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scores across eight dimensions, a total score, an A-F grade, and prioritized improvement suggestions.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
