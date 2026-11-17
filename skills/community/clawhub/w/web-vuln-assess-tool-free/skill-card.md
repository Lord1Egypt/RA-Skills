## Description: <br>
基于OWASP Top 10:2021标准，覆盖19类漏洞及100+检查项，支持多技术栈，提供安全检查清单与修复建议，生成按严重度排序的评估报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to assess authorized web applications and APIs against OWASP-aligned vulnerability checklists, technology-specific checks, and compliance mappings before release or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill concerns web vulnerability assessment and could be misapplied to systems without authorization. <br>
Mitigation: Install and use it only for applications you own or are explicitly authorized to test. <br>
Risk: Generated commands or assessment steps may be unsuitable for the target environment. <br>
Mitigation: Review any generated commands before running them and confirm scope, credentials, and operational impact. <br>
Risk: Callback URLs may receive sensitive report data. <br>
Mitigation: Avoid callback URLs unless the endpoint is trusted and the data-sharing implications are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-vuln-assess-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured JSON-like assessment summaries with optional code or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are checklist-driven and require human confirmation of findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
