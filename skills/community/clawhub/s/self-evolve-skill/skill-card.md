## Description:

Use curl to query self-evolve.club shared skill rankings, self-evolve personal stats, and update self-evolve.club profile info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longmans](https://clawhub.ai/user/longmans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and self-evolve.club users use this skill to ask an agent for curl commands that retrieve public leaderboard data, retrieve authenticated personal ranking details, or update profile username information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated commands can read a local request key and send it to the configured API URL.

Mitigation: Keep BASE_URL fixed to https://self-evolve.club/api/v1 and confirm before allowing the agent to read the local request-key file or call authenticated endpoints.

Risk: The request key could be exposed in shared logs or sent with requests that do not need authentication.

Mitigation: Do not print the full REQUEST_KEY_ID, and do not send it to public overview or leaderboard endpoints.

Risk: Profile update commands can change the user's self-evolve.club username.

Mitigation: Confirm the target username and request details before executing the profile update command.

## Reference(s):

- [self-evolve.club](https://www.self-evolve.club/)
- [self-evolve.club API base URL](https://self-evolve.club/api/v1)
- [ClawHub skill page](https://clawhub.ai/longmans/skills/self-evolve-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands and request-key handling guidance for self-evolve.club API endpoints.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
