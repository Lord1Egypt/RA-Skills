## Description: <br>
Create new skills, modify and improve existing skills, measure skill performance, and manage skill distribution across agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hulk-yin](https://clawhub.ai/user/hulk-yin) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to scope, draft, evaluate, improve, optimize, package, and distribute agent skills. It supports iterative development workflows with test prompts, benchmark artifacts, review pages, and helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent skill files and package distributable skill archives. <br>
Mitigation: Review generated skill directories and package contents before syncing or distributing them. <br>
Risk: The evaluation workflow can run subprocesses, background tools, local review servers, and Claude or Anthropic service calls. <br>
Mitigation: Run evaluations in a trusted workspace, use only intended credentials, monitor long-running processes, and prefer static review output or an unused localhost port. <br>
Risk: Evaluation content may include sensitive prompts, outputs, or files that are exposed through review artifacts. <br>
Mitigation: Avoid using secret-containing skills or eval sets, and remove sensitive data from generated reports, review pages, and feedback files before sharing. <br>
Risk: The security guidance identifies an XLSX preview sanitization issue in the viewer. <br>
Mitigation: Do not preview untrusted XLSX outputs until the viewer sanitization issue is fixed. <br>


## Reference(s): <br>
- [ClawHub release: Skill Creator](https://clawhub.ai/hulk-yin/skill-creator-usm) <br>
- [Publisher profile: hulk-yin](https://clawhub.ai/user/hulk-yin) <br>
- [Skill Manager ecosystem reference](https://github.com/ZiweiAxis/skill-manager) <br>
- [Evaluation and benchmark schemas](references/schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with code blocks, JSON evaluation metadata, generated skill files, benchmark reports, and optional HTML review pages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent skill files, evaluation workspaces, packaged .skill archives, reports, and local or static review pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
