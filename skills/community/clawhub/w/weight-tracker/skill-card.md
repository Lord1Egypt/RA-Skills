## Description:

帮助用户通过本地 JSON 记录体重、配置减肥目标，并用浏览器页面展示中英文减重进度图表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mixinan](https://clawhub.ai/user/mixinan)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals using an AI agent use this skill to log daily weight entries, update local JSON history, and view progress toward a target weight in a local browser page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private weight history is stored in local plaintext JSON.

Mitigation: Install only when local plaintext storage is acceptable and avoid sharing config or history files without review.

Risk: The local web page can expose weight data if served beyond localhost.

Mitigation: Run the HTTP server bound to localhost only, and add access controls before any LAN sharing.

Risk: Imported or shared configuration and history files may contain unsafe stored values.

Mitigation: Treat external config.json and weight_history.json files as untrusted and review them before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mixinan/skills/weight-tracker)
- [Artifact README](artifact/assets/README.md)
- [Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON file updates and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local configuration/history changes and browser-viewable progress output; no API credentials were detected.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
