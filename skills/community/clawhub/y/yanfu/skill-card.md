## Description:

Yanfu helps developers rewrite an existing public landing page and 1-5 product screenshots into a clearer, evidence-grounded product story without changing positioning or inventing claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaohuadavidlee](https://clawhub.ai/user/shaohuadavidlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn a developer-oriented landing page into a target-user-facing `landing.html` while preserving verified product facts, brand style, CTA links, and evidence boundaries. The skill also produces concise translation notes so unresolved claims and major wording decisions remain reviewable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill browses a public URL and uses screenshots as rewrite evidence, which can expose non-public product information if sensitive inputs are provided.

Mitigation: Use only public landing pages and screenshots that are acceptable to process as rewrite evidence; avoid private screenshots and confidential product details.

Risk: Landing page rewriting can accidentally introduce unsupported product claims, metrics, testimonials, or customer evidence.

Mitigation: Keep every important claim tied to the public page, screenshots, or developer-confirmed facts, and place unresolved items in `yanfu-notes.md` instead of `landing.html`.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaohuadavidlee/skills/yanfu)
- [Server-Resolved GitHub Provenance](https://github.com/ShaohuaDavidLee/yanfu/tree/main/skills/yanfu)
- [Evidence and Browsing](artifact/references/evidence-and-browsing.md)
- [Output Specification](artifact/references/output-spec.md)
- [Translation Method](artifact/references/translation-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [HTML file plus Markdown notes and concise response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces `landing.html` for users and `yanfu-notes.md` for translation rationale and open confirmations.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
