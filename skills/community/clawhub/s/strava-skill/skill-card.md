## Description: <br>
Talk to your Strava data — ask questions about your activities, fitness trends, PRs, and training load using AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nftechie](https://clawhub.ai/user/nftechie) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent query Transition endpoints for Strava-linked activity history, performance trends, workouts, athlete profile details, and AI coaching chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TRANSITION_API_KEY exposure could allow unauthorized access to Transition-backed Strava data. <br>
Mitigation: Store the key in a secret manager or scoped environment, avoid committing or sharing it, and rotate or revoke it if exposed. <br>
Risk: Fitness and performance data is processed by Transition when personalized endpoints are used. <br>
Mitigation: Install only when the user is comfortable connecting Strava through Transition and letting an agent query that service. <br>


## Reference(s): <br>
- [Transition](https://www.transition.fun) <br>
- [Strava Skill on ClawHub](https://clawhub.ai/nftechie/strava-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated requests require TRANSITION_API_KEY; a no-auth workout endpoint is also documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
