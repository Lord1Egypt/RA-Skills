## Description: <br>
Transcribe, diarise, translate, post-process, and structure audio/video with AssemblyAI for speaker-aware transcripts, subtitles, Markdown, normalized JSON, and downstream agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run audio or video transcription workflows that need AssemblyAI-specific capabilities such as model routing, language detection, speaker diarisation, translation, structured extraction, and reusable transcript exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive audio, video, transcripts, prompts, schemas, and API keys may pass through the SkillBoss/HeyBossAI service path. <br>
Mitigation: Install only when that service path is approved; test with non-sensitive content first and avoid confidential or regulated recordings unless approved. <br>
Risk: Transcript bundles and sidecar exports can write sensitive transcript artifacts to disk. <br>
Mitigation: Review output locations such as --bundle-dir and --out, restrict access to generated files, and remove unneeded artifacts after review. <br>
Risk: The CLI includes a delete command that removes remote transcript data. <br>
Mitigation: Only allow delete when the user explicitly intends to remove the remote transcript. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-audio-transcribe) <br>
- [AssemblyAI documentation](https://www.assemblyai.com/docs) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [Capabilities reference](references/capabilities.md) <br>
- [Workflow recipes](references/workflows.md) <br>
- [Output formats](references/output-formats.md) <br>
- [Speaker mapping reference](references/speaker-mapping.md) <br>
- [LLM Gateway notes](references/llm-gateway.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown transcripts, normalized agent JSON, raw JSON, bundle manifests, subtitles, paragraph/sentence text, and CLI command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bundle mode can write multiple sidecar files; speaker-aware formatting and schema-based LLM extraction are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
