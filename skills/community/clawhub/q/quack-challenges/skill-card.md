## Description:

Browse and complete Quack Network challenges by listing active challenges, submitting proof, and checking the leaderboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to participate in Quack Network challenges through an agent, including browsing available challenges, submitting proof text, and viewing leaderboard results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking the scripts reads a local Quack API key and sends authenticated requests, including submitted proof text, to quack.us.com.

Mitigation: Install and invoke the skill only when connecting an agent to Quack Network is intended, and avoid submitting sensitive proof text.

Risk: Some trigger phrases are broad and may cause the skill to run in contexts that are not clearly Quack-related.

Mitigation: Use explicit Quack-related prompts when listing challenges, submitting proof, or checking leaderboards.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpaulgrayson/skills/quack-challenges)
- [Quack API base URL](https://quack.us.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authenticated Quack Network API requests when scripts are invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
