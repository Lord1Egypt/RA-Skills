## Description: <br>
Run the video-skill pipeline to convert narrated videos into structured step data and enriched timeline-ready outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelgold](https://clawhub.ai/user/michaelgold) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical content teams use this skill to turn narrated videos into structured step data, visual enrichment outputs, and rendered Markdown guides. It also supports provider connectivity checks and staged debugging for transcription, chunking, extraction, frame sampling, and enrichment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive video, transcript, or frame data may be sent to configured AI services. <br>
Mitigation: Use local or approved provider endpoints and avoid private, proprietary, or regulated media unless processing is authorized. <br>
Risk: The local model Docker setup exposes unauthenticated services broadly by default. <br>
Mitigation: Bind Docker services to localhost or add authentication and firewall controls before starting the model stack. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michaelgold/video-skill) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [OpenTimelineIO documentation](https://readthedocs.org/projects/opentimelineio-deb/downloads/pdf/latest/) <br>
- [DaVinci Resolve 18.5 new features guide](https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_18.5_New_Features_Guide.pdf?_v=1681801210000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; pipeline outputs include JSON, JSONL, and Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged transcript, segment, chunk, step, frame-manifest, enrichment, optional error-manifest, and rendered Markdown artifacts.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata; artifact pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
