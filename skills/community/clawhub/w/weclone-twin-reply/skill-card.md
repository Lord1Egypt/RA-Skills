## Description:

Build a review-gated digital twin reply from persona markdown, persona examples, and live conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xming521](https://clawhub.ai/user/xming521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to assemble an isolated prompt package from a persona pack and live conversation context, then generate a reviewable reply candidate in the user's voice. It is intended for draft-review-send workflows with explicit human approval before any outbound message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona directories can contain sensitive information and extra Markdown files that may be included in the generated prompt.

Mitigation: Keep the persona directory tightly curated, include only intended Markdown files, and review the rendered prompt before sending it to another model.

Risk: A generated reply may overcommit, expose private information, damage reputation, or depend on ambiguous context.

Mitigation: Use the required review gate, check the draft and risk flags, gather more context when facts are missing, and send only after explicit approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xming521/skills/weclone-twin-reply)
- [WeClone-Skill homepage](https://github.com/xming521/WeClone-Skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown draft reply with risk flags, reviewer note, and optional shell command guidance for rendering the isolated prompt package.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a curated persona directory with profile.md, persona_examples.md, guardrails.md, and optional state.md; generated replies remain gated on explicit human approval.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
