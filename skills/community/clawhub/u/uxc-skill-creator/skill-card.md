## Description: <br>
Creates wrapper skills that call remote tools through UXC, with reusable templates, validation rules, and anti-pattern guidance for provider skill design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to create or refine UXC-based provider wrapper skills with consistent command linking, discovery, authentication, validation, and safety conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated wrapper skills may include incorrect provider endpoint, protocol, authentication, or operation assumptions if used before verification. <br>
Mitigation: Confirm provider details with official documentation, UXC help probes, and local auth-binding checks before publishing or relying on the wrapper. <br>
Risk: Wrapper guidance can enable provider write operations when a generated skill is adapted for a service with high-impact actions. <br>
Mitigation: Keep read-before-write workflows and require explicit user confirmation before destructive or high-impact operations. <br>
Risk: Provider accounts or OAuth scopes may grant broader access than the wrapper skill needs. <br>
Mitigation: Use trusted provider endpoints, review OAuth or API-key scopes before connecting accounts, and remove local UXC links that are no longer needed. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Templates](references/templates.md) <br>
- [Validation Rules](references/validation-rules.md) <br>
- [Anti-Patterns](references/anti-patterns.md) <br>
- [ClawHub Release Page](https://clawhub.ai/jolestar/uxc-skill-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates, YAML configuration examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces wrapper skill structure and validation guidance for UXC-based provider integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
