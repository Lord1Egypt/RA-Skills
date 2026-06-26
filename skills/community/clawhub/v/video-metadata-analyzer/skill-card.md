## Description: <br>
Analyzes video files by extracting frames and audio, using visual and transcription analysis, and generating structured Bilibili publishing metadata such as title, intro, tags, category, and cover suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberkurry](https://clawhub.ai/user/cyberkurry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and publishing workflow operators use this skill to turn a source video into structured Bilibili publishing metadata. It is suited for video metadata analysis, publish preparation, and upstream handoff to a Bilibili publishing automation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video frames, audio, transcripts, and derived metadata can be sent to configured external LLM endpoints in API modes. <br>
Mitigation: Use local or agent-direct modes for confidential, regulated, or sensitive media; verify endpoint trust and retention policy before using API modes. <br>
Risk: The skill requires sensitive credentials for full API-based analysis. <br>
Mitigation: Provide credentials only through approved runtime configuration and avoid exposing keys in chat or published artifacts. <br>
Risk: Generated observations or publishing metadata may be inaccurate or unsuitable for direct publication. <br>
Mitigation: Review agent-mode prompt output and generated metadata before passing it to another agent or publishing pipeline. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberkurry/video-metadata-analyzer) <br>
- [Video Metadata Analyzer Technical Reference](references/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Files, Guidance] <br>
**Output Format:** [JSON files for visual observations, audio observations, and synthesized metadata, with optional Markdown for manual review.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include extracted frame and audio files when agent-direct or keep-frame modes are used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
