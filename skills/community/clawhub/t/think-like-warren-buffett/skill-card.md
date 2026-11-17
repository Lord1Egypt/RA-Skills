## Description:

Point-in-time Buffett-style company analysis for stocks, Berkshire case studies, and BUY/PASS verdicts, grounded in cached company cards and strict decision-date discipline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yixiao1032-publish](https://clawhub.ai/user/yixiao1032-publish)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to produce Buffett/Graham-style underwriting memos, moat tests, Berkshire case re-underwriting, benchmark comparisons, and BUY/PASS research verdicts. Outputs are research framing, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BUY/PASS research outputs may be mistaken for personalized financial advice.

Mitigation: Present outputs as research framing only and require a qualified human review before making investment decisions.

Risk: Helper commands can fetch filings and write persistent cached analysis artifacts.

Mitigation: Run helper commands only in a controlled workspace and review generated files before reuse or publication.

Risk: The security summary flags under-scoped local file reading in helper tooling.

Mitigation: Do not run oracle.py learn on sensitive files or directories.

Risk: The security summary flags persistent framework mutation behavior.

Mitigation: Treat evolution or framework-changing commands as maintainer-only and review diffs before accepting changes.

Risk: The preview server may expose generated files beyond localhost.

Mitigation: Do not run serve-site on an untrusted network unless the bind behavior is fixed or the service is firewalled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yixiao1032-publish/skills/think-like-warren-buffett)
- [Skill homepage](https://github.com/yixiao1032-publish/buffet-oracle)
- [README](README.md)
- [Buffett Oracle prompt](buffett-oracle.md)
- [Buffett Brain framework](buffett_brain.md)
- [Coverage scope](coverage_scope.md)
- [Methodology audit](methodology_audit.md)
- [Gate review](gate_review.md)
- [Company card schema](company_cards/_schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown research memo with a structured summary block; optional JSON company-card and index updates when maintaining the artifact.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses point-in-time public evidence, cached company cards, hard-gate checks, named exemptions, moat analysis, safety-margin math, and control-group comparisons.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
