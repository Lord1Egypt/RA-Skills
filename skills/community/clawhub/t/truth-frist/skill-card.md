## Description: <br>
Evidence-first verification for status, config, file contents, actions, connectivity, mounts, and model selection. Use before answering any such claim. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[royhk920](https://clawhub.ai/user/royhk920) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to make an agent verify claims about system state, files, configuration, actions, connectivity, mounts, and model selection before answering. It is intended for status checks, configuration reviews, and other workflows where unsupported assertions would create operational risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification commands may expose sensitive configuration, log, or environment values in the agent response. <br>
Mitigation: Use command approval on sensitive systems and ask the agent to redact secrets or avoid printing full config, log, or .env lines unless necessary. <br>
Risk: The skill can still leave a claim Unknown when required tools, permissions, files, or runtime status sources are unavailable. <br>
Mitigation: Follow the skill's next-step commands and avoid treating Unknown claims as verified until direct evidence is available. <br>


## Reference(s): <br>
- [Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with evidence citations and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Classifies claims as Verified, Inferred, or Unknown and provides next-step commands for unknown claims.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
