## Description: <br>
Compress, encode, and decode large JSON payloads into a compact, reversible TOON string to reduce token usage in LLM prompts and tool payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmkkevin](https://clawhub.ai/user/zmkkevin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to shrink repeated or large JSON for prompts and tool payloads, then decode or validate TOON back to JSON when a lossless round trip is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TOON output is reversible and can expose any secrets or sensitive JSON included in the input. <br>
Mitigation: Treat TOON as plaintext and avoid sending encoded sensitive data to prompts, logs, or external tools unless that sharing is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmkkevin/toon-json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [TOON strings, JSON, and Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional schema metadata for repeated-key compression; TOON is reversible compression, not encryption.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
