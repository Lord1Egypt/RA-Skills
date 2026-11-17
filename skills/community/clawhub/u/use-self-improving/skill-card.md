## Description:

Enables an agent to perform read-only lookup against local project, file, knowledge, and experience records when prior context may affect an answer, troubleshooting step, or external-impact action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzusp](https://clawhub.ai/user/zzusp)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to consult local, read-only knowledge and experience indexes before answering questions about prior projects, files, decisions, rules, similar failures, or before taking external-impact actions. It is intended for situations where historical local context may materially affect the current response or operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically searches persistent local agent knowledge across many ordinary tasks without clear user consent or tight scope limits.

Mitigation: Install only when automatic consultation of local knowledge is desired, and keep sensitive records out of the local knowledge base or require an operational rule that asks before opening local knowledge for unrelated projects, external-impact actions, or referenced original files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzusp/skills/use-self-improving)
- [Publisher profile](https://clawhub.ai/user/zzusp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language response, usually in Mandarin, with distinctions between index navigation, original evidence, historical records, and current state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookup posture; does not create, modify, or delete local knowledge-base content.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
