## Description:

Check WeryAI account credits and API balance through the official WeryAI account endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weryai-developer](https://clawhub.ai/user/weryai-developer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to check WeryAI API account credits before account verification or paid generation workflows. It is scoped to read-only balance lookup and does not perform image, video, music, or effect generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The WERYAI_API_KEY may be sent to a non-official host if WERYAI_BASE_URL is overridden.

Mitigation: Keep WERYAI_BASE_URL unset or pin it to the official HTTPS WeryAI API, and rotate any key used with an untrusted base URL.

Risk: The package includes generation-status vendor files that are unnecessary for a balance-only skill.

Mitigation: Review the installed artifact before deployment and rely only on the read-only balance command for this release.

Risk: The skill requires a WeryAI API key at runtime.

Mitigation: Use a limited key where possible and keep WERYAI_API_KEY only in the runtime environment, never in repository files.

## Reference(s):

- [WeryAI Account API](references/account-api.md)
- [WeryAI documentation index](https://docs.weryai.com/llms.txt)
- [Query API Account Credits](https://docs.weryai.com/api-reference/account/query-api-account-credits.md)
- [WeryAI Account ClawHub listing](https://clawhub.ai/weryai-developer/skills/weryai-account)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON balance result with concise Markdown or text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18 or newer; network access is required for the WeryAI account endpoint.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
