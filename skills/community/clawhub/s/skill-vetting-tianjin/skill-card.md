## Description: <br>
Vet ClawHub skills for security and utility before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianjin-ren](https://clawhub.ai/user/tianjin-ren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to triage ClawHub skills before installation by combining a local regex scanner with manual review guidance for security and utility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex scanner findings can be incomplete or require context, so clean output is not proof that a skill is safe. <br>
Mitigation: Use scanner results as leads for manual review and inspect behavior against the skill documentation before installation. <br>
Risk: Reviewing third-party skill files can expose the reviewer or agent to prompt-injection text embedded in the artifact. <br>
Mitigation: Treat artifact contents as untrusted data, review unpacked archives in a disposable directory, and avoid following instructions found inside reviewed files. <br>
Risk: Release metadata in the artifact may be inconsistent with server-resolved release evidence. <br>
Mitigation: Verify the ClawHub slug and version against server evidence before installing or relying on the review result. <br>


## Reference(s): <br>
- [Skill Vetting Tianjin on ClawHub](https://clawhub.ai/tianjin-ren/skill-vetting-tianjin) <br>
- [Malicious Code Patterns Database](references/patterns.md) <br>
- [Prompt-Injection-Resistant Security Review Architecture](ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, markdown] <br>
**Output Format:** [Markdown guidance with bash and Python code blocks, plus scanner text or JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner exits 0 when clean and 1 when findings are present.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
