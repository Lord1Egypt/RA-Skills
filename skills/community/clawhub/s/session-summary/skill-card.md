## Description:

Automatically generate session summaries and save them to an Obsidian daily notes folder at the end of a session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taka3693](https://clawhub.ai/user/taka3693)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture session duration, decisions, progress, next actions, and modified files as a structured Markdown summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session summaries may capture sensitive chat details into a local Obsidian vault path.

Mitigation: Invoke the skill only for sessions that are appropriate to summarize locally, and review the generated summary before retaining or sharing it.

Risk: The bundled script prints a sample summary and does not itself save content to Obsidian.

Mitigation: Verify the installed runner provides the intended save behavior before relying on the skill for persistence.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown session summary with configuration guidance and optional shell script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets an Obsidian vault daily notes folder when persistence is implemented by the runner.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
