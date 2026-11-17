## Description:

Produces a branded Psyke SEO and GEO audit deck for a website, with dual scoring, competitor benchmarking, AI citation analysis, and Psyke-branded dark-mode slides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beebeebot](https://clawhub.ai/user/beebeebot)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing and SEO practitioners can use this skill to create client-facing Psyke audit decks that collect website evidence, score SEO and GEO readiness, benchmark competitors, and propose specific fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client audit material may be published publicly without a clear consent or review gate.

Mitigation: Require explicit client approval, review staged files before deployment, and prefer private or access-controlled publishing.

Risk: Website crawling and external AI or search tools may expose client information beyond the audit workspace.

Mitigation: Confirm client approval before collection, limit sensitive inputs, and verify findings before sharing the deck.

Risk: Unpinned deployment tooling can change behavior between audit runs.

Mitigation: Pin deployment tooling where possible and review generated output before release.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/beebeebot/skills/psyke-audit)
- [Scoring methodology](artifact/references/scoring.md)
- [GEO assessment framework](artifact/references/geo-framework.md)
- [Slide structure](artifact/references/slide-structure.md)
- [Psyke theme CSS](artifact/references/psyke-theme.css)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [HTML slide deck, Markdown summaries, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single index.html deck for Vercel deployment with SEO and GEO scores, issue evidence, benchmark sections, and an action plan.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
