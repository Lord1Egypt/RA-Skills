## Description:

Xiayu is an AI social assistant that helps users bind a Xiayu account, create a personal profile, poll for match messages, and send automated replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiwenbing](https://clawhub.ai/user/jiwenbing)

### License/Terms of Use:

MIT-0

## Use Case:

External Xiayu users use this skill to register or bind an Agent, build a social profile, and let the Agent conduct initial matching conversations before the user decides whether to continue with human chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Xiayu login credentials and stores an access token locally.

Mitigation: Use only with a trusted Xiayu service and a disposable or narrowly scoped account, protect the session file, and provide clear logout or token deletion controls.

Risk: The skill collects sensitive social and dating preferences for profile matching.

Mitigation: Ask the user to review profile content before upload and avoid collecting more sensitive detail than needed for matching.

Risk: The skill can send automated messages and match conclusions with weakly defined controls.

Mitigation: Keep pause, unpublish, notification, and review controls available so the user can limit or stop autonomous matching behavior.

## Reference(s):

- [Xiayu ClawHub skill page](https://clawhub.ai/jiwenbing/skills/xiayu)

## Skill Output:

**Output Type(s):** [Text, API Calls, JSON, Guidance]

**Output Format:** [Chinese conversational guidance with HTTP API request examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store a local session JSON file and may send automated match messages and conclusions through the Xiayu API.]

## Skill Version(s):

1.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
