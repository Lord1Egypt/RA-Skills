## Description:

Runs the video-skill pipeline to convert narrated videos into structured step data, enriched timeline-ready outputs, and markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelgold](https://clawhub.ai/user/michaelgold)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to process narrated instructional videos into structured steps, visually grounded timeline metadata, and markdown guides while validating provider connectivity and model-backed enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured AI endpoints may receive sensitive video, audio, transcript, and frame data.

Mitigation: Use providers with acceptable privacy and retention controls, and avoid private or regulated videos unless those controls are approved.

Risk: Model deployment examples can expose unauthenticated services or send data over plaintext HTTP.

Mitigation: Bind local services to localhost or protect them with authentication, TLS, firewall rules, and rate limits; prefer HTTPS for non-local providers.

Risk: AI extraction and enrichment can produce incorrect or misleading step guidance.

Mitigation: Review generated step data, markdown, and error manifests before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michaelgold/skills/video-skill)
- [uv documentation](https://docs.astral.sh/uv/)
- [OpenTimelineIO documentation](https://readthedocs.org/projects/opentimelineio-deb/downloads/pdf/latest/)
- [DaVinci Resolve 18.5 features guide](https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_18.5_New_Features_Guide.pdf?_v=1681801210000)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSONL or Markdown file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, ffmpeg, and python3; AI modes use configured transcription, reasoning, and vision-language endpoints.]

## Skill Version(s):

0.1.2 (source: server release evidence; artifact pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
