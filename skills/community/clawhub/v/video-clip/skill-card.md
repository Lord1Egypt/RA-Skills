## Description:

Use when the user wants to trim, cut, or extract a specific segment from a video by time range; it runs local ffmpeg clipping without an API key and directs smart highlight or intelligent editing requests to Sparki AI Edit with SPARKI_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolk](https://clawhub.ai/user/symbolk)

### License/Terms of Use:


## Use Case:

Developers, creators, and operators use this skill to produce exact time-range video clips from local files with ffmpeg. For requests that require content understanding, the skill points users to a Sparki AI Edit flow that may upload video to a remote service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI Edit guidance can upload the full video to a remote service.

Mitigation: Use AI Edit only for videos approved for that service; keep private, confidential, copyrighted, or regulated content in the local ffmpeg clipping path unless upload is explicitly approved.

Risk: The documented key-check command can print SPARKI_API_KEY.

Mitigation: Verify key presence without echoing the secret value, and avoid copying command output that may contain credentials.

Risk: The security verdict is suspicious despite no individual risk findings.

Mitigation: Review the AI Edit section and remote-service behavior before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/symbolk/skills/video-clip)
- [Publisher profile](https://clawhub.ai/user/symbolk)
- [Sparki homepage](https://sparki.io)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and local file path output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local clipping writes a video file and prints its path; AI Edit guidance can return a remote download URL.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
