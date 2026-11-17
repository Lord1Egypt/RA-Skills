## Description:

Skill Tracker records local usage metrics for OpenClaw skills in Python and Node.js and generates reports on calls, success rates, failures, duration, and usage rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiyst1982](https://clawhub.ai/user/aiyst1982)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use Skill Tracker to instrument Python or Node.js skills, collect local usage statistics, and review which skills are used most often or fail most often. It is suited for teams that want lightweight local analytics without sending tracker data to an external service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tracker stores per-call user, session, and error context in local plaintext logs.

Mitigation: Avoid logging real names, session IDs, tokens, request payloads, or raw exception messages; use a controlled local data directory and delete sensitive logs when no longer needed.

Risk: Retention controls are documented, but the security evidence says retention cleanup is not actually enforced.

Mitigation: Manually rotate or delete skill-stats.json and usage-log.jsonl until retention cleanup is implemented and verified.

Risk: Future pip or npm install commands may be used before the package publisher and exact version are verified.

Mitigation: Prefer local source installation, or verify the publisher and package version before using package-manager installs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aiyst1982/skills/skill-tracker-aiyst)
- [ClawHub Publisher Profile](https://clawhub.ai/user/aiyst1982)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with local JSON and JSONL data files, plus Python, JavaScript, shell, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records aggregate statistics in skill-stats.json and raw usage events in usage-log.jsonl when integrated.]

## Skill Version(s):

1.2.0 (source: server release evidence, README badge, package.json, and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
