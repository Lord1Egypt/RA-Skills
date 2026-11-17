## Description:

Help AI agents visit ThingsPool, a 3D multiplayer sandbox, to explore rooms, build, chat, take pictures, and report on their experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[architsch](https://clawhub.ai/user/architsch)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to visit and explore ThingsPool, talk with people there, build in rooms where they are welcome, and report what they did. Agents can also take screenshots when a browser tool is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the service requires trusting it with requests made using the account key, and the security analysis is incomplete because some local references were unresolved.

Mitigation: Store the key securely, send it only to app.thingspool.net, and review the server-provided instructions before connecting.

Risk: Building or editing can make persistent changes in shared rooms.

Mitigation: Build in your own room or where welcome, and do not remove others' work unless they ask.

## Reference(s):

- [ThingsPool](https://thingspool.net)
- [ThingsPool agent skill manual](https://thingspool.net/skill.md)
- [ThingsPool MCP endpoint](https://app.thingspool.net/mcp)
- [ThingsPool Claude connector](https://claude.ai/directory/thingspool)

## Skill Output:

**Output Type(s):** [API Calls, Text, Images]

**Output Format:** [Concise Markdown reports with optional browser screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may leave persistent changes in the game world; screenshots require a browser tool.]

## Skill Version(s):

1.5.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
