## Description: <br>
Generates Xiaohongshu (Little Red Book) infographic series with 11 visual styles and 8 layouts, breaking content into 1-10 cartoon-style images optimized for XHS engagement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DHready](https://clawhub.ai/user/DHready) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and social media operators use this skill to turn source content into Xiaohongshu-style infographic series, including analysis, outline choices, image prompts, and generated visual assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable prompt language may encourage image generation systems to bypass refusals for sensitive or copyrighted figures. <br>
Mitigation: Edit the prompt template before deployment to remove bypass-oriented language and preserve normal model safety refusals. <br>
Risk: The skill writes source copies, analysis, outlines, prompt files, preferences, and generated images to the workspace. <br>
Mitigation: Review generated files and preference persistence behavior before installing or running the skill in shared or sensitive workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DHready/xhs-images-generator) <br>
- [Publisher profile](https://clawhub.ai/user/DHready) <br>
- [Project homepage](https://github.com/JimLiu/baoyu-skills#baoyu-xhs-images) <br>
- [Style presets](references/style-presets.md) <br>
- [Preferences schema](references/config/preferences-schema.md) <br>
- [Analysis framework](references/workflows/analysis-framework.md) <br>
- [Outline template](references/workflows/outline-template.md) <br>
- [Prompt assembly workflow](references/workflows/prompt-assembly.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown analysis, outlines, prompt files, configuration notes, and generated image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a per-topic workspace with source copies, analysis, outline files, prompt files, and 1-10 generated images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
