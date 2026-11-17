## Description:

Retrieves basic Douyin video details from a video link, including the creator, engagement counts, title, music, publication time, and image collection, but not play counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

People analyzing Douyin content can provide a video link to retrieve its basic metadata without requesting play counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or upgrade Node.js and qhkit on the user's machine.

Mitigation: Review the dependencies before use and preinstall vetted versions when possible.

Risk: Paid external data calls may incur Qinghu credits.

Mitigation: Check the estimated charge and obtain user approval before making paid calls.

Risk: Setting a qhkit API token locally may leave persistent credentials on the user's machine.

Mitigation: Provide the token through a controlled secret mechanism and review local credential storage.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-douyin-video-basic)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key management](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response with video metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Excludes play counts; reports credits charged for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
