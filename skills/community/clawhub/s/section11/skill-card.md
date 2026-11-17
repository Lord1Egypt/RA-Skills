## Description:

Evidence-based endurance coaching protocol for analyzing athlete training data, reviewing sessions, generating workout reports, planning workouts, answering training questions, and giving endurance coaching advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crankaddict](https://clawhub.ai/user/crankaddict)

### License/Terms of Use:

MIT-0

## Use Case:

External athletes and endurance coaches use this skill to turn user-controlled Intervals.icu-derived JSON data into readiness checks, training analysis, workout plans, and pre/post-workout, weekly, or block reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive training, wellness, activity, route, and threshold data from user-configured JSON files and dossiers.

Mitigation: Use local files or private repositories for training data, grant only the agent access needed for the task, and review what files the agent can read.

Risk: Fallback protocol and template files may be fetched from mutable remote URLs when local copies are unavailable.

Mitigation: Prefer local packaged files or pinned repository revisions, and review protocol/template changes before relying on fetched content.

Risk: First-use setup asks users to add a data discipline rule to persistent agent instructions, which can affect future sessions.

Mitigation: Add persistent rules only after review, scope them to this skill where the agent platform allows, and remove them when they are no longer needed.

Risk: Optional write workflows can change Intervals.icu calendar items, annotations, and sport thresholds.

Mitigation: Keep write operations in preview mode until reviewed, require explicit confirmation for changes, and update thresholds only from validated test results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crankaddict/skills/section11)
- [Section 11 open-source repository](https://github.com/CrankAddict/section-11)
- [Data mirror setup guide](https://github.com/CrankAddict/section-11#2-set-up-your-data-mirror-optional-but-recommended)
- [Section 11 protocol fallback](https://raw.githubusercontent.com/CrankAddict/section-11/main/SECTION_11.md)
- [Heartbeat configuration template](artifact/HEARTBEAT_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text coaching guidance with optional command examples and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite only metrics read from current-response JSON data sources and may include previewed write actions for supported agent runtimes.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
