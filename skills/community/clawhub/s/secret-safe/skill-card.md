## Description: <br>
Secure API key and secrets management guidance for agent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brycexbt](https://clawhub.ai/user/brycexbt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill reviewers use this skill to configure API keys safely, avoid placing credentials in model context or logs, and audit other skills for credential handling mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may accidentally expose credentials by pasting API keys into chat, logs, prompts, or generated artifacts. <br>
Mitigation: Use OpenClaw environment injection or a secrets manager, and do not ask users to paste secrets into chat or print them in agent output. <br>
Risk: Credential-handling examples can be copied into other skills without preserving the required secret gates and output filtering. <br>
Mitigation: Review derived skills with the included audit checklist and require environment declarations for real secrets before publishing or installing. <br>


## Reference(s): <br>
- [Skill Security Audit Checklist](references/audit-checklist.md) <br>
- [Env Injection Examples: Common API Integrations](references/env-injection-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/brycexbt/secret-safe) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline YAML, JSON, Bash, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no bundled execution behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
