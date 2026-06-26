## Description: <br>
AI-powered multisport coaching for personalized workouts, training plans, performance analytics, and AI coaching across running, cycling, swimming, and triathlon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nftechie](https://clawhub.ai/user/nftechie) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External athletes, coaches, and developers use this skill to retrieve workouts, inspect training metrics, adapt training plans, and ask a Transition AI coach through Claude, MCP clients, or direct HTTP calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive fitness, profile, performance, and coach-chat data through Transition API calls. <br>
Mitigation: Install only if the user trusts Transition with the API key and coaching data, and avoid sharing unnecessary medical details in coach chat. <br>
Risk: Plan adaptation and Garmin push actions can affect a user's training schedule or connected services. <br>
Mitigation: Confirm user intent before adapting a plan or pushing workouts to Garmin, and use adaptation only for explicit schedule, fatigue, injury, or race-change requests. <br>


## Reference(s): <br>
- [Transition Skill Page](https://clawhub.ai/nftechie/transition-mcp) <br>
- [Publisher Profile](https://clawhub.ai/user/nftechie) <br>
- [Transition](https://www.transition.fun) <br>
- [Transition API Base URL](https://api.transition.fun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with HTTP API responses as JSON text and MCP tool/resource text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated features require TRANSITION_API_KEY; the Workout of the Day endpoint is available without authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and MCP server implementation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
