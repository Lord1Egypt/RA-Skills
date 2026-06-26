## Description: <br>
Gemini Gem、Claude Code、Slidevを使って日本語のプレゼン資料を作成し、AIらしさを抑えるためのデザイン品質ルールを適用するワークフローです。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lastone3939](https://clawhub.ai/user/lastone3939) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators and agents use this skill to turn a slide brief, design prompt, optional character assets, and supporting context into Slidev HTML and a PDF deck. It is aimed at producing polished Japanese-language presentation materials with explicit typography, layout, and visual-quality constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks the agent to bypass normal permission checks when invoking Claude Code. <br>
Mitigation: Remove the permission-bypass flag and require normal command approval before executing generated slide-building commands. <br>
Risk: The workflow can upload or publicly share generated decks through hard-coded external Google Drive account and folder settings. <br>
Mitigation: Replace hard-coded account and folder values with private configuration and upload only after explicit confirmation that the deck may be shared. <br>
Risk: The workflow starts a temporary local HTTP server during screenshot and export steps. <br>
Mitigation: Keep outputs local by default and stop the temporary server after screenshots or PDF export are complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lastone3939/slide-creator) <br>
- [Structure Gemini Gem](https://gemini.google.com/gem/1n4WJG5tY6MlVpO2qM5PghGoNxY99z5v0) <br>
- [Design Gemini Gem](https://gemini.google.com/gem/1iLz7X88qkvl4hhT98AD8eEfHL8ptOVAC) <br>
- [Google Fonts family request](https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Zen+Kaku+Gothic+New:wght@700;900&display=swap) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown workflow guidance with bash, CSS, HTML, and Python snippets that produce Slidev HTML and PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May export files locally, send a PDF through Telegram, and optionally upload archives to Google Drive when explicitly requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
