## Description:

Monitors public website pages for content changes such as prices, regulations, job posts, news, or technical documentation and helps notify users when relevant changes occur.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and agents use this skill to define website monitoring tasks, capture baseline snapshots, compare later page fetches, and report meaningful changes in public web content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch any URL reachable from the user's machine, including private-network targets if not constrained.

Mitigation: Use only authorized public sites, and add URL allowlists plus private-network blocking before deployment.

Risk: The artifact includes anti-bot and CAPTCHA-related guidance that may conflict with site terms or acceptable-use expectations.

Mitigation: Follow target site terms and robots.txt, keep request rates low, and avoid CAPTCHA or anti-bot bypass tactics.

Risk: Page snapshots and logs may store sensitive or regulated content locally.

Mitigation: Do not monitor authenticated or sensitive pages, and protect or delete local snapshot data according to organizational policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/web-data-monitor-claw)
- [Monitoring rules](references/monitoring-rules.md)
- [Extraction templates](references/extraction-templates.md)
- [Anti-detection guidance](references/anti-detection.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local task records, snapshots, logs, and diff reports under the configured web monitor data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
