## Description:

Monitor US-Iran strike probability using open-source indicators including news alerts, Iran internet connectivity, oil prices, flight traffic, military tanker detection, weather, Polymarket odds, and Pentagon activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexpolonsky](https://clawhub.ai/user/alexpolonsky)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to query StrikeRadar status, inspect individual open-source risk indicators, and monitor viewer pulse activity from the terminal or an agent workflow. Outputs are operational signals and algorithmic estimates, not intelligence assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and run paths execute unpinned npm tooling from the network.

Mitigation: Review before installing; prefer cloning a reviewed commit and running with a locally installed, pinned tsx version or a lockfile-managed workflow.

Risk: The skill contacts api.usstrikeradar.com when used.

Mitigation: Run only in environments where outbound access to that service is acceptable.

Risk: The reported strike probabilities are algorithmic estimates and not intelligence assessments.

Mitigation: Do not rely on the scores for safety, financial, personal, or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexpolonsky/skills/strikeradar)
- [Publisher profile](https://clawhub.ai/user/alexpolonsky)
- [StrikeRadar](https://usstrikeradar.com/)
- [StrikeRadar API](https://api.usstrikeradar.com)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Terminal text for interactive use and JSON with next_actions when piped]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries a public remote API and reports algorithmic risk scores, signal details, timestamps, and suggested next actions.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
