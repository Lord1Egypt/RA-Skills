## Description: <br>
Recommends and can execute a cost-aware Chinese LLM for a prompt using task classification, benchmark scores, context length, token estimates, and budget tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nihaoxuan2026](https://clawhub.ai/user/nihaoxuan2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced agent users use this skill to classify a prompt, compare supported Chinese LLMs by quality, cost, latency, and context length, then choose cheap, balanced, or quality-focused routing. It can return recommendation guidance only or execute the prompt through configured provider APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may be sent to third-party model providers during automatic execution. <br>
Mitigation: Use --dry-run or --no-exec for recommendation-only operation, and avoid secrets, regulated data, or confidential prompts. <br>
Risk: Prompt snippets are retained in the local SQLite usage log. <br>
Mitigation: Review or clear local usage logs before sharing the environment and avoid entering sensitive text. <br>
Risk: The skill contacts countapi.xyz telemetry during usage logging and statistics display. <br>
Mitigation: Remove or disable the telemetry calls before use in privacy-sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nihaoxuan2026/token-decision) <br>
- [Publisher profile](https://clawhub.ai/user/nihaoxuan2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown-style console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external model-provider APIs unless run with --dry-run or --no-exec; local usage logs include truncated prompt text.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
