## Description:

Wahoo Fitness Cloud API skill for fetching workout metadata, downloading FIT files, and parsing power, heart-rate, cadence, GPS, and elevation data into local SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tgmerritt](https://clawhub.ai/user/tgmerritt)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to connect a personal Wahoo account, sync workout history, parse FIT telemetry, and query local training data for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived Wahoo tokens grant ongoing account access.

Mitigation: Store tokens only in local secrets files with restrictive permissions, avoid pasting credentials into chat or third-party tools, and remove user_read unless profile lookup is needed.

Risk: The local database and FIT directory contain GPS, heart-rate, power, device, and workout history.

Mitigation: Keep the training directory private, tighten permissions on shared machines, and keep database, FIT, environment, and token files out of commits.

Risk: Full syncs download FIT files from remote URLs without the bounds recommended by the security guidance.

Mitigation: Run full syncs cautiously in shared or high-trust network environments until FIT URL validation and download size limits are added.

## Reference(s):

- [ClawHub Wahoo Skill Release](https://clawhub.ai/tgmerritt/skills/wahoo-skill)
- [Wahoo Fitness Cloud API](https://cloud-api.wahooligan.com/)
- [Wahoo Developer Portal](https://developers.wahooligan.com)
- [fitparse FIT decoder](https://github.com/dtcooper/python-fitparse)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, SQL examples, and JSON/SQLite outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Wahoo developer credentials and local token storage]

## Skill Version(s):

0.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
