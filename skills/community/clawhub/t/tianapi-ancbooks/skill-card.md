## Description:

Queries TianAPI ancient Chinese literature content by chapter ID, covering classics such as the Analects, Tao Te Ching, and Classic of Mountains and Seas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to look up chapters from Chinese classic literature through TianAPI and present returned book, chapter, author, and content fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TianAPI keys may be exposed through command-line arguments, scripts/.env, logs, or shell history.

Mitigation: Prefer the TIANAPI_ANCBOOKS_KEY environment variable, avoid sharing logs or command history that may contain the key, and rotate the key if exposure is suspected.

Risk: The skill depends on an external TianAPI service and account quota, so requests can fail because of invalid keys, missing API access, exhausted quota, empty results, or network timeouts.

Mitigation: Check returned API codes and error messages, confirm the chapter ID and TianAPI account status, and retry transient network failures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/workxin/skills/tianapi-ancbooks)
- [TianAPI AncBooks API Documentation](https://www.tianapi.com/apiview/265)
- [TianAPI AncBooks API Endpoint](https://apis.tianapi.com/ancbooks/index)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration guidance]

**Output Format:** [JSON from the helper script, commonly summarized as Markdown or plain text by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TianAPI API key and a chapter ID; the helper returns success, data, error, and optional API code fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
