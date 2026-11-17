## Description:

AIを使った資料作成ワークフローで、Gemini Gem、Claude Code、Slidevを使ってスライド構成、デザイン指示、HTMLスライド、PDF配信までを案内します。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lastone3939](https://clawhub.ai/user/lastone3939)

### License/Terms of Use:


## Use Case:

External users and slide creators use this skill to turn source material, design preferences, optional character assets, and client context into a Slidev-based presentation workflow. It guides the agent through prompt preparation, slide generation, screenshot capture, PDF creation, and optional sharing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External AI and cloud-sharing steps can expose confidential slide content or client context.

Mitigation: Use only with non-confidential material unless the workflow is edited to make every external AI handoff and cloud upload an explicit opt-in step.

Risk: The workflow includes unrestricted local agent execution.

Mitigation: Remove the dangerous permission bypass and run generation in a constrained workspace before installing or using the skill.

Risk: Public Drive sharing and embedded credential details can create unauthorized access or account exposure.

Mitigation: Remove hardcoded credential material and disable public sharing by default before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lastone3939/skills/slide-creator)
- [Publisher profile](https://clawhub.ai/user/lastone3939)
- [Structure Gemini Gem](https://gemini.google.com/gem/1n4WJG5tY6MlVpO2qM5PghGoNxY99z5v0)
- [Design Gemini Gem](https://gemini.google.com/gem/1iLz7X88qkvl4hhT98AD8eEfHL8ptOVAC)
- [Google Fonts CSS for Noto Sans JP and Zen Kaku Gothic New](https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Zen+Kaku+Gothic+New:wght@700;900&display=swap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow instructions for creating Slidev HTML, screenshots, PDFs, and optional sharing steps.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
