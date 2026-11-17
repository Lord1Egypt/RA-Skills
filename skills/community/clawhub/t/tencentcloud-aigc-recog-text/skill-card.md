## Description:

TencentCloud Text AIGC Detection helps agents submit text to Tencent Cloud TextModeration for AI-generated text detection and returns a structured result with suggestion, label, score, keywords, details, and request metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn233](https://clawhub.ai/user/shawn233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill through an agent to check whether submitted text, file content, or stdin input is likely AI-generated using Tencent Cloud TextModeration. It supports content review, article screening, news authenticity checks, and AI writing detection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text, including file contents passed to the skill, may be sent to Tencent Cloud using the configured Tencent Cloud credentials.

Mitigation: Avoid submitting sensitive or regulated content unless approved for the use case, and use narrowly scoped or temporary Tencent Cloud credentials.

Risk: Missing credentials, missing BizType, API errors, or over-limit text can prevent a valid detection result.

Mitigation: Treat API failures as failures, return the reported error to the user, and do not infer whether text is AI-generated without a successful Tencent Cloud response.

Risk: The Tencent Cloud SDK dependency may change behavior across versions if installed without pinning.

Mitigation: Install the SDK in a controlled environment and pin the dependency version when reproducibility matters.

## Reference(s):

- [TextModeration API Reference](references/text_moderation_api.md)
- [Tencent Cloud TextModeration API](https://cloud.tencent.com/document/product/1124/51860)
- [Tencent Cloud SDK Guide](https://cloud.tencent.com/document/product/1124/100983)
- [ClawHub Skill Page](https://clawhub.ai/shawn233/skills/tencentcloud-aigc-recog-text)

## Skill Output:

**Output Type(s):** [Text, Configuration instructions, Shell commands, Guidance]

**Output Format:** [JSON results with Markdown configuration guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials, a text moderation BizType, and input text of at most 10000 Unicode characters.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
