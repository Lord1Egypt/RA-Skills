## Description:

Calls Tencent Cloud LicensePlateOCR to locate and recognize mainland China vehicle license plates from image URLs or Base64 image input, returning plate number, color, confidence, category, coordinates, and multi-plate results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to submit intended vehicle images or trusted image URLs to Tencent Cloud OCR and receive structured license-plate recognition results for automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local-file image input can upload arbitrary readable files to Tencent Cloud if an agent selects paths automatically or receives unintended file paths.

Mitigation: Run in a restricted environment, pass only intended vehicle images or trusted image URLs, and avoid allowing autonomous path selection.

Risk: The skill sends vehicle images or image URLs to a third-party cloud OCR service.

Mitigation: Use least-privilege Tencent Cloud credentials and ensure users understand that submitted images are processed by Tencent Cloud.

Risk: The security verdict is suspicious pending stronger input validation, clearer third-party data disclosure, and pinned dependencies.

Mitigation: Review before installing and require the publisher to add image validation, data-disclosure documentation, and pinned dependencies before treating the skill as low risk.

## Reference(s):

- [Tencent Cloud LicensePlateOCR API Documentation](https://cloud.tencent.com/document/api/866/36211)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON results with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials and either an image URL or Base64 image input; successful results may include request IDs, confidence scores, colors, categories, coordinates, and multi-plate entries.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
