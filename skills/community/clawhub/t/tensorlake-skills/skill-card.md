## Description: <br>
Tensorlake SDK guidance for AI agents and applications that need current Tensorlake documentation, sandbox APIs, orchestration APIs, setup steps, and safety guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cooleel](https://clawhub.ai/user/cooleel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to answer Tensorlake questions and generate Tensorlake Python, TypeScript, CLI, sandbox, and orchestration guidance grounded in live documentation or bundled fallback snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends a pipe-to-shell CLI installer. <br>
Mitigation: Review or avoid the installer unless the source is trusted and the command can be verified before execution. <br>
Risk: The skill may guide agents to run generated or untrusted code, expose ports, and reuse persistent sandboxes. <br>
Mitigation: Require human review before executing generated commands, exposing network services, or reusing sandbox state across tasks. <br>
Risk: The skill involves sensitive credentials such as TENSORLAKE_API_KEY and may process sensitive documents through the service. <br>
Mitigation: Use environment variables for credentials, do not print or paste secrets into chat, and avoid sending sensitive documents unless the data handling requirements are acceptable. <br>


## Reference(s): <br>
- [ClawHub Tensorlake Skill](https://clawhub.ai/cooleel/tensorlake-skills) <br>
- [Tensorlake Documentation Index](https://docs.tensorlake.ai/llms.txt) <br>
- [Tensorlake Documentation](https://docs.tensorlake.ai) <br>
- [Feature Lookup Snapshot](references/feature_lookup.md) <br>
- [Sandbox SDK Snapshot](references/sandbox_sdk.md) <br>
- [Applications SDK Snapshot](references/applications_sdk.md) <br>
- [Sandbox Use Cases Snapshot](references/sandbox_usecases.md) <br>
- [Platform Snapshot](references/platform.md) <br>
- [Troubleshooting Snapshot](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to fetch live Tensorlake documentation before using bundled snapshot references.] <br>

## Skill Version(s): <br>
2.9.0 (source: evidence.release.version, SKILL.md metadata, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
