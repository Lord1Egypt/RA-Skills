## Description:

Intelligent sensitive data detection and masking using Microsoft Presidio with SQLite storage and local restoration support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stj001](https://clawhub.ai/user/stj001)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to mask passwords, API keys, PII, and other sensitive values in received messages before downstream API processing, while retaining local mappings that can restore the original values for task execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Masking may fail open and allow original sensitive messages to continue downstream.

Mitigation: Review and test message:received masking end-to-end before installation; disable the hook if masking failures are observed.

Risk: Recoverable secret mappings may remain in local storage longer than users expect unless cleaned.

Mitigation: Set an appropriate TTL, run the cleanup or clear commands when needed, and protect the local data directory and encryption key.

Risk: The server security verdict is suspicious for this release.

Mitigation: Review this skill carefully before installing and rely on the server-provided security guidance as the authoritative risk source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stj001/skills/sensitive-data-masker)
- [Source Homepage](https://gitee.com/subline/onepeace/tree/develop/src/skills/sensitive-data-masker)
- [Microsoft Presidio](https://github.com/microsoft/presidio)
- [spaCy](https://spacy.io/)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Masked or restored text, JSON command output, and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite mappings with a default 7-day TTL; requires python3, Microsoft Presidio, spaCy, and the zh_core_web_sm spaCy model.]

## Skill Version(s):

1.0.7 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
