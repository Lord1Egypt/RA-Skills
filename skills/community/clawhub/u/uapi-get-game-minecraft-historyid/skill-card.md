## Description:

This skill guides an agent to use UAPI's GET /game/minecraft/historyid endpoint to look up Minecraft username history by username or UUID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to prepare UAPI Minecraft name-history lookups, including choosing the name or uuid query parameter, handling the two response shapes, and interpreting common error responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Minecraft usernames or UUIDs submitted for lookup may be sent to uapis.cn.

Mitigation: Confirm that the user wants a UAPI lookup and avoid submitting unnecessary player identifiers.

Risk: The skill metadata includes a Minecraft server-status keyword that does not match the documented name-history endpoint.

Mitigation: Verify the request is for Minecraft name history before invoking this skill; use a different capability for server-status requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuakami/skills/uapi-get-game-minecraft-historyid)
- [UAPI service](https://uapis.cn)
- [Quick start](references/quick-start.md)
- [查询 MC 曾用名 operation](references/operations/get-game-minecraft-historyid.md)
- [Game resource](references/resources/Game.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with endpoint, query parameter, request, response, and error-handling details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an HTTP GET request shape for the UAPI endpoint; no generated files are required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
