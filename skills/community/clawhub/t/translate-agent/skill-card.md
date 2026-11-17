## Description:

Translate Agent provides stateless translation and summarization that returns deterministic raw JSON for translation, summarization, combined translation and summarization, heartbeat, and error flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anhducna](https://clawhub.ai/user/anhducna)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate text, summarize content, or do both while receiving machine-readable JSON responses. It is especially suited for workflows that need consistent schemas, language detection, Vietnamese default translation, and structured error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill activates broadly for translation or summarization wording and suppresses normal prose responses.

Mitigation: Install it only in agent environments where JSON-only translation or summarization responses are desired.

Risk: Unspecified translations default to Vietnamese, which may be unexpected in mixed-language workflows.

Mitigation: Provide an explicit target_lang when a different output language is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anhducna/skills/translate-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/anhducna)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Raw JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must contain only the JSON object for the selected action, with no Markdown, explanation, preamble, or code fences.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
