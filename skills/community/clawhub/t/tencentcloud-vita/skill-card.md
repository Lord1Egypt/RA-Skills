## Description:

TencentCloud VITA helps an agent analyze images and publicly accessible videos through Tencent Cloud VITA, returning media descriptions, summaries, and prompt-directed visual understanding results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wayne-j151](https://clawhub.ai/user/wayne-j151)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send image inputs or public video URLs to Tencent Cloud VITA for visual content understanding, summaries, event extraction, and other prompt-guided media analysis. It can also persist a default VITA prompt for future calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, media URLs, and prompts are sent to Tencent Cloud under the user's VITA account.

Mitigation: Use only media and prompts appropriate for Tencent Cloud processing under that account, and avoid submitting sensitive content unless the deployment policy allows it.

Risk: A persisted VITA prompt can affect future analyses without being passed explicitly on the command line.

Mitigation: Review or reset the skill-local prompt file before shared or automated use.

Risk: Automated calls can produce unexpectedly long outputs or higher usage if max tokens are not constrained.

Mitigation: Set --max-tokens for automated workflows and monitor token usage returned by non-streaming calls.

Risk: The script depends on the openai Python package and reads credentials from the process environment.

Mitigation: Run in an isolated environment, pin the openai dependency, and expose only the required TENCENTCLOUD_VITA_API_KEY secret.

## Reference(s):

- [TencentCloud VITA Skill Page](https://clawhub.ai/wayne-j151/skills/tencentcloud-vita)
- [TencentCloud VITA Service Management Console](https://console.cloud.tencent.com/tiia/vita-service-management)
- [TencentCloud VITA API Endpoint](https://api.vita.cloud.tencent.com/v1/video2text)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON result with token usage for non-streaming calls, or streaming text when --stream is enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the supplied media, prompt, TencentCloud VITA API key, and optional temperature or max token settings.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
