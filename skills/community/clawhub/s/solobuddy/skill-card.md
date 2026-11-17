## Description:

Build-in-public companion for indie hackers: content workflow, Twitter engagement, project soul creation, and activity-aware nudges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humanji7](https://clawhub.ai/user/humanji7)

### License/Terms of Use:


## Use Case:

External creators, indie hackers, and developers use SoloBuddy to maintain a build-in-public workflow: capture ideas, draft posts, publish through a configured repository, monitor project activity, and optionally find Twitter/X engagement opportunities. The skill also helps create project personality profiles from documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Twitter/X monitoring can run recurring local jobs and send engagement opportunities without the user re-reading each fetch cycle.

Mitigation: Enable the monitor only after reviewing the LaunchAgent configuration, and keep documented stop, inspect, and remove commands available before use.

Risk: Twitter/X session credentials may be stored as plaintext shell environment values.

Mitigation: Avoid storing session tokens in shell startup files or scripts; use a dedicated credential store or re-authenticate manually when possible.

Risk: Broad publishing commands such as git add . can commit unintended local files from the configured data path.

Mitigation: Use a dedicated private repository, review git status and diffs before committing, and stage only intended files.

Risk: The skill reads and writes local files under the configured data path, including drafts, logs, activity snapshots, and project personality data.

Mitigation: Point solobuddy.dataPath at a dedicated folder that contains only intended build-in-public material.

## Reference(s):

- [SoloBuddy ClawHub page](https://clawhub.ai/humanji7/skills/solobuddy)
- [Project homepage](https://github.com/gHashTag/bip-buddy)
- [ClawdBot](https://clawd.bot)
- [Soul Creation Wizard](references/soul-wizard.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses with inline JSON, shell commands, draft content, and Telegram button payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update files under the configured data path and may propose git, Telegram, and optional Twitter/X monitoring commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
