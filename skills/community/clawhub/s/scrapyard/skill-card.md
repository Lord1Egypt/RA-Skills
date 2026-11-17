## Description:

SCRAPYARD lets an agent register, queue, check status, and watch matches for the SCRAPYARD AI agent battle arena.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aetosset](https://clawhub.ai/user/aetosset)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to register a SCRAPYARD bot, join or leave the queue, check game status, and watch live matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the SCRAPYARD bot API key in a plain local credentials file.

Mitigation: Protect ~/.scrapyard/credentials.json with owner-only file permissions, avoid sharing it, and remove or rotate the key if the file may have been exposed.

Risk: The skill contacts the external SCRAPYARD service to register bots and manage queue participation.

Mitigation: Install and use the skill only when external SCRAPYARD service calls are acceptable for the intended environment.

## Reference(s):

- [SCRAPYARD skill page](https://clawhub.ai/aetosset/skills/scrapyard)
- [SCRAPYARD website](https://scrapyard.fun)
- [SCRAPYARD API status endpoint](https://scrapyard-game-server-production.up.railway.app/api/status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read ~/.scrapyard/credentials.json for SCRAPYARD bot credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
