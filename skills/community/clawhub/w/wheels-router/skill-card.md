## Description: <br>
Plan public transit trips globally using Wheels Router (Hong Kong) and Transitous (worldwide). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anscg](https://clawhub.ai/user/anscg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search for locations and plan public transit routes, with detailed Hong Kong trip information and broader global transit coverage where Transitous data is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route searches, coordinates, and travel times may be shared with the Wheels Router or Transitous service. <br>
Mitigation: Review privacy expectations before use and avoid sending sensitive travel details unless the service is acceptable for that context. <br>
Risk: Some MCP client setups use npx helper packages, which can introduce supply-chain exposure. <br>
Mitigation: Use a trusted MCP client setup and pin or preinstall helper packages where practical. <br>
Risk: Worldwide transit coverage can vary by city, so routes or schedules may be incomplete outside the best-supported areas. <br>
Mitigation: Check route results for plausibility and confirm important trips against local transit sources when needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anscg/wheels-router) <br>
- [Wheels Router MCP endpoint](https://mcp.justusewheels.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MCP connection guidance and route-planning tool usage guidance for search_location and plan_trip.] <br>

## Skill Version(s): <br>
0.5.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
