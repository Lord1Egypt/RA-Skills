## Description: <br>
Security compliance checker for MCP/LLM applications. Performs non-invasive security assessments on configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaillera999](https://clawhub.ai/user/kaillera999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use SafeClaw to run non-invasive security checks against MCP, LLM application, and OpenClaw configuration files and receive prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local OpenClaw-related configuration or log paths while diagnosing security posture. <br>
Mitigation: Approve only the specific paths needed for the requested check, and avoid granting access to secrets files or session contents unless there is a narrow, explicit need. <br>
Risk: Security findings may include remediation suggestions or commands that change configuration or service behavior. <br>
Mitigation: Review suggested changes before applying them, especially for authentication, network exposure, firewall, plugin-source, and credential-handling settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaillera999/safeclaw) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [example-config.json](artifact/example-config.json) <br>
- [templates/minimal-config.json](artifact/templates/minimal-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with JSON-derived findings and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports pass, attention, and high-risk findings with remediation suggestions; the underlying checker emits JSON and distinct exit codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
