## Description:

Converts Chinese WeChat public-account articles and supplied images into publish-ready vertical WeChat Channels video packages with narration, subtitles, covers, storyboard and timeline files, publish copy, and QA checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Content producers, developers, and agent operators use this skill to transform Chinese WeChat articles, especially enterprise, product, medical, and pharma source material, into factual 9:16 video packages with synchronized narration and delivery QA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The video workflow may run an unpinned external rendering CLI.

Mitigation: Pin or preinstall the renderer tooling in a contained project workspace before using the skill for release work.

Risk: Weak asset path validation could expose files outside the intended project when processing untrusted storyboards.

Mitigation: Use trusted storyboard files, keep assets project-relative, and run storyboard validation before TTS or rendering.

Risk: Medical or pharma videos can become misleading if source claims, dosage forms, indications, or disclaimers are expanded beyond the supplied article.

Mitigation: Maintain a content brief with source references for factual claims and verify the final narration, on-screen text, CTA, and disclaimer during delivery QA.

## Reference(s):

- [Content And Compliance](references/content-and-compliance.md)
- [Vertical Layout System](references/layout-system.md)
- [Storyboard And Timeline Schema](references/storyboard-schema.md)
- [Delivery QA](references/qa.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON manifests, shell commands, and generated media-package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a 1080x1920 video package with storyboard, timeline, captions, voiceover, cover, publish copy, QA report, and contact sheet.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
