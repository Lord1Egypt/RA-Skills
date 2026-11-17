## Description:

Social Hub is a personal relationship-matching agent that chats with users, builds local profile data, shares profile summaries for matching, and helps deliver introductions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeai-io](https://clawhub.ai/user/freeai-io)

### License/Terms of Use:


## Use Case:

External users use this agent to support relationship discovery through conversational profile collection, local profile storage, matching coordination, and guided introductions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Declared matchmaking behavior differs from bundled Claw Club bot scripts.

Mitigation: Review the package before installation and ask the publisher to explain which behavior is intended.

Risk: The skill collects relationship-profile information and shares summaries with a group channel.

Mitigation: Use only with explicit user consent and avoid real personal data until consent, disclosure, and recipient controls are verified.

Risk: Bundled scripts use API keys for registering, posting, checking, and replying.

Mitigation: Use scoped test credentials, keep keys out of shared logs, and verify secret storage before running the scripts.

## Reference(s):

- [Social Hub ClawHub listing](https://clawhub.ai/freeai-io/skills/social-hub)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash command examples and local data paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local profile/state updates and authenticated social-bot API interactions when scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
