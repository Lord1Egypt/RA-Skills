## Description:

Binary classification-based human portrait segmentation for complete body contour recognition and image matting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neck-cn](https://clawhub.ai/user/neck-cn)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to send a portrait image or image URL to Tencent Cloud's SegmentPortraitPic API and return image matting results. It is intended for workflows that need a segmented portrait image and mask URL rather than model-generated guesses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portrait images or image URLs are sent to Tencent Cloud for processing.

Mitigation: Use the skill only for images approved for Tencent Cloud processing, and avoid submitting sensitive portraits unless the workflow has appropriate consent and privacy review.

Risk: The script can install an unpinned Tencent SDK dependency at runtime.

Mitigation: Install a pinned, reviewed Tencent SDK in the execution environment before use and disable or review runtime dependency installation.

Risk: Tencent Cloud credentials are required and may be long-lived if stored in shell startup files.

Mitigation: Use narrowly scoped credentials, prefer temporary/session credentials where available, and avoid storing secrets in persistent shell profile files.

## Reference(s):

- [SegmentPortraitPic API Reference](references/SegmentPortraitPicApi.md)
- [Tencent Cloud SegmentPortraitPic Documentation](https://cloud.tencent.com/document/product/1208/42970)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Tencent Cloud result image and mask URLs when successful; errors are returned as JSON.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
