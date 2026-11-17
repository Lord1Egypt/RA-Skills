## Description:

Batch-generates first-frame image prompts and image-to-video storyboard prompts for AI short drama and comic drama, with character consistency anchors, 9:16 vertical shot vocabulary, six model dialects, and CSV/JSON batch export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plinkchan](https://clawhub.ai/user/plinkchan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, short-drama studios, and developers use this skill to turn scripts or rough storyboard tables into model-specific prompt packs for AI short drama and comic drama production. It is suited for batch storyboard prompt generation, character consistency planning, dialect-specific prompt formatting, and local CSV/JSON manifest export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated manifest.csv can contain user-supplied storyboard values that spreadsheet software may interpret as formulas.

Mitigation: Prefer manifest.json for exact review, and sanitize formula-like CSV cells before opening generated manifests in spreadsheet software.

Risk: Untrusted or malformed storyboard CSV input can produce incorrect prompt scaffolds or validation failures.

Mitigation: Use trusted storyboard CSV inputs when possible and run the exporter validation before batch generation.

Risk: Model-specific duration, resolution, and reference-image limits can change outside the skill package.

Mitigation: Confirm the target model, output language, and current official model settings before generating or exporting a full prompt pack.

Risk: User-provided scripts, story text, or visual concepts may be copyrighted or unauthorized.

Mitigation: Use owned, licensed, or public-domain source material and pause for review when the source rights are unclear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/plinkchan/skills/short-drama-storyboard-pipeline)
- [Storyboard Table Spec](artifact/references/storyboard-spec.md)
- [Consistency Anchor](artifact/references/consistency-anchor.md)
- [Shot Vocabulary for 9:16 Vertical Drama](artifact/references/shot-vocabulary.md)
- [Model Dialects](artifact/references/model-dialects.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, CSV/JSON manifests, per-shot prompt text files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Python 3.8+ stdlib exporter validates storyboard CSV inputs and emits per-shot prompt scaffolds plus manifest.csv and manifest.json.]

## Skill Version(s):

1.0.2 (source: frontmatter, README, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
