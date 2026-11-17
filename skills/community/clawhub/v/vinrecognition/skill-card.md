## Description:

Recognizes VINs from vehicle images through JisuAPI OCR and returns the VIN, validity flag, brand, and manufacturer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent workflows use this skill to extract VIN, correctness, brand, and manufacturer details from uploaded vehicle VIN images such as windshield or vehicle registration photos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local path inputs can unintentionally send non-image local files to a third-party API through symlinks.

Mitigation: Use the skill only in a controlled working directory, avoid symlink paths, and prefer base64 input from a known image.

Risk: VIN images are processed by the third-party JisuAPI service.

Mitigation: Send only images intentionally approved for third-party processing and provide a clear privacy notice before use.

Risk: Image type and size are not fully validated locally before submission.

Mitigation: Validate image type and size locally before calling the skill; the API documentation indicates image-related errors including empty, invalid, oversized, and failed-recognition cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/vinrecognition)
- [JisuAPI homepage](https://www.jisuapi.com/)
- [JisuAPI VIN recognition API](https://www.jisuapi.com/api/vinrecognition/)
- [JisuAPI VIN recognition endpoint](https://api.jisuapi.com/vinrecognition/recognize)

## Skill Output:

**Output Type(s):** [json, text, shell commands, configuration, guidance]

**Output Format:** [JSON API result or Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; accepts a base64 image or a controlled local image path.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
