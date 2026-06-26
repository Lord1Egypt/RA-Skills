## Description: <br>
TokenLens Token Value Optimizer helps OpenClaw users estimate token usage, review efficiency, and get context-loading and model-routing recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuellai118](https://clawhub.ai/user/samuellai118) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect estimated token usage, receive optimization recommendations, and generate command-line guidance for reducing token waste while preserving task value. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates token tracking files under ~/.openclaw/workspace/memory/tokenlens/. <br>
Mitigation: Review that local workspace path before installation and back up or remove the generated files if they are no longer needed. <br>
Risk: Token usage, cost, savings, and routing recommendations may be estimates rather than measurements from a verified data source. <br>
Mitigation: Treat reported values as planning guidance and compare them with trusted provider or OpenClaw usage data before making operational decisions. <br>
Risk: Apply mode prints OpenClaw configuration commands that could affect agent behavior if run manually. <br>
Mitigation: Review each printed command and confirm it matches the intended configuration change before executing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samuellai118/tokenlens-token-value-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/samuellai118) <br>
- [TokenLens homepage](https://tokenlens.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, optional JSON, Markdown guidance, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local token usage and configuration data under ~/.openclaw/workspace/memory/tokenlens/.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
