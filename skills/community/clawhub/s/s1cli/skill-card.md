## Description:

s1cli helps agents use the Stage1st (S1) forum CLI to log in or out, browse forums and threads, post or reply, search posts, check in daily, view profile details, and manage configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoion](https://clawhub.ai/user/geoion)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for s1cli commands and workflows for interacting with the Stage1st forum, including browsing, posting, replying, searching, checking in, and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents installation from the s1cli package or repository, which can execute third-party code in the user's environment.

Mitigation: Install in a virtual environment and pin or review the exact package or repository version before use.

Risk: The login command can accept a password on the command line and stores a local session file.

Mitigation: Prefer the interactive login prompt instead of passing passwords as command arguments, and protect the local s1cli configuration directory.

Risk: Posting, replying, checking in, and changing configuration can modify a forum account or user settings.

Mitigation: Allow the agent to perform those actions only after the user explicitly requests the specific action and reviews the intended command or content.

## Reference(s):

- [s1cli complete command reference](artifact/references/commands.md)
- [ClawHub skill page](https://clawhub.ai/geoion/skills/s1cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and short code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON parsing guidance for s1cli --json output.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
