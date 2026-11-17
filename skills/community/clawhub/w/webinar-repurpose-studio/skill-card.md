## Description:

Repurposes webinar source material into reviewable Markdown drafts for replay descriptions, short copy, social outlines, FAQ content, follow-up email drafts, and secondary content ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Content, marketing, and event operations teams use this skill after a webinar to turn supplied topics, transcripts, and highlights into structured, reviewable content assets. It is intended for draft generation and planning, not for fabricating speaker details, exposing unpublished material, or publishing directly to external systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or confidential webinar transcripts may be included in user-provided input.

Mitigation: Provide only material suitable for local processing, redact sensitive details first, and review generated drafts before sharing.

Risk: Generated repurposed content may imply unsupported facts, speaker details, or unpublished information if source material is incomplete.

Mitigation: Use the skill's待确认项 review flow and verify all names, claims, and unpublished details before publication.

Risk: The helper can write output to a user-selected local file path.

Mitigation: Use dry-run or stdout when reviewing behavior, and choose output paths deliberately to avoid overwriting unrelated files.

Risk: Dormant audit and scanning code in the package may make the behavior harder to assess.

Mitigation: Keep installation scoped to this content workflow and ask the publisher to remove or separate dormant audit/scanning paths in future releases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/webinar-repurpose-studio)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Structured Markdown draft, with optional JSON output from the local helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a chosen local output file when invoked through the bundled Python helper; otherwise returns reviewable draft content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
