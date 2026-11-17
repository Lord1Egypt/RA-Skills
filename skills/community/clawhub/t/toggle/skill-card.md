## Description:

Context layer for your agent: ToggleX captures work sessions, projects, focus scores, and context switches across the web so the agent can summarize activity, answer recall questions, detect patterns, and suggest next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aleksandar-jive](https://clawhub.ai/user/aleksandar-jive)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to give an agent context about recent work activity, including sessions, projects, focus patterns, stale work, and follow-up suggestions. It supports digests, recall, nudges, pattern detection, and optional automation or prediction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose detailed work-history records, including activity descriptions, domains, project context, and timing data.

Mitigation: Review the raw ToggleX data before broad use, avoid sharing raw records unnecessarily, and summarize activity in user-facing responses unless exact details are requested.

Risk: Persisted memory and cron-based syncing can retain sensitive activity data over time.

Mitigation: Enable persistence, cron syncing, digests, and prediction features only when the user has accepted local retention and the environment has clear retention controls.

Risk: The skill depends on a third-party activity API and a TOGGLE_API_KEY credential.

Mitigation: Store the API key outside chat, rotate it if exposed, and use the skill only when the ToggleX data source is trusted.

## Reference(s):

- [ToggleX homepage](https://x.toggle.pro)
- [ToggleX workflows API endpoint](https://ai-x.toggle.pro/public-openclaw/workflows)
- [ToggleX Clawbot integration](https://x.toggle.pro/new/clawbot-integration)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional raw JSON from the ToggleX API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TOGGLE_API_KEY; can optionally persist fetched activity data into local memory files.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
