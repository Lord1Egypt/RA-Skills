## Description: <br>
Yuanfang HTML PPT helps an agent turn text or URL content into professional, editable PPTX decks and companion HTML previews using YAML-driven slide data and HTML templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyuanfang](https://clawhub.ai/user/iyuanfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users use this skill when they want an agent to create or revise local presentation decks from text, URLs, or structured slide content. It is intended for workflows that need editable PowerPoint output, reusable HTML previews, configurable themes, and human confirmation of content, branding, layout, and media choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering can replace existing local deck.html or deck.pptx files at the chosen output path. <br>
Mitigation: Review and confirm output paths before running render commands, and write to a new directory when preserving prior decks matters. <br>
Risk: The skill may fetch user-provided URLs and reuse discovered branding assets in a presentation. <br>
Mitigation: Provide only URLs whose content and branding assets are appropriate to fetch and include, and review extracted logos, colors, and fonts before rendering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iyuanfang/yuanfang-html-ppt) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with YAML or JSON slide content, Node.js shell commands, and generated PPTX and HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can generate or revise local deck.pptx and deck.html outputs from a content file and selected theme, brand, layout, and media options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
