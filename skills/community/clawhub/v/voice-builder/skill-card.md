## Description:

Builds a reusable voice.md by analyzing a person or brand's real writing samples so downstream social content skills can write in that voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, founders, executives, brands, and content teams use this skill to analyze real writing samples and create a reusable voice.md guide for ghostwriting and downstream social content generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided writing samples or generated calibration anchors may contain private messages, call excerpts, or sensitive drafts.

Mitigation: Use only samples the user is comfortable sharing, and review voice.md to redact sensitive snippets before storing or reusing it.

Risk: A reusable voice guide can preserve inaccurate or overconfident voice patterns when samples are thin, inconsistent, ghostwritten, or AI-generated.

Mitigation: Follow the artifact guidance to exclude weak samples, label low-confidence sections, and validate the guide with a fresh voice test before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/social-media-skills/skills/voice-builder)
- [Samples Guide](references/samples-guide.md)
- [Voice Analysis Framework](references/analysis-framework.md)
- [voice.md Template](references/voice-template.md)
- [Validation - The Voice Test](references/validation.md)
- [Examples - voice extraction, end to end](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown voice guide with evidence-backed analysis and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or refines a reusable voice.md from user-provided writing samples; may include quoted calibration snippets from those samples.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
