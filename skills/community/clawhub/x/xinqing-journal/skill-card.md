## Description:

Xinqing Journal is a local Chinese mood journal that records natural-language entries, detects seven mood categories, scores mood from 1 to 10, extracts tags, and generates daily, weekly, monthly, and trend reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyby99-gif](https://clawhub.ai/user/dyby99-gif)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to keep a private local mood journal in Chinese and review mood history through summaries, calendars, and period reports. It is intended for personal tracking and reflection, not clinical diagnosis or medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Journal entries may contain sensitive mood and personal content stored in a local JSON file.

Mitigation: Install only when local storage is acceptable, keep workspace file permissions restricted, and avoid sharing raw journal files unless intentionally exported.

Risk: Mood classification is simple keyword-based tracking and may be inaccurate or incomplete.

Mitigation: Treat classifications and trend reports as reflective aids rather than medical or clinical advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyby99-gif/skills/xinqing-journal)
- [ClawHub publisher profile](https://clawhub.ai/user/dyby99-gif)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Command-line text and optional JSON reports backed by local JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries locally under the OpenClaw workspace and uses configurable mood and tag rules.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
