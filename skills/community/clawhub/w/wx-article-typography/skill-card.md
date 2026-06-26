## Description: <br>
A WeChat article typography skill that guides agents to organize article drafts into either a concise natural-flow style or a structured analytical Markdown style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[facadefish](https://clawhub.ai/user/facadefish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, and publishing agents use this skill to format WeChat article drafts as Markdown according to defined typography, paragraph, image placeholder, and publishing-flow conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional publish workflow may invoke local tools that upload article text or images and use WeChat or third-party credentials. <br>
Mitigation: Before running the example publish commands, confirm what each local tool invokes, where content is uploaded, and which credentials are used. <br>
Risk: The skill is a formatting guide, so misuse can produce Markdown that does not match the intended WeChat editorial style. <br>
Mitigation: Review generated drafts against the selected style rules before rendering or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/facadefish/wx-article-typography) <br>
- [Publisher profile](https://clawhub.ai/user/facadefish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines article structure, typography rules, image placeholders, and publish workflow conventions; it does not generate or upload content by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
