## Description:

Shop Ad Guard checks Chinese e-commerce titles, product detail copy, livestream scripts, and promotional text before publication for high-frequency advertising-law risk terms, then returns risk levels, findings, and suggested revisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, operators, livestream teams, and agent builders use this skill as a pre-publication guardrail for Chinese e-commerce advertising copy. It flags absolute claims, medical-effect claims, exaggerated claims, promotion wording, comparative wording, and superstition-oriented terms before the copy is published.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may mistake keyword findings for legal advice or complete compliance approval.

Mitigation: Use the output as an auxiliary pre-publication check and route material or high-risk decisions to qualified legal or compliance review.

Risk: Rule-based matching can miss novel phrasing or flag context-dependent terms.

Mitigation: Review findings in context and maintain the term rules for the relevant product category and current compliance requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/shop-ad-guard)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or structured JSON reports with decision, risk level, finding count, matched terms, categories, severities, suggestions, and text positions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on supplied Chinese-language ad copy and uses Python standard library code with no external services or third-party packages.]

## Skill Version(s):

1.0.0 (source: package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
