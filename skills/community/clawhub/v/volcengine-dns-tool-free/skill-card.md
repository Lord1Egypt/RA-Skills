## Description: <br>
火山引擎DNS免费版 helps individual developers manage Volcengine DNS zones and records, including queries, create, update, delete, TTL handling, rollback values, and propagation checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and domain operators use this skill to perform guided Volcengine DNS record maintenance, service-migration DNS cutovers, and post-change propagation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DNS record changes can interrupt websites, routing, or email. <br>
Mitigation: Use the skill only for explicit Volcengine DNS tasks, verify existing records before changes, and require manual confirmation for update and delete operations. <br>
Risk: The activation scope is broader than the DNS-only purpose. <br>
Mitigation: Limit use to DNS record maintenance, service-migration DNS cutovers, and propagation checks; avoid invoking it for vague code or deployment requests outside that scope. <br>
Risk: Over-permissioned or exposed API credentials could increase the impact of mistakes. <br>
Mitigation: Use limited-scope Volcengine API keys from environment variables and avoid hardcoding credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/volcengine-dns-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DNS record status, change logs, rollback commands, and propagation verification results.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
