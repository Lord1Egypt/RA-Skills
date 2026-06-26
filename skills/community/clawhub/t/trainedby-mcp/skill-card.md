## Description: <br>
Connects an agent to the trainedby.ai MCP server for personal coaching, health tracking, training timeline review, goal management, and reflective note capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Joostrothweiler](https://clawhub.ai/user/Joostrothweiler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to let an assistant review their trainedby.ai coaching timeline, health and fitness progress, goals, reflections, and onboarding profile, then provide coaching guidance or save user-approved notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive health, fitness, goals, reflections, and coaching profile data through an external MCP service. <br>
Mitigation: Install only when the user trusts trainedby.ai with that data, and review the OAuth login and requested access before use. <br>
Risk: Saved notes can retain personal coaching information in the user's trainedby.ai timeline. <br>
Mitigation: Confirm with the user before saving goals, workout feedback, reflections, or other coaching notes. <br>


## Reference(s): <br>
- [trainedby.ai MCP server](https://trainedby.fastmcp.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API Calls] <br>
**Output Format:** [Conversational text with structured MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OAuth-gated access to trainedby.ai timeline, onboarding, note, and feedback tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
