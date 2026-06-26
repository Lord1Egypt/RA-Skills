## Description: <br>
Configures a local OpenClaw agent for Ryzen 9 5900XT and RX 6600XT workstations using Ollama gemma4 with unsandboxed tools for theoretical physics work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zedwiater](https://clawhub.ai/user/zedwiater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers with compatible high-RAM local workstations use this configuration to run a local agent tuned for theoretical physics exploration and local LLM performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configuration enables broad local agent permissions, including elevated tools and shell environment exposure. <br>
Mitigation: Install only when those permissions are intended, and narrow or disable elevated tools and shell environment access before use in sensitive workspaces. <br>
Risk: Discord access, persistent memory, automatic updates, and unredacted logging can expose activity or data beyond the immediate local session. <br>
Mitigation: Disable or restrict Discord control, memory, automatic updates, and unredacted logging unless they are required for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zedwiater/winchester-physics-bare-metal) <br>
- [Source skill instructions](artifact/SKILL.md) <br>
- [OpenClaw configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance] <br>
**Output Format:** [JSON configuration with Markdown usage notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets local workstation execution with Ollama models and OpenClaw settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
