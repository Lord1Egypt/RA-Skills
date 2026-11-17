## Description:

Create, modify, or repair Tesla in-car custom wrap PNGs (UV unwrapped textures) — handling vehicle template selection, on-car orientation, mirrored numerals, logo removal, graphic cropping, incomplete images, the 1 MB per-image limit, and batch ZIP delivery. Use when the user asks for Tesla custom wraps, Model Y wraps, or editing an existing wrap; not for physical vinyl production cutter templates or for generating car render photos only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albert-lv](https://clawhub.ai/user/albert-lv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create or repair custom Tesla in-car wrap textures from the matching official UV template, then check file integrity, visual completeness, and panel orientation before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images may be sent to the selected image-generation provider.

Mitigation: Use only reference images the user is comfortable sharing with that provider.

Risk: Passing PNG validation can be mistaken for proof that template geometry or on-car orientation is correct.

Mitigation: Check template boundaries separately and verify panel orientation in-car; report any untested stage as unverified.

## Reference(s):

- [Tesla custom-wraps template and instructions](https://github.com/teslamotors/custom-wraps)
- [Prompt patterns](references/prompt-patterns.md)
- [Failure modes and safeguards](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Files, Guidance, Shell commands]

**Output Format:** [PNG wrap images and ZIP archives, with concise Markdown status and validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-image size limits and separate reporting of file, template geometry, and in-car orientation checks]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
