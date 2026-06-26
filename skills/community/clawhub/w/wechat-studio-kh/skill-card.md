## Description: <br>
Wechat Content Studio helps agents research, draft, review, prepare covers for, publish, verify, and monitor WeChat Official Account articles using the bundled writing methodology and publishing scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to turn topics or source material into WeChat Official Account article drafts, optionally run deeper horizontal-vertical research first, create cover assets, publish to the WeChat draft box, verify search visibility, and track article status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage WeChat credentials and includes helper scripts that may print or handle secrets. <br>
Mitigation: Store only the required WeChat credentials, avoid running credential helpers in logged terminals, and review credential files before use. <br>
Risk: Publishing workflows can run side-effectful commands and create WeChat draft content. <br>
Mitigation: Confirm the target article, theme, account credentials, and publish intent before running publishing scripts. <br>
Risk: The publishing script may install a global npm package when the required publishing CLI is missing. <br>
Mitigation: Review the global install step first or preinstall the required CLI through a trusted package-management process. <br>
Risk: Article titles may be sent to Sogou WeChat search during verification and monitoring. <br>
Mitigation: Do not verify sensitive or unpublished titles through Sogou unless external search disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luis1213899/wechat-studio-kh) <br>
- [Content Methodology](references/content_methodology.md) <br>
- [Horizontal-Vertical Analysis Methodology](references/hv-analysis-methodology.md) <br>
- [Style Examples](references/style_examples.md) <br>
- [Writing Techniques](references/写作技巧.md) <br>
- [Human-Like Writing Guide](references/去AI味指南.md) <br>
- [Popular Article Methodology](references/爆款方法论.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Files] <br>
**Output Format:** [Markdown and Chinese prose with inline shell commands and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create article markdown, cover image files, WeChat draft publishing actions, and local monitoring state when the user chooses those workflow steps.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
