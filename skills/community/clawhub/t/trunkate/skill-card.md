## Description: <br>
Trunkate AI semantically optimizes agent context history and large text blocks through the Trunkate AI API, with optional OpenClaw hooks for proactive token management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engineering-trunkate-ai](https://clawhub.ai/user/engineering-trunkate-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Trunkate AI to compress large agent histories, logs, and handoff context while preserving critical instructions and explicitly tagged private blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filtered OpenClaw history can be sent to the Trunkate API during optimization. <br>
Mitigation: Use PRIVATE and KEEP tags for sensitive content, keep TRUNKATE_API_KEY scoped and revocable, and avoid enabling the hook for highly confidential or regulated work. <br>
Risk: Enabled hooks can automatically replace local session history when token thresholds are met. <br>
Mitigation: Review hook configuration and threshold variables before enabling, and keep logs or backups where context replacement would affect auditability. <br>
Risk: TRUNKATE_API_URL can redirect optimization traffic if overridden. <br>
Mitigation: Verify TRUNKATE_API_URL points to the expected Trunkate endpoint before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/engineering-trunkate-ai/trunkate) <br>
- [Publisher Profile](https://clawhub.ai/user/engineering-trunkate-ai) <br>
- [Trunkate Homepage](https://trunkate.ai) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hooks Setup](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, inline shell commands, configuration snippets, and optimized text returned to agent history] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can replace OpenClaw session history when hooks are enabled; requires TRUNKATE_API_KEY for API-backed optimization.] <br>

## Skill Version(s): <br>
0.31.0 (source: evidence.release.version, version.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
