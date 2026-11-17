## Description:

Convert Word documents (.docx/.doc) to high-quality JPG images with 100% formatting fidelity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxue185-png](https://clawhub.ai/user/jerryxue185-png)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert local Word documents into page-by-page JPG image files while preserving document layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Existing JPG or PNG files in the shared output folder may be deleted during conversion.

Mitigation: Review the output folder before running the skill, or use a revised version that writes each conversion to a per-run output folder.

Risk: Converted document content may remain in generated JPG files and in a predictable temporary source copy.

Mitigation: Use the skill only for documents intended for conversion and remove temporary source copies and generated images when they are no longer needed.

Risk: Unpinned dependencies can change behavior across installations.

Mitigation: Install reviewed dependency versions or prefer a revised release that pins comtypes and PyMuPDF versions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [JPG image files with brief terminal status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces page_1.jpg, page_2.jpg, and subsequent page images at JPG 95% quality in ~/.openclaw/media/outbound/word-images.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
