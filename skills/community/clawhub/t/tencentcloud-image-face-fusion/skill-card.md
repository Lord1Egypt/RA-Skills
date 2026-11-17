## Description:

Uses Tencent Cloud FuseFaceUltra to fuse a user face image with a template image and return a generated result URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neck-cn](https://clawhub.ai/user/neck-cn)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run Tencent Cloud face fusion on authorized face and template images. It is suited for agent workflows that return the service-generated fused image URL or a clear JSON error.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive face and template images are processed by Tencent Cloud.

Mitigation: Use the skill only with images the user is authorized to process, and disclose that images are sent to Tencent Cloud before enabling the workflow.

Risk: Tencent Cloud credentials are required for execution.

Mitigation: Use narrowly scoped Tencent Cloud credentials and avoid persisting secrets in shell startup files when possible.

Risk: The script can install the Tencent Cloud SDK at runtime without a pinned version.

Mitigation: Preinstall a pinned Tencent SDK in a controlled environment before using the skill.

Risk: The AI-synthesis logo can be disabled with a command option.

Mitigation: Keep the synthesis logo enabled unless there is a legitimate and reviewed reason to disable it.

## Reference(s):

- [Tencent Cloud FuseFaceUltra API reference](artifact/references/FuseFaceUltraApi.md)
- [Tencent Cloud original FuseFaceUltra documentation](https://cloud.tencent.com/document/product/670/106891)
- [ClawHub skill release page](https://clawhub.ai/neck-cn/skills/tencentcloud-image-face-fusion)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [JSON response containing a FusedImage URL, or JSON error output when credentials, image input, or the Tencent Cloud API call fails.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials and sends provided face and template images to Tencent Cloud; result URLs from the API may be time-limited.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
