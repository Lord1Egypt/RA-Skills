## Description: <br>
Guides an agent through researching, planning, prompting, and generating Xiaohongshu cover images and content cards with Lovart and optional Python/PIL text-card generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[velmavalienteqejimu22-jpg](https://clawhub.ai/user/velmavalienteqejimu22-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to turn Xiaohongshu post drafts, brand references, and optional source materials into cover concepts, Lovart prompts, generated image files, and supporting text-card assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide Lovart session cookies that can act as their account. <br>
Mitigation: Use a dedicated Lovart account when possible, keep .lovart_cookies.json private, and exclude it from version control. <br>
Risk: The download helper disables HTTPS certificate checks for image downloads. <br>
Mitigation: Patch the helper to use certificate verification or avoid the helper until the download path is corrected. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/velmavalienteqejimu22-jpg/xiaohongshu-cover-gen) <br>
- [Lovart operation guide](artifact/references/lovart-operation.md) <br>
- [Prompt checklist](artifact/references/prompt-checklist.md) <br>
- [Research platforms guide](artifact/references/research-platforms.md) <br>
- [Aesthetic guide](artifact/references/aesthetic-guide.md) <br>
- [Design tokens template](artifact/templates/design-tokens.md) <br>
- [Lovart](https://lovart.ai) <br>
- [Dribbble](https://dribbble.com) <br>
- [Xiaohongshu](https://xiaohongshu.com) <br>
- [Pillow documentation](https://pillow.readthedocs.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with prompts, shell commands, Python-generated image files, and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Lovart-ready prompts, visual direction notes, design tokens, iteration logs, and PNG/JPEG image assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
