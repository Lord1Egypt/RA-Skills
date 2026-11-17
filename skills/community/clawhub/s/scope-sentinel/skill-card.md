## Description:

Monitors coding sessions for scope drift by comparing the stated task with file changes and prompting the agent to keep unrelated work separate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill during focused implementation work to define a task boundary, monitor file changes for scope drift, and produce alerts or session summaries that separate unrelated follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scope-drift alerts may surface sensitive or unfinished local repository changes.

Mitigation: Review alert content in the intended local session and avoid sharing repository details outside approved channels.

Risk: Suggestions to stash, commit separately, expand scope, or continue could affect version-control workflow if accepted without review.

Mitigation: Treat alerts as advisory and explicitly confirm any version-control action before executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcools1977/skills/scope-sentinel)
- [Publisher profile](https://clawhub.ai/user/jcools1977)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown alerts, decision prompts, and session summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external API calls or automatic privileged actions; recommendations require user review.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
