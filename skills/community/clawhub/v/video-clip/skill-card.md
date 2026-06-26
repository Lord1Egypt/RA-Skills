## Description: <br>
Trims, cuts, or extracts precise video segments by time range locally with ffmpeg, with guidance to use AI Edit for smart highlight extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Symbolk](https://clawhub.ai/user/Symbolk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to clip local video files to exact time ranges and receive the output file path. When a request requires content-aware highlight selection, it directs users to a separate AI editing flow rather than performing that locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AI Edit workflow can upload video files to an external service. <br>
Mitigation: Use the local ffmpeg clipping path for private media unless the external endpoint, retention policy, and access controls have been reviewed. <br>
Risk: The documented key-check command can reveal whether SPARKI_API_KEY is configured in logs or shared terminal output. <br>
Mitigation: Avoid running credential checks in logged or shared environments, and handle SPARKI_API_KEY as a secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Symbolk/video-clip) <br>
- [Publisher profile](https://clawhub.ai/user/Symbolk) <br>
- [Sparki homepage](https://sparki.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; the local clipping script returns the clipped file path on stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg for local clipping; the documented AI Edit path requires SPARKI_API_KEY and may upload video to an external service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
