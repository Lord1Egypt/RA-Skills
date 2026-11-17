## Description:

Use Tafu's paid API for deterministic BaZi chart calculation, thematic readings, synastry, and soul-song generation when users ask for Chinese astrology analysis based on birth data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihao93li](https://clawhub.ai/user/zhihao93li)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call Tafu's paid API for BaZi chart calculations, thematic Chinese astrology readings, synastry, and soul-song generation from birth data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive birth data and the paid API key are sent to an external Tafu endpoint.

Mitigation: Install only when the user trusts Tafu with the submitted birth data and configure the API key through the host secret mechanism rather than chat.

Risk: TAFU_API_BASE_URL can redirect requests, including the bearer token, to a different endpoint.

Mitigation: Leave the default HTTPS API endpoint in place unless the override is a trusted HTTPS endpoint controlled by the operator.

Risk: The documented examples use fixed files under /tmp for payloads that can contain personal data.

Mitigation: Use private temporary files with cleanup for real user data instead of the fixed example paths.

Risk: Paid endpoints may consume credits or return asynchronous task IDs.

Mitigation: Call paid endpoints only after the user asks for that capability, surface credit usage when returned, and preserve task IDs for follow-up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhihao93li/skills/tafu-bazi)
- [Tafu Developers](https://tafu.me/developers)
- [Tafu Developer Billing](https://tafu.me/developers/billing)
- [Tafu API Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with preserved API results and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credits used, credits remaining, view URLs, task IDs, and validation prompts when returned or required by the API.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
