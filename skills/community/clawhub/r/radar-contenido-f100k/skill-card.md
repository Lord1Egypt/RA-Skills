## Description:

Radar de contenido de FORMULA 100K helps an agent monitor Instagram-format signals, verify visible mechanics from Reels, track recurrence across niches, and report which content formats have crossed a repeatability threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content operators use this skill to run a recurring research radar for Instagram Reels formats. It helps the agent configure the radar, collect candidate posts through approved sources, verify video mechanics visually, maintain a recurrence register, and produce Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting collection instructions could lead an agent toward logged-in Instagram browsing or private saved-post scraping.

Mitigation: Use only the OpenClaw path described by the release: no logged-in Instagram browser session, no scraping saved posts, and add saved Reels only from links explicitly sent by the user.

Risk: The workflow can involve Apify, Higgsfield, Telegram, and local report files, which may expose URLs, captions, transcripts, screenshots, or research notes to external tools or storage.

Mitigation: Review the content before processing or sending it, avoid sensitive private material, and require explicit user approval before paid or external-service actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/radar-contenido-f100k)
- [registro-ejemplo.json](references/registro-ejemplo.json)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, JSON, Markdown, Shell commands]

**Output Format:** [Markdown guidance with JSON register entries, configuration files, and report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before paid Apify or Higgsfield actions; reports are intended for delivery through Telegram in the OpenClaw workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
