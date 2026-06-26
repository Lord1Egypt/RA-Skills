## Description: <br>
Skill Security Scanner scans ClawHub, GitHub, and local skills for security risks in JavaScript, TypeScript, Python, and Shell files using static rules and optional LLM semantic analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torchesfrms](https://clawhub.ai/user/torchesfrms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan skills before installation or deployment, review rule-based findings, and decide whether to request semantic analysis for suspected issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary reports unsafe command handling in the top-level wrapper. <br>
Mitigation: Invoke scripts/scan.sh directly with trusted, clearly typed targets instead of passing untrusted or shell-like strings through index.js. <br>
Risk: Semantic-analysis prompts can include scanned local source code. <br>
Mitigation: Inspect generated prompts before sharing them with an agent or model, and avoid including sensitive source content unless the user has approved that review path. <br>
Risk: Whitelist entries skip future scans by skill name. <br>
Mitigation: Use whitelist entries sparingly and periodically review trusted names before relying on skipped scan results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/torchesfrms/skill-sec-scan) <br>
- [Detection rules](references/rules.md) <br>
- [Dangerous commands](references/dangerous-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown security reports with optional JSON scan output and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include scores, threat categories, issue tables, explanations, and optional semantic-analysis prompts.] <br>

## Skill Version(s): <br>
4.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
