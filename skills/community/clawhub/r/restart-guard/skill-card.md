## Description: <br>
Deterministic OpenClaw gateway restart with down/up state-machine verification, origin-session proactive ACK, and backward-compatible config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zjianru](https://clawhub.ai/user/Zjianru) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to restart an OpenClaw gateway from natural-language restart intent while preserving context, verifying the down/up transition, and reporting the result back to the originating session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to restart the OpenClaw gateway, which can interrupt availability if used unintentionally. <br>
Mitigation: Require an explicit confirmation step before restart execution and restrict who can invoke or configure the restart workflow. <br>
Risk: The workflow can run diagnostic commands and send external notifications that may include operational details. <br>
Mitigation: Keep notification channels minimal, review diagnostic content before enabling broad delivery, and restrict edits to restart config and context files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zjianru/restart-guard) <br>
- [README](README.md) <br>
- [Enhanced restart implementation spec](ENHANCED_RESTART_IMPLEMENTATION_SPEC.md) <br>
- [Troubleshooting reference](references/troubleshooting.md) <br>
- [Example configuration](config.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with bash commands, YAML configuration, and JSON or Markdown restart result artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write restart context, diagnostics, and delivery status files during restart workflows.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
