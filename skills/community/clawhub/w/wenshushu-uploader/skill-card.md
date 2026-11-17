## Description:

Uploads selected local files to wenshushu.cn and returns a public download link, pickup code, and optional management link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gcdd1993](https://clawhub.ai/user/gcdd1993)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to share intentionally selected local files through Wenshushu from an agent conversation or command line. It is useful when an agent needs to provide a downloadable file link and pickup code instead of attaching the file directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload arbitrary local files and produce public sharing links.

Mitigation: Confirm the exact file path before upload, use the skill only for files intended for sharing, and encrypt sensitive files before uploading.

Risk: Automatic setup can run remote installers and package installation commands.

Mitigation: Review installation commands and pinned dependencies before running setup; prefer a verified local installation when possible.

Risk: Public links, pickup codes, management links, and optional login tokens may grant access if stored or shared carelessly.

Mitigation: Limit who receives links and codes, avoid posting management links, protect local token files, and delete uploaded files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gcdd1993/skills/wenshushu-uploader)
- [Wenshushu](https://www.wenshushu.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style status text with file name, file size, public download link, pickup code, management link, and error messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated public URLs, pickup codes, and management URLs for files uploaded to wenshushu.cn.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
