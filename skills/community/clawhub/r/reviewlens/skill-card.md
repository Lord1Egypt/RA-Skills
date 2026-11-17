## Description:

ReviewLens compresses mainland China marketplace reviews into a decision card that highlights repeated praise, recurring complaints, fit, regret risk, and whether a cheaper route is flawed or a pricier route is steadier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to turn product links, review screenshots, or copied review snippets into a practical buying judgment. It is aimed at mainland China shopping decisions where the user needs repeated praise, repeated complaints, concentrated bad-review issues, fit, regret risk, and price-versus-stability tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat review-based buying judgment as a guarantee about product quality.

Mitigation: Frame conclusions as review-based assessment, call out thin or biased samples, and avoid presenting marketplace review patterns as certainty.

Risk: The artifact includes a maintainer publish script that can run validation and publish the package.

Mitigation: Do not run artifact/scripts/publish.sh unless maintaining the release, and review any external validator it invokes before execution.

Risk: Live review inspection could cross into account activity or irreversible shopping actions.

Mitigation: Use public review evidence only unless explicitly required, and do not log in, post reviews, place orders, or submit irreversible actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/reviewlens)
- [Review Signals](artifact/references/review-signals.md)
- [Fit And Mismatch](artifact/references/fit-mismatch.md)
- [Verdict Cards](artifact/references/verdict-cards.md)
- [Example Prompts](artifact/references/example-prompts.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown decision card in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically structured as final call, repeated praise, repeated complaints, negative-signal concentration, best fit, likely regret, price-versus-stability judgment, and next step.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
