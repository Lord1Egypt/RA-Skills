## Description: <br>
AI技术报告社媒宣发一键生成器，可从PDF技术报告生成X Thread、小红书帖子、微信公众号文章，并可选择生成配图提示或图片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianashannon](https://clawhub.ai/user/christianashannon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical marketing teams use this skill to turn a PDF technical report or paper into platform-specific launch and social media copy. It supports English X threads, Chinese Xiaohongshu posts, Chinese WeChat articles, and image specifications for optional AI-generated illustrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python scripts and install Python packages while processing a PDF. <br>
Mitigation: Run it in a virtual environment or sandbox and review the dependency list before execution. <br>
Risk: When image API keys are available, report-derived prompts may be sent to third-party image generation services. <br>
Mitigation: Use --no-image for confidential or unpublished PDFs unless external API use has been approved. <br>
Risk: Generated output files may contain extracted report content and publication-ready summaries. <br>
Mitigation: Review the output directory after use and delete generated files that should not remain on disk. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/christianashannon/tech-write-assist) <br>
- [Image Prompt Guide](artifact/references/image-prompt-guide.md) <br>
- [Platform Specs](artifact/references/platform-specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown content files, JSON image specifications, optional image files, and a Markdown summary report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated assets under an output directory; optional image generation may call external image APIs when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
