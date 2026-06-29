## Description: <br>
公众号长文配图生成器。输入MD文章，输出PNG配图包，同步到飞书云盘。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to turn Markdown long-form articles into WeChat public-account illustration packages, including covers, visual cards, section graphics, and usage guidance. It is intended for article illustration workflows rather than full article typesetting, video, or image retouching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically write generated images and intermediate files to a local Desktop folder. <br>
Mitigation: Use it only in workspaces where local file creation is expected, and review the generated output directory before sharing or publishing files. <br>
Risk: The workflow can upload outputs through a Feishu or lark-cli account without a clear per-run confirmation step. <br>
Mitigation: Require explicit confirmation before cloud upload, disable upload steps for sensitive drafts, or manually review files before running lark-cli upload commands. <br>
Risk: The workflow may contact external image or font services while generating article illustrations. <br>
Mitigation: Avoid unpublished or confidential article content when external assets are enabled, and prefer user-provided local images or approved asset sources for sensitive work. <br>
Risk: Master Mode can skip normal confirmation points for plan and style choices. <br>
Mitigation: Avoid Master Mode for sensitive or brand-critical content; use the multi-step mode so the illustration plan and style decisions are reviewed before generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwardwason/wx-peitu) <br>
- [Source repository](https://github.com/EdwardWason/wx-peitu) <br>
- [Workflow](references/workflow.md) <br>
- [Design System](references/design-system.md) <br>
- [Quality Gates](references/quality-gates.md) <br>
- [Assets](references/assets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown instructions with generated HTML/CSS, screenshot scripts, PNG/JPEG image files, and upload links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces standalone HTML as an intermediate artifact, screenshots it with Puppeteer, saves images locally, and can sync outputs to Feishu cloud drive.] <br>

## Skill Version(s): <br>
7.0.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
