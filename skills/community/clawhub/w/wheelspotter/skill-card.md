## Description:

A wheel-spotting scout that finds reusable solutions before you build from scratch. Cost-controlled intelligent search with complexity-aware filtering, intent-based platform selection, and form consistency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garylooop](https://clawhub.ai/user/garylooop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use WheelSpotter to search for reusable libraries, services, tools, or reference implementations before building from scratch. The skill helps classify intent and complexity, query relevant package or repository sources, and return actionable recommendations or a self-build conclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub tokens can be supplied through command-line arguments.

Mitigation: Use environment-based secret handling where possible, avoid placing tokens in shell history or logs, and prefer running unauthenticated searches when higher rate limits are not required.

Risk: Search results and package metadata come from external sources and may be inaccurate, malicious, or stale.

Mitigation: Verify package ownership, license, recent activity, vulnerability status, and installation commands before integrating any recommendation.

Risk: The skill can suggest external packages or repositories that may not fit the user's exact requirements.

Mitigation: Treat recommendations as research leads, review the linked project documentation, and test candidates in an isolated environment before production use.

## Reference(s):

- [WheelSpotter ClawHub release page](https://clawhub.ai/garylooop/skills/wheelspotter)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include package names, repository or package URLs, install commands, filtering rationale, warnings, and search cost metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
