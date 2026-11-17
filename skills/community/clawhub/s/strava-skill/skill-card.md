## Description:

Talk to your Strava data: ask questions about your activities, fitness trends, PRs, and training load using AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nftechie](https://clawhub.ai/user/nftechie)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to query Strava-linked training data through Transition, including workouts, performance metrics, athlete profile, AI coaching chat, and workout suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose Strava-linked activity data, performance metrics, profile details, prompts, and prior coach chats through Transition API access.

Mitigation: Use authenticated endpoints only with a trusted agent session, protect TRANSITION_API_KEY like a password, and revoke the key when access is no longer needed.

## Reference(s):

- [Strava Skill on ClawHub](https://clawhub.ai/nftechie/skills/strava-skill)
- [Transition](https://www.transition.fun)
- [Transition API](https://api.transition.fun)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline shell commands and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized endpoints require TRANSITION_API_KEY and may return Strava-linked activity, performance, profile, prompt, and coach chat data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
