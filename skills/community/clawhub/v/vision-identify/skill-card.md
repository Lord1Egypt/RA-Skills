## Description: <br>
通过图片识别物品、动植物、人物、商品、文字等可见事物，并结合场景状态推断意图、提供选购和兼容提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyanggz11](https://clawhub.ai/user/zhangyanggz11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to identify visible subjects in uploaded images, understand likely context, and receive practical follow-up guidance such as shopping keywords, compatibility checks, or care suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images may contain private documents, faces, addresses, screens, or other sensitive information. <br>
Mitigation: Avoid using the skill with sensitive images unless that image handling is acceptable for the user and deployment context. <br>
Risk: Image identification, shopping, repair, or compatibility guidance can be wrong or incomplete. <br>
Mitigation: Verify recommendations before buying parts, making repairs, or taking safety-relevant action. <br>
Risk: Broad image-identification triggers may lead to overconfident responses on unclear or multi-object images. <br>
Mitigation: State uncertainty, identify likely alternatives, and ask for a clearer image or additional context when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyanggz11/vision-identify) <br>
- [Publisher homepage](https://wtmvw.com) <br>
- [Multimodal reference](references/multimodal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown image-identification response with scene analysis, suggested search terms, compatibility checks, and practical guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied image context and may include uncertainty notes when the image is unclear or ambiguous.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
