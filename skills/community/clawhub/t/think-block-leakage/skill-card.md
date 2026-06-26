## Description: <br>
Internal reasoning from <think> blocks leaks into the final user-facing reply instead of being stripped. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvogt99](https://clawhub.ai/user/mvogt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to identify leaked reasoning tags or planning prose in model replies and decide whether to strip, redact, trim, or regenerate the response before showing it to users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Leaked reasoning tags or planning prose can expose internal model reasoning or confuse users when returned directly. <br>
Mitigation: Inspect replies for reasoning tags and planning preambles, then strip, redact, trim, or regenerate before delivery. <br>
Risk: Automatic redaction can make raw model output less visible during debugging. <br>
Mitigation: Keep raw debug output limited to authorized diagnostic workflows and show users only the regenerated or redacted answer. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown guidance with checklist-style bullets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or external service calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
