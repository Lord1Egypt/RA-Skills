## Description:

SAI Creator AI turns validated OJS/PKP journal briefs into publish-ready HTML article pages, fixed-structure social carousels, optional platform captions, and handoff JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nijam727](https://clawhub.ai/user/nijam727)

### License/Terms of Use:

MIT-0

## Use Case:

External journal teams and developers use this skill to transform validated OJS/PKP intelligence briefs into accessible article pages, social carousel assets, optional captions, and structured handoff JSON for downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated article, carousel, and caption outputs unconditionally include a third-party openjournaltheme.com CTA.

Mitigation: Install the skill only when that CTA is intended, and review generated links and CTA text before publishing.

Risk: Generated SVG or HTML may carry incorrect links or text if the supplied brief contains bad source material.

Mitigation: Review generated SVG and HTML before publication, with particular attention to source attribution, outbound links, and brief-derived text.

Risk: The packaging helper could include unintended sensitive files if run against a folder that contains secrets.

Mitigation: Run packaging only on curated skill directories and exclude secrets or private working files before packaging.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nijam727/skills/sai-creator)
- [Article Template Spec](artifact/references/article-template-spec.md)
- [Carousel Spec](artifact/references/carousel-spec.md)
- [CTA Variants](artifact/references/cta-variants.md)
- [OpenJournalTheme CTA Destination](https://openjournaltheme.com/)
- [schema.org Article](https://schema.org/Article)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Files, JSON]

**Output Format:** [HTML, SVG, social caption text, and JSON handoff metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs should preserve the validated brief, include source attribution, meet WCAG AA expectations, and keep the required CTA behavior visible for review.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
