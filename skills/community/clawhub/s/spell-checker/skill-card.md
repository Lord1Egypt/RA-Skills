## Description:

Use when interpreting user messages that may contain obvious spelling, grammar, speech-to-text, or casing errors, especially before acting on ambiguous instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elimaine](https://clawhub.ai/user/elimaine)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to interpret noisy or casually written user requests before reasoning, tool use, retrieval, graph updates, or embedding workflows. It normalizes obvious prose errors while preserving exact artifacts such as commands, filenames, URLs, code, config keys, and identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quiet typo normalization could change how an agent understands a request before reasoning.

Mitigation: Normalize only obvious natural-language errors; surface ambiguity or action-changing corrections with a concise confirmation before acting.

Risk: Exact strings such as code, commands, secrets, file names, URLs, and identifiers could be damaged if treated as prose.

Mitigation: Preserve byte-sensitive strings exactly and avoid rewriting quoted text, code blocks, logs, configuration keys, and other exact artifacts unless the user explicitly requests correction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elimaine/skills/spell-checker)
- [Publisher Profile](https://clawhub.ai/user/elimaine)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Natural-language guidance or concise clarification notices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves exact user-provided artifacts and asks before applying ambiguous or action-changing corrections.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
