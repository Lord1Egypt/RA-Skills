## Description:

Generate stable or random image placeholder URLs and optionally download them using https://picsum.photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hicoldcat](https://clawhub.ai/user/hicoldcat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and documentation authors use this skill to generate reproducible Picsum placeholder image URLs for UI mockups, docs, tests, and demos. When explicitly requested, it may also help download placeholder images and report the saved paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact picsum.photos and may download placeholder images when requested.

Mitigation: Keep URL-only generation as the default, download files only on explicit request, use a user-specified or clearly stated safe path, and treat downloaded network content as untrusted.

## Reference(s):

- [Picsum Photos](https://picsum.photos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with generated URLs, selected parameters, optional file paths, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [URL-only output is the default; local file paths are included only for explicit download requests.]

## Skill Version(s):

0.1.1 (source: server release metadata, released 2026-03-18T04:52:35Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
