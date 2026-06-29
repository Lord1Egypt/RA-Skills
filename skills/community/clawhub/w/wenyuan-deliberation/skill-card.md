## Description: <br>
Three-seat deliberation protocol for complex decisions: exposes assumptions, compares options, and identifies risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gordonlu](https://clawhub.ai/user/gordonlu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product leaders, architects, and other decision makers use this skill to structure complex decisions with explicit assumptions, trade-offs, risks, disagreement, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deliberation protocol can make answers longer and more elaborate than needed. <br>
Mitigation: Use Quick Mode for brief answers and keep each section concise. <br>
Risk: A single agent may appear to provide independent multi-party deliberation when it is only using structured perspectives. <br>
Mitigation: State that it is prompt-only deliberation unless an external Wenyuan runtime or multi-model system is explicitly available. <br>
Risk: Decision recommendations may be misleading when facts, constraints, or assumptions are missing. <br>
Mitigation: Label missing information as assumptions or unresolved issues, preserve serious disagreement, and provide concrete next actions for validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gordonlu/skills/wenyuan-deliberation) <br>
- [Project homepage](https://github.com/gordonlu/wenyuan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown by default; valid JSON only when the user explicitly requests Deep Mode JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English outputs follow the user's language; prompt-only with no external APIs, credentials, binaries, or tools.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
