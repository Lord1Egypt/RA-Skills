## Description: <br>
xhs-auto helps an agent prepare Xiaohongshu posts by drafting copy, generating or editing images, and running debug publishing checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luweizheng](https://clawhub.ai/user/luweizheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators, marketing operators, and their agents use this skill to turn a topic and optional user-provided images into a Xiaohongshu draft, generated image assets, and a pre-publication validation report. It is intended to keep the workflow in debug publishing until the user reviews the exact post content and confirms any live publish action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward live Xiaohongshu publishing through xhs-kit with a logged-in account. <br>
Mitigation: Use xhs-kit debug-publish first, review the exact title, body, tags, images, account, and schedule, and require explicit user confirmation before any live xhs-kit publish command. <br>
Risk: Image prompts or selected base images may be sent to external image providers. <br>
Mitigation: Avoid sensitive personal or proprietary content in prompts and base images, and confirm the selected provider and API endpoint before generation or editing. <br>
Risk: Draft copy, tags, generated prompts, and images may be saved in the workspace. <br>
Mitigation: Review the workspace output directory before sharing or publishing, and remove private campaign or account material when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luweizheng/xhsauto) <br>
- [Xiaohongshu publishing guide](references/publish.md) <br>
- [Text-to-image and image-editing guide](references/text-to-image.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown drafts, shell commands, JSON command results, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates draft content and image outputs under a workspace xhs-auto timestamp directory; image generation scripts report structured JSON results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
