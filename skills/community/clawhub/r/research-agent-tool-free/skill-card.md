## Description: <br>
研究代理助手免费版 helps users conduct interactive topic research, synthesize findings, and maintain structured Markdown research documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, students, independent developers, and founders use this skill to run interactive web research on a single topic, organize findings into persistent Markdown documents, review progress, and optionally export research to PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs web research and creates or updates local Markdown/PDF research files. <br>
Mitigation: Keep research topics and writable source folders scoped, and review generated research artifacts before relying on them. <br>
Risk: The optional callback URL can send completion notifications to an external endpoint. <br>
Mitigation: Do not provide a callback URL unless the endpoint is trusted for the research content being processed. <br>
Risk: PDF export or setup guidance may involve local tools or package-install commands. <br>
Mitigation: Review PDF export and package-install commands before allowing execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/research-agent-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON-like status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local research files; PDF export is optional and depends on local tools such as pandoc.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
