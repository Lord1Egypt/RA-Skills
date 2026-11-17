## Description:

Query WakaTime cloud coding statistics across time ranges, projects, languages, categories, editors, and machines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chensoul](https://clawhub.ai/user/chensoul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to retrieve read-only WakaTime cloud statistics for coding time, project activity, language breakdowns, editor usage, machines, and date-range summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The WAKATIME_API_KEY allows access to the user's WakaTime coding statistics.

Mitigation: Store the key only in a trusted environment, do not paste it into shared logs or prompts, and rotate it if exposed.

Risk: WakaTime responses may reveal sensitive work patterns, project names, branches, languages, editors, or machine names.

Mitigation: Query only the date ranges, projects, and filters needed for the task, and avoid sharing raw output when it contains sensitive activity details.

## Reference(s):

- [WakaTime API reference for this skill](references/wakatime-api.md)
- [WakaTime Developers](https://wakatime.com/developers)
- [WakaTime Summaries API](https://wakatime.com/developers#summaries)
- [ClawHub skill page](https://clawhub.ai/chensoul/skills/wakatime-skill)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WAKATIME_API_KEY and performs read-only requests to WakaTime cloud.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
