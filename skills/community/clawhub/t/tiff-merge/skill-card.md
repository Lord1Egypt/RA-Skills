## Description:

TIFF Merge & Split helps agents merge local image files into a multi-page TIFF or split a TIFF into per-page image outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to run local TIFF conversion tasks for document scans, photos, or other image sets without uploading files to a remote service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and writes local image paths supplied by the user.

Mitigation: Run it from a directory that contains only the intended images and review input and output paths before execution.

Risk: The security guidance notes that TIFF splitting and JPG/PNG support appear incomplete despite the description.

Mitigation: Verify generated files before relying on them, and treat split-mode output as needing review for this release.

Risk: The skill depends on the local Node package utif.

Mitigation: Pin utif to a reviewed version during installation when stronger supply-chain control is required.

## Reference(s):

- [ClawHub TIFF Merge & Split Skill Page](https://clawhub.ai/fly3094/skills/tiff-merge)
- [UTIF.js](https://github.com/photopea/UTIF.js)

## Skill Output:

**Output Type(s):** [shell commands, guidance, files]

**Output Format:** [Text or Markdown with shell commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local TIFF or image files at user-provided paths; the split path behavior should be verified because the security review notes incomplete functionality.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
