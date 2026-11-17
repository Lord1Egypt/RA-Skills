## Description:

Slogan Maker helps agents generate brand taglines, industry slogans, rhyming slogans, translations, effectiveness checks, and classic slogan examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, brand builders, and agents use this skill to draft, translate, compare, and evaluate short Chinese and English slogans for products, industries, and campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated data-processing command that creates local storage and logs user arguments.

Mitigation: Review the package before installation, avoid using the unrelated data command, and require the publisher to remove or clearly document its local logging behavior.

Risk: Sensitive campaign text, customer identifiers, file paths, or private queries could be captured if passed to the logging data command.

Mitigation: Do not enter sensitive inputs into this skill unless the logging behavior is removed or isolated and reviewed.

Risk: Slogan scoring and recommendations are heuristic and may not predict campaign performance.

Mitigation: Treat generated slogans as drafts and validate them with human review, brand checks, and audience testing before release.

## Reference(s):

- [Slogan Maker Tips](tips.md)
- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/slogan-maker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with slogan drafts, translation notes, scoring summaries, and tabular examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated locally by bundled shell scripts; no external API keys were detected in the evidence.]

## Skill Version(s):

2.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
