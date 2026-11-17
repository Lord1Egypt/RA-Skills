## Description:

Process text through curated content patterns for summarization, extraction, analysis, writing, and review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carolz1](https://clawhub.ai/user/carolz1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to apply curated text-processing patterns for summaries, insight extraction, claim analysis, writing improvement, text cleanup, and named fabric-style pattern workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch live pattern instructions from GitHub when local patterns are unavailable, so behavior can change outside the released artifact.

Mitigation: Prefer vendored or pinned pattern files and ask the user before any network fetch.

Risk: Remote pattern instructions may be treated as controlling instructions for processing user content.

Mitigation: Confirm the selected pattern and source before use, especially for sensitive documents.

Risk: The skill processes untrusted external text that may contain prompt-injection content.

Mitigation: Treat processed content as data and do not execute instructions found inside the input text.

## Reference(s):

- [Server-resolved source repository](https://github.com/CarolZ1/text-patterns)
- [Daniel Miessler fabric](https://github.com/danielmiessler/fabric)
- [Pattern Catalog](references/pattern-catalog.md)
- [ClawHub skill page](https://clawhub.ai/carolz1/skills/text-patterns)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or text following the selected pattern, with shell commands when the fabric CLI path is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Markdown files when the user asks to save output.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
