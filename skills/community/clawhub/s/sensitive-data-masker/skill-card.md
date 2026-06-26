## Description: <br>
Intelligent sensitive data detection and masking. Uses Microsoft Presidio + SQLite for automatic PII redaction with local restoration support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[STJ001](https://clawhub.ai/user/STJ001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to detect and mask sensitive message content before it is sent to an LLM, while retaining local mappings for restoration during task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Masking may fail silently or be misconfigured, allowing sensitive data to reach downstream services. <br>
Mitigation: Review before installing and verify that the hook masks a representative test message before use. <br>
Risk: Restorable secrets are retained in local mappings. <br>
Mitigation: Reduce or disable restoration retention where possible, and protect the mapping database and encryption key like a secrets store. <br>
Risk: Secrets passed through command-line arguments can be exposed by process listings or shell history. <br>
Mitigation: Avoid sending secrets through command-line arguments; use safer local input paths for testing and restoration workflows. <br>
Risk: Missing cryptography support or a Python module-name mismatch can prevent secure operation. <br>
Mitigation: Fix the cryptography dependency and module-name mismatch before deployment, then retest masking and restoration end to end. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/STJ001/sensitive-data-masker) <br>
- [Skill homepage](https://gitee.com/subline/onepeace/tree/develop/src/skills/sensitive-data-masker) <br>
- [Microsoft Presidio](https://github.com/microsoft/presidio) <br>
- [spaCy](https://spacy.io/) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text masking and restoration results with Markdown documentation and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores temporary local mappings for restoration; default retention is 7 days.] <br>

## Skill Version(s): <br>
1.0.7 (source: evidence release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
