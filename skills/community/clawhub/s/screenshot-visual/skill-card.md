## Description:

Takes screenshots of targets using Playwright and performs visual/contextual analysis for potential vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nyetnighy](https://clawhub.ai/user/nyetnighy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security testers use this skill for authorized web reconnaissance by capturing browser screenshots and local evidence for exposed panels, debug interfaces, login pages, weak security-header indicators, and related web-surface inventory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically probes common admin, debug, API, configuration, and login paths.

Mitigation: Run it only against targets you control or are explicitly authorized to test, and confirm target scope before execution.

Risk: Generated screenshots, metadata, and reports can contain sensitive page content or target details.

Mitigation: Store outputs in protected locations, limit sharing, and delete or retain them according to the applicable engagement data-handling rules.

Risk: Automated browsing and path probing may contact unintended internal or sensitive network targets.

Mitigation: Avoid internal or sensitive networks unless that is intended and authorized, and review the target URL before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nyetnighy/skills/screenshot-visual)
- [Publisher profile](https://clawhub.ai/user/nyetnighy)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, Analysis, Shell commands]

**Output Format:** [PNG screenshots, JSON metadata, Markdown report, and console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local screenshots/<domain>/ artifacts; default viewport is 1280x720 and full-page capture is enabled.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
