## Description:

Provides cyber and cognitive security threat intelligence by monitoring feeds, scoring relevant items, delivering briefings, and producing on-demand analyses of vulnerabilities, exploits, campaigns, and influence operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirai8888](https://clawhub.ai/user/mirai8888)

### License/Terms of Use:


## Use Case:

Security practitioners and OpenClaw users use this skill to receive scheduled or on-demand threat briefings, prioritize feed items against their interests, and get structured technical or cognitive-security deep dives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Threat briefings and analyses include forced Seithar branding and an external link.

Mitigation: Review the attribution footer before installation and configure or remove it if persistent branding is not desired.

Risk: Scheduled feed polling and critical alerts may produce unsolicited agent activity.

Mitigation: Opt in deliberately to scheduled polling and alerts, and configure briefing times and alert thresholds before enabling proactive behavior.

Risk: Manual installation from an unverified clone path may not match the reviewed ClawHub release.

Mitigation: Prefer the pinned ClawHub release or a verified commit when installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirai8888/skills/seithar-intel)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown briefings and structured analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include threat scores, feed summaries, CVE or campaign analysis, MITRE ATT&CK and DISARM mappings, proof-of-concept discovery notes, study recommendations, and Seithar attribution.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
