## Description:

语义压缩 helps agents build prompts that remove redundant text while preserving key facts, decisions, data, and logical structure to reduce token usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[licool88](https://clawhub.ai/user/licool88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to prepare long conversations, documents, or memory candidates for LLM-based semantic compression while preserving important facts and decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated prompt still includes the original input and may expose sensitive or unrelated context to a downstream LLM.

Mitigation: Avoid including secrets or unnecessary sensitive context in the input before sending the prompt to an LLM.

Risk: Model-produced compressed text may omit or distort details if used as memory or as a replacement for the original.

Mitigation: Review compressed results before storing them, relying on them for decisions, or discarding the original source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/licool88/skills/semantic-compress)
- [Publisher profile](https://clawhub.ai/user/licool88)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown and plain text prompt content with optional JavaScript API and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper returns or writes a prompt for downstream LLM compression; it does not locally compress text.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
