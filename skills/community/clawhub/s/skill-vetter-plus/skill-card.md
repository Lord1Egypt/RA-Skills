## Description: <br>
Security scanner for AI agent skills. 9 built-in detection signatures. Identifies secrets, unsafe execution patterns, and prompt injection. Sub-50ms results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and ClawHub users use this skill as a first-pass local scanner before installing or reviewing agent skills. It reports text-matched indicators such as hardcoded secrets, unsafe execution patterns, raw network calls, and prompt-injection language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text-match findings can miss issues that require semantic, control-flow, dependency, or binary analysis. <br>
Mitigation: Use the scanner as a first-pass signal and manually review HIGH and CRITICAL findings before relying on the result. <br>
Risk: Reports may expose private file paths or matched snippets from scanned skill files. <br>
Mitigation: Run it only on the specific skill folder being reviewed and sanitize reports before sharing them. <br>
Risk: A clean scan does not prove that a skill is safe. <br>
Mitigation: Combine clean results with source review, dependency review, and the skill's threat model before installation or deployment. <br>


## Reference(s): <br>
- [Skill Vetter Plus product page](https://certainlogic.ai/products/skill-vetter-plus) <br>
- [Skill Vetter Plus on ClawHub](https://clawhub.ai/certainlogicai/skill-vetter-plus) <br>
- [Skill Vetter Plus documentation](https://certainlogic.ai/docs/skill-vetter-plus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Analysis] <br>
**Output Format:** [Plain text scan summary or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports matched fragments, severity, file path, line number, scanned file count, duration, and exit status.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
