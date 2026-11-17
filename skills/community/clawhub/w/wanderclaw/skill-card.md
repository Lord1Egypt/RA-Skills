## Description:

WanderClaw is a dormant OpenClaw knowledge-exploration agent that activates on explicit keywords, searches the web around user interests, and returns concise postcard-style discoveries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzstart2](https://clawhub.ai/user/zzstart2)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to set up a personalized knowledge explorer that performs scheduled and user-triggered web exploration, summarizes findings, and manages postcard history, favorites, feedback, and blocked topics through chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs daily and weekly scheduled web exploration tasks.

Mitigation: Review the scheduled jobs and pending-cron queue after setup, and only enable recurring execution when the user expects persistent background activity.

Risk: The skill stores an interest profile, postcard archive, feedback, favorites, and blocked topics in the workspace.

Mitigation: Keep the state directory scoped to the skill, review stored interests before sharing a workspace, and avoid recording sensitive interests unless that storage is acceptable.

Risk: The setup flow can write a one-time onboarding prompt into agent memory.

Mitigation: Review memory changes during installation and remove the onboarding prompt once it has served its purpose.

Risk: Generated postcards depend on web search and fetch results.

Mitigation: Treat postcards as discovery aids and verify important claims against the linked original sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzstart2/skills/wanderclaw)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)
- [Explorer workflow](artifact/references/EXPLORER.md)
- [Postcard format](artifact/references/postcard-format.md)
- [Source map](artifact/references/sources.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chat messages with source links, plus JSON workspace state and configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May schedule recurring web explorations and write postcard, index, interest-profile, and exploration-log files in the workspace.]

## Skill Version(s):

3.2.4 (source: server release metadata and CHANGELOG, released 2026-04-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
