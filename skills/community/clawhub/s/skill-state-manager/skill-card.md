## Description:

A meta skill that manages API keys and state persistence for tools that require authentication or return 401/403 errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qipengguo](https://clawhub.ai/user/qipengguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to help agents prompt for missing third-party API credentials and persist local authentication state for future tool use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes asking users to paste live API keys or tokens into chat.

Mitigation: Prefer OAuth, masked prompts, environment variables, an OS keychain, or a dedicated secret manager where supported.

Risk: The skill describes saving credentials in plaintext local JSON files for reuse.

Mitigation: Use narrow-scope, short-lived tokens and review local file permissions before storing any credential.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qipengguo/skills/skill-state-manager)

## Skill Output:

**Output Type(s):** [guidance, configuration, code]

**Output Format:** [Markdown instructions with JSON file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to ask for credentials in chat and save them as local JSON state.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
