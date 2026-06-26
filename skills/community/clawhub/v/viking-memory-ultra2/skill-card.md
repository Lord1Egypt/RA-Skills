## Description: <br>
Viking Memory System Ultra 2 helps agents manage layered memory with write, read, search, autoload, promotion, weighting, compression, archive summary, and decompression commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsangho](https://clawhub.ai/user/tsangho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to persist, retrieve, search, rank, compress, archive, and restore agent memory files across hot, warm, cold, and archive layers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory contents may be sent to MiniMax and NVIDIA LLM services without a clear opt-in step. <br>
Mitigation: Do not use the skill with secrets, private business notes, or sensitive personal memory data unless remote LLM use is acceptable and documented for the deployment. <br>
Risk: The artifact includes embedded API credentials for remote LLM services. <br>
Mitigation: Require user-supplied credentials and remove embedded keys before production use. <br>
Risk: The skill can write or move persistent files in broad locations. <br>
Mitigation: Run it with a constrained memory workspace and review file-moving behavior before enabling automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tsangho/viking-memory-ultra2) <br>
- [Publisher profile](https://clawhub.ai/user/tsangho) <br>
- [MiniMax Anthropic-compatible messages endpoint](https://api.minimaxi.com/anthropic/v1/messages) <br>
- [NVIDIA chat completions endpoint](https://integrate.api.nvidia.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command output with persistent memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, python3, curl, VIKING_HOME, and SV_WORKSPACE; memory operations may call remote LLM APIs.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
