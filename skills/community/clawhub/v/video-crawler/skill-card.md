## Description:

Downloads videos from Douyin and Twitter/X URLs and reports either the saved file path or an error message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ly5201314gjx](https://clawhub.ai/user/ly5201314gjx)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run a command-line video downloader for Douyin and Twitter/X URLs, saving the resulting video file or receiving a clear failure message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an unrelated embedded API key that users should not inherit or redistribute.

Mitigation: The maintainer should remove and rotate the key before republishing; users should review the skill before installation.

Risk: The skill downloads media from user-provided URLs and can write to a user-provided output path.

Mitigation: Run it in a virtual environment or container, avoid administrator privileges, restrict outbound network access where possible, and provide only trusted URLs and output paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [Plain text command output and downloaded MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [On success, prints the saved output path; on failure, prints an error message.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
