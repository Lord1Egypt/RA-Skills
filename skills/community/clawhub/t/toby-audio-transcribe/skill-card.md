## Description:

Transcribes, diarises, translates, post-processes, and structures audio/video with AssemblyAI into agent-friendly Markdown, JSON, subtitle, and bundle outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run AssemblyAI-specific transcription workflows for local files or media URLs, including speaker labels, speaker naming, language detection, translation, structured extraction, and reusable transcript exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive recordings, media URLs, transcript text, prompts, and schemas may be sent through the SkillBoss/HeyBoss API hub and AssemblyAI.

Mitigation: Use only approved media and prompts; avoid confidential, regulated, or consent-sensitive recordings unless that processing path is approved.

Risk: The skill documentation may read like direct AssemblyAI processing while server security evidence flags an additional API hub processing path.

Mitigation: Review the processing path before installation and disclose or approve the external services involved before use.

Risk: Custom base URLs can redirect audio, transcript, prompt, or schema data to an untrusted destination.

Mitigation: Pass custom base URLs only when the destination is explicitly trusted and approved for the data being processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-audio-transcribe)
- [AssemblyAI documentation](https://www.assemblyai.com/docs)
- [AssemblyAI capabilities reference](references/capabilities.md)
- [Workflow recipes](references/workflows.md)
- [Output formats](references/output-formats.md)
- [Speaker mapping reference](references/speaker-mapping.md)
- [LLM Gateway notes](references/llm-gateway.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands; generated artifacts may include Markdown transcripts, normalized agent JSON, raw JSON, text, SRT, VTT, and manifest files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, internet access, and SKILLBOSS_API_KEY; bundle mode writes multiple transcript sidecar files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
