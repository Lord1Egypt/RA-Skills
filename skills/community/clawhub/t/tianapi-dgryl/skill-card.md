## Description:

随机返回一条幽默励志的打工人语录，涵盖加班、老板画饼等职场真实写照。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch a random humorous workplace quote from TianAPI and present it as workplace copy, a light motivational line, or a relatable response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The TianAPI API key can be exposed through command-line history, a local .env file, provider URL logs, or committed files.

Mitigation: Prefer TIANAPI_DGRYL_KEY or a managed secret store, avoid passing the key on the command line, do not commit scripts/.env, restrict local secret-file permissions, and rotate the key if exposure is suspected.

Risk: The skill depends on an external TianAPI request and may fail because of invalid credentials, missing API access, exhausted quota, network timeouts, or provider errors.

Mitigation: Check TianAPI error codes before presenting output, retry transient network failures once, and ask the user to verify API access or quota when credential or entitlement errors occur.

## Reference(s):

- [TianAPI DGRYL API Documentation](https://www.tianapi.com/apiview/262)
- [TianAPI DGRYL API Endpoint](https://apis.tianapi.com/dgryl/index)
- [ClawHub Skill Page](https://clawhub.ai/workxin/skills/tianapi-dgryl)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON from the helper script, usually transformed into concise text or Markdown for the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a TianAPI API key supplied through TIANAPI_DGRYL_KEY, a local scripts/.env file, or a command-line argument.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
