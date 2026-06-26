## Description: <br>
End-to-end Xiaohongshu / RedNote operations skill for setting content style, saving an operating profile, generating posts in that house style, choosing or generating suitable images, and publishing through a dedicated independent browser flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spencer17x](https://clawhub.ai/user/spencer17x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operations teams use this skill to configure a reusable RedNote operating profile, generate post copy and image assets, and run publishing workflows through a dedicated browser profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live RedNote posts through a saved browser login. <br>
Mitigation: Keep review-before-publish enabled unless immediate posting is intentional, and require a human review checkpoint before using direct publish flows. <br>
Risk: A persistent browser profile may retain account login state. <br>
Mitigation: Use the dedicated RedNote browser profile documented by the skill, avoid sharing a daily browser profile, and periodically clear the saved profile when retained login state is not desired. <br>
Risk: Source images may include watermarks or reuse restrictions. <br>
Mitigation: Use watermark-free sources, reject watermarked images, and do not remove or script removal of watermarks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spencer17x/rednote-ops) <br>
- [Skill instructions](SKILL.md) <br>
- [English README](README.en.md) <br>
- [Workflow](references/workflow.md) <br>
- [Content rules](references/content-rules.md) <br>
- [Content output format](references/content-output-format.md) <br>
- [Image sources](references/image-sources.md) <br>
- [Independent browser publish path](references/publish-independent-browser.md) <br>
- [Publish usage](references/publish-usage.md) <br>
- [Auto learning](references/auto-learning.md) <br>
- [Profile schema](references/profile-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON configuration, shell commands, and generated asset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce temporary post assets such as post.json, pages.json, SVG files, and PNG files under the configured runtime output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
