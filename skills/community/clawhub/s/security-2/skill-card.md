## Description: <br>
Runs a backend-backed live safety check for instructions that may trigger tool execution, external calls, file edits, permission changes, destructive or irreversible actions, prompt injection, or compliance-sensitive operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modeioai](https://clawhub.ai/user/modeioai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill before executing instructions with side effects to receive a machine-readable safety decision and caller policy guidance. It is intended for live pre-execution checks, not repository auditing or pure read-only planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Instruction text, operation context, and target identifiers are sent to the configured Modeio safety backend. <br>
Mitigation: Do not include secrets or credentials in those fields, and use the skill only when sending that operational context to the backend is acceptable. <br>
Risk: Network, dependency, API, or blocking responses can make the safety decision unavailable or unfavorable. <br>
Mitigation: Treat backend failures and blocking responses as stop conditions instead of silently proceeding. <br>
Risk: The safety backend URL can be overridden through SAFETY_API_URL. <br>
Mitigation: Verify SAFETY_API_URL in shared or production environments before relying on the decision. <br>


## Reference(s): <br>
- [Skill homepage](https://github.com/mode-io/mode-io-skills/tree/main/security) <br>
- [ClawHub skill page](https://clawhub.ai/modeioai/security-2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON safety-check output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success or error envelopes and depends on python3, the requests package, network reachability, and the configured safety backend.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
