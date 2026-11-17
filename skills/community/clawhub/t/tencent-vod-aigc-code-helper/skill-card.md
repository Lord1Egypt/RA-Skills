## Description:

Helps agents guide Tencent Cloud VOD AIGC integrations, including image and video generation, custom elements and voices, task status polling, callbacks, and SDK-based code examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to generate implementation guidance and sample code for Tencent Cloud VOD AIGC APIs. It emphasizes API selection, Tencent Cloud SDK usage, credential handling, task polling or callbacks, and billing-risk reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tencent Cloud VOD AIGC API calls can create paid jobs and related storage costs.

Mitigation: Review the current billing documentation before use, test with low-cost parameters, and configure billing alerts or limits.

Risk: Tencent Cloud credentials could be exposed or over-privileged in generated examples.

Mitigation: Use least-privileged keys stored in environment variables or a secret manager, and avoid hard-coding secrets in code.

Risk: Blind SDK upgrades can introduce unexpected dependency or API changes.

Mitigation: Use pinned SDK versions in an isolated environment and upgrade deliberately when a needed API is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencent-mpaas-skills/skills/tencent-vod-aigc-code-helper)
- [Publisher profile](https://clawhub.ai/user/tencent-mpaas-skills)
- [CreateAigcImageTask documentation](https://cloud.tencent.com/document/product/266/126240)
- [CreateAigcVideoTask documentation](https://cloud.tencent.com/document/product/266/126239)
- [CreateAigcCustomElement documentation](https://cloud.tencent.com/document/product/266/127544)
- [CreateAigcCustomVoice documentation](https://cloud.tencent.com/document/product/266/129120)
- [Tencent Cloud VOD API overview](https://cloud.tencent.com/document/product/266/31753)
- [DescribeTaskDetail documentation](https://cloud.tencent.com/document/product/266/33431)
- [Tencent Cloud API key documentation](https://cloud.tencent.com/document/api/266/31757)
- [Tencent Cloud VOD callback event documentation](https://cloud.tencent.com/document/product/266/35579)
- [Tencent Cloud VOD AIGC billing documentation](https://cloud.tencent.com/document/product/266/95125#9c4dc6ff-4b3f-4b25-bf2d-393889dfb9ac)
- [Tencent Cloud International VOD AIGC billing documentation](https://www.tencentcloud.com/zh/document/product/266/14666#87e472ca-9c95-4658-ab7b-8f2130608419)
- [Tencent Cloud SDK for Python](https://github.com/TencentCloud/tencentcloud-sdk-python)
- [Tencent Cloud SDK for Go](https://github.com/TencentCloud/tencentcloud-sdk-go)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tencent Cloud API references, SDK installation commands, credential and SubAppId configuration guidance, polling or callback patterns, and billing-risk reminders.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
