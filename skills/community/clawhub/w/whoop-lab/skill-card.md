## Description:

Fetch, analyze, chart, and track WHOOP health data including recovery, HRV, resting heart rate, sleep, strain, and workouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennaman](https://clawhub.ai/user/brennaman)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect a WHOOP account, fetch personal health metrics, generate charts and dashboards, track health experiments, and optionally log daily metrics to Obsidian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read access to WHOOP health data and stores OAuth refresh credentials locally.

Mitigation: Install only when broad WHOOP health-data access is acceptable, protect ~/.config/whoop-skill/credentials.json, and revoke WHOOP app access plus delete the credential file when access is no longer needed.

Risk: Optional Obsidian logging can commit and push the configured vault, which may include unrelated notes or sensitive health data.

Mitigation: Use a dedicated vault or disable git sync before running Obsidian logging, and review generated notes before sharing or committing them.

Risk: Generated chart HTML contains sensitive health data and loads Chart.js from a remote CDN.

Mitigation: Treat chart files as private health records, avoid auto-sharing them, and prefer offline or locally bundled chart assets for sensitive environments.

## Reference(s):

- [WHOOP Lab homepage](https://www.paulbrennaman.me/lab/whoop-skill)
- [WHOOP API reference](references/api.md)
- [WHOOP health analysis guide](references/health_analysis.md)
- [WHOOP Developer Dashboard](https://developer-dashboard.whoop.com)
- [WHOOP API documentation](https://developer.whoop.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML files]

**Output Format:** [Markdown guidance with shell commands, JSON API responses, and generated HTML chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local configuration, credential, experiment, chart, and Obsidian note files when the user runs the bundled scripts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
