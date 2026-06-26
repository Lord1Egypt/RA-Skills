## Description: <br>
OpenClaw Token省钱管家 helps agents control token costs with intelligent caching, dynamic model routing, real-time cost monitoring, and local budget controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e2e5g](https://clawhub.ai/user/e2e5g) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor skill-level token spend, route simpler tasks to lower-cost models, cache repeated work, and apply local controls when spend exceeds configured limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps cache, history, and control-state files locally in plaintext. <br>
Mitigation: Avoid caching sensitive prompts or responses on shared machines and review .openclaw/data periodically. <br>
Risk: Disable and budget controls can block or change agent behavior if configured too aggressively. <br>
Mitigation: Use disable and budget controls deliberately, and review current controls before relying on cost reports or routing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/e2e5g/token-cost-controller) <br>
- [Publisher profile](https://clawhub.ai/user/e2e5g) <br>
- [README](artifact/README.md) <br>
- [Configuration example](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text and JSON reports, Node.js module return values, and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local .openclaw/data cache, history, and control-state files.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
