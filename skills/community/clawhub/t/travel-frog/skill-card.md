## Description:

A travel frog that autonomously explores the world, sends postcards, and takes photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nibbinnone](https://clawhub.ai/user/nibbinnone)

### License/Terms of Use:


## Use Case:

External users install this skill to run a playful travel-frog agent that plans trips, sends in-character updates, creates postcard and photo prompts, and keeps lightweight journey state and collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send autonomous channel messages during heartbeat events.

Mitigation: Review the configured channel and target before enabling scheduled heartbeats, and monitor early runs for unexpected message volume or content.

Risk: Postcard and photo workflows can call external image-generation providers.

Mitigation: Enable image generation only where external provider use is allowed, and review generated prompts before sending or archiving media.

Risk: The skill keeps persistent diaries, collections, state, and media paths.

Mitigation: Store only non-sensitive travel-frog content, review retained files periodically, and keep runtime data in an approved workspace path.

Risk: Shell-based writes, arbitrary state directories, and reset behavior can affect local files.

Mitigation: Use a fixed contained state directory, avoid user-controlled shell text or paths, and require confirmation before reset or force-status actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nibbinnone/skills/travel-frog)
- [Runtime configuration](config.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; persists state and collections under travel-frog-data and may produce image-generation prompts for postcard and photo workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
