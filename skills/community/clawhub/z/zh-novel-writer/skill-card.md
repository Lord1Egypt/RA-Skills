## Description: <br>
Generates Chinese web-novel chapters in batches by calling configured external LLM APIs and saving generated chapters locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shine8592](https://clawhub.ai/user/shine8592) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors, writing assistants, and developers use this skill to generate batches of Chinese web-novel chapters from an outline and chapter range. It is intended for bulk drafting workflows, not single-chapter polishing, human editorial review, or publication-quality proofreading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outlines, plot notes, prompts, and chapter excerpts are sent to the configured external LLM provider. <br>
Mitigation: Avoid confidential manuscripts and personal data unless the selected provider and account are approved for that content. <br>
Risk: The skill uses API keys from environment variables to call external services. <br>
Mitigation: Use limited or disposable API keys where possible and rotate keys if they may have been exposed. <br>
Risk: Generated Markdown files are written to a user-selected output directory. <br>
Mitigation: Choose an output directory where new chapter files can safely be created and review generated content before reuse. <br>


## Reference(s): <br>
- [API 配置](references/api-config.md) <br>
- [Prompt 模板](references/prompt-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/shine8592/zh-novel-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated chapters are saved as local Markdown files in the selected output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
