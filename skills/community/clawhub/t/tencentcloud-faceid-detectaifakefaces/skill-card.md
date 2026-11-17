## Description:

Calls Tencent Cloud FaceID DetectAIFakeFaces to assess face images or videos for AI face swaps, recapture attacks, batch abuse signals, watermark attacks, and related anti-fraud indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzzhanglijie](https://clawhub.ai/user/hzzhanglijie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to submit authorized face images or videos to Tencent Cloud for anti-fraud and anti-spoofing analysis. It is intended for workflows that need JSON risk results for possible AI face swap, recapture, watermarked, or other attack traces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive face images or videos through a third-party biometric service.

Mitigation: Use it only with valid consent or another lawful basis for biometric processing, and confirm Tencent Cloud service terms and data handling requirements before use.

Risk: Tencent Cloud credentials are required to call the API.

Mitigation: Provide narrowly scoped credentials through environment variables and rotate or revoke them if they are exposed.

Risk: Runtime behavior depends on the Tencent Cloud Python SDK and external API availability.

Mitigation: Install a pinned, reviewed SDK version in an isolated environment and handle API errors before relying on results in production workflows.

## Reference(s):

- [Tencent Cloud DetectAIFakeFaces API Documentation](https://cloud.tencent.com/document/product/1007/101561)
- [ClawHub Skill Page](https://clawhub.ai/hzzhanglijie/skills/tencentcloud-faceid-detectaifakefaces)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [JSON API results with human-readable command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials and sends selected face image or video inputs to Tencent Cloud for analysis.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
