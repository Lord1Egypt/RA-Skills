## Description: <br>
Sanitize logs, configs, prompts, stack traces, and skill content before they are shared publicly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nighty35628](https://clawhub.ai/user/nighty35628) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and support teams use Safe Share to create shareable copies of logs, configs, prompts, stack traces, and skill text before posting them publicly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pattern-based sanitization can miss custom secrets, names, hostnames, or context-specific identifiers. <br>
Mitigation: Provide only the text or file intended for sanitization, review the sanitized output manually before sharing, and avoid treating the result as a guarantee that all sensitive data was removed. <br>


## Reference(s): <br>
- [Detection Patterns](references/patterns.md) <br>
- [Output Format](references/output-format.md) <br>
- [Representative Test Cases](references/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, markdown, guidance] <br>
**Output Format:** [JSON or human-readable sections containing sanitized_text, findings_summary, and review_notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sanitized output should not include raw matched sensitive values.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
