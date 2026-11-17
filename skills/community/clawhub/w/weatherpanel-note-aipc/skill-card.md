## Description:

WeatherPanel Note AI PC fetches Shanghai weather from Open-Meteo, summarizes conditions with a local LLM through the summarize CLI, updates a local Canvas dashboard, and appends summaries to a configured Obsidian note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinquan251](https://clawhub.ai/user/yinquan251)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to refresh a local Shanghai weather dashboard, generate a short weather summary, and append that summary to an Obsidian-compatible Markdown note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill's security claims do not match the shipped code and that it can run configurable local executables.

Mitigation: Review the installed files before use, lock SUMMARIZE_BIN and OBSIDIAN_BIN to trusted absolute paths, and avoid sensitive environments until the summarize shell invocation is fixed.

Risk: The release security guidance notes that dashboard functions load third-party web resources.

Mitigation: Use the dashboard only where third-party resource loading is acceptable, or replace external dashboard dependencies with locally pinned assets before deployment.

Risk: The release security guidance notes that configured coordinates may be sent to Open-Meteo.

Mitigation: Keep location settings non-sensitive and disclose that configured weather coordinates are sent to Open-Meteo when fetching forecasts.

## Reference(s):

- [Open-Meteo Documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated local JSON dashboard data and Markdown note entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Canvas dashboard assets, time-series JSON, summary JSON, token-cost JSON, and queued or appended Markdown summaries.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
