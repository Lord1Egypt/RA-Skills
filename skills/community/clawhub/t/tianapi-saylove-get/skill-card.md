## Description:

随机获取一句土味情话。当用户需要情话、撩人语录或幽默表白时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch a random cheesy love line from TianAPI for humorous messages, flirtatious quotes, or lighthearted confession text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper sends a TianAPI API key to TianAPI when fetching content.

Mitigation: Use the skill only when that data transfer is acceptable, and supply the key from a secure environment variable or secret manager.

Risk: Passing the API key on the command line or storing it in scripts/.env can expose the secret through shell history, process listings, or committed files.

Mitigation: Prefer TIANAPI_SAYLOVE_KEY, avoid command-line keys, and keep any scripts/.env file out of version control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/workxin/skills/tianapi-saylove-get)
- [TianAPI Saylove API Documentation](https://www.tianapi.com/apiview/80)
- [TianAPI Saylove API Endpoint](https://apis.tianapi.com/saylove/index)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON from the helper script or concise text presented to the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a TianAPI API key supplied through TIANAPI_SAYLOVE_KEY, scripts/.env, or the --key argument.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
