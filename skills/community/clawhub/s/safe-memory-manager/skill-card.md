## Description: <br>
When building OpenClaw agents that read untrusted text, use this skill to prevent prompt injection and memory poisoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horn111](https://clawhub.ai/user/horn111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a local memory helper that sanitizes untrusted text before writing it to memory files and reads bounded memory excerpts back into an agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security and integrity claims may be stronger than the protections enforced by the helper. <br>
Mitigation: Review carefully before installing, use only with a dedicated memory directory, and do not treat the ISNAD label or regex sanitizer as a strong protection against prompt injection or tampering. <br>
Risk: Memory files may contain sensitive data or untrusted content that later influences an agent. <br>
Mitigation: Avoid storing secrets and keep human or automated review in place before relying on persisted memory in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horn111/safe-memory-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python helper responses and sanitized memory file entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to a dedicated local memory directory and returns status metadata for append and read operations.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
