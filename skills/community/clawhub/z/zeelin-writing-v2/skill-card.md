## Description: <br>
A Chinese-language self-media writing assistant that guides article, Xiaohongshu, and video-script work from brief creation through research, topic selection, drafting, review, formatting, draft publishing, and archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelcey2023](https://clawhub.ai/user/kelcey2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and marketing teams use this skill to plan, draft, revise, format, and prepare Chinese self-media content for platforms such as WeChat public accounts, Xiaohongshu, and video scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local content and may process private writing materials or workspace files. <br>
Mitigation: Use it only in a dedicated content workspace and keep unrelated private files outside the default folders it reads. <br>
Risk: The skill may store Google or WeChat credentials in local configuration files or shell profiles. <br>
Mitigation: Provide credentials only in a trusted environment, protect local credential files, and rotate keys if they are exposed. <br>
Risk: The skill can install packages or run helper scripts as part of formatting and initialization workflows. <br>
Mitigation: Install dependencies manually in a trusted environment and review shell commands before execution. <br>
Risk: The workflow may prepare upload or publishing actions for platform drafts with limited user control. <br>
Mitigation: Require explicit approval before any draft upload, publishing, or external platform action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelcey2023/zeelin-writing-v2) <br>
- [Publisher profile](https://clawhub.ai/user/kelcey2023) <br>
- [Reference documentation index](references/README.md) <br>
- [Brief template](references/brief-template.md) <br>
- [User persona](references/用户人设.md) <br>
- [Google AI Studio API key page](https://aistudio.google.com/app/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content, brief files, HTML files, JSON manifests, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local project folders and draft content files; may prepare platform publishing drafts when credentials are configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
