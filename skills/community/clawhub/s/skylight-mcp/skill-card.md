## Description:

Read and manage Skylight Calendar events, chores, rewards, shared lists, and meal plans through the user's signed-in family hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

People using a Skylight Calendar family hub can ask an agent to review or update household events, chores, rewards, shared lists, and meal plans. The skill can also help users configure the Skylight MCP connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary meal or shopping requests may activate Skylight handling without clear Skylight context.

Mitigation: Review activation rules and require clear Skylight or family-hub context before accessing the connected account.

Risk: Some security scanner reference checks were partial, so coverage is incomplete.

Mitigation: Review the skill's activation rules and requested actions before installing or connecting a personal account.

## Reference(s):

- [Skylight Calendar](https://www.ourskylight.com)
- [skylight-mcp on npm](https://www.npmjs.com/package/skylight-mcp)
- [Repository link listed in the skill documentation](https://github.com/chrischall/skylight-mcp)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/skylight-mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration instructions]

**Output Format:** [Natural-language summaries, structured Skylight data, and a JSON MCP configuration example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may reflect or confirm changes to the user's Skylight family hub.]

## Skill Version(s):

1.8.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
