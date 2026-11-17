## Description:

Proofread, propose edits, and check argument flow in reading order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-kapsalis](https://clawhub.ai/user/c-kapsalis)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, and teams use the skill to review drafts before publication or sending, get source-anchored suggestions, and preserve the author's intent and voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional editor's HTML export contains the supplied draft and context.

Mitigation: Keep generated HTML private and limit review to a narrowly selected project folder.

Risk: Optional command or network checks may access files or contact external destinations.

Mitigation: Review each command and destination first; use a disposable checkout and temporary credentials.

## Reference(s):

- [Project context guidance](artifact/references/PROJECT-CONTEXT.md)
- [Edit operations](artifact/references/EDIT-OPERATIONS.md)
- [Product verification guidance](artifact/references/PRODUCT-VERIFICATION.md)
- [Canonical documentation style guide](https://documentation.ubuntu.com/style-guide/)
- [Diátaxis documentation framework](https://diataxis.fr/)
- [Second Read Editor on ClawHub](https://clawhub.ai/c-kapsalis/skills/second-read)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML]

**Output Format:** [Editorial feedback in chat or Markdown; optional review JSON and HTML, with an author-approved revised draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggestions are source-anchored and remain author-controlled; a clean draft may receive no edits.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
