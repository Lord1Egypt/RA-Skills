## Description: <br>
A self-evolution engine for AI agents. Analyzes runtime history to identify improvements and applies protocol-constrained evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmmoeny](https://clawhub.ai/user/mmmoeny) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent teams use this skill to analyze runtime history, select reusable evolution assets, and generate protocol-bound prompts or artifacts for auditable agent improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated code-changing and background loop behavior can alter a workspace or continue running beyond an operator's immediate review. <br>
Mitigation: Install and run only in an isolated, version-controlled workspace; prefer review mode and avoid lifecycle or skills-monitor repair helpers against untrusted skills. <br>
Risk: Update, publish, and external EvoMap or Hub communication paths may expose tokens or send data outside the local workspace. <br>
Mitigation: Disable auto-update and auto-publish unless intentionally needed, and avoid exposing broad GitHub, ClawHub, or API tokens. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mmmoeny/repo2) <br>
- [EvoMap Documentation](https://evomap.ai/wiki) <br>
- [EvoMap](https://evomap.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text with inline shell commands and JSON-like evolution artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read runtime history, emit protocol-constrained evolution prompts, and write local GEP assets or reports depending on execution mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
