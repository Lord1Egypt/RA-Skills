## Description: <br>
Summarizes important problem-solving events into structured memory notes and saves them for later review and reuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marklyk](https://clawhub.ai/user/marklyk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill after troubleshooting, configuration changes, or notable decisions to decide whether a memory should be saved, classify it by priority and layer, and draft or update a concise record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory notes may preserve secrets, sensitive logs, or private operational details if saved without review. <br>
Mitigation: Review each generated note before saving and redact secrets, credentials, tokens, sensitive logs, and unnecessary personal or operational data. <br>
Risk: High-priority or always-loaded memories can affect future agent behavior beyond the original session. <br>
Mitigation: Reserve P0/L0 entries for durable rules or preferences that are intentionally reused, and use lower priority or archive layers for temporary troubleshooting records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marklyk/zongjie) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown notes with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes priority and memory-layer labels plus a save-location confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
