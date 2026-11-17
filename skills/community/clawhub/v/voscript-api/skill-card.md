## Description:

VoScript API helps agents operate a self-hosted speech transcription service by submitting audio, tracking jobs, fetching transcripts, exporting SRT/TXT/JSON, and managing voiceprints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapleeve](https://clawhub.ai/user/mapleeve)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide agents through VoScript transcription workflows, including audio upload, job polling, transcript retrieval, subtitle export, speaker assignment, voiceprint enrollment, and AS-norm cohort rebuilds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive recordings, transcripts, API keys, and voiceprints.

Mitigation: Use it only with authorized recordings, confirm speaker consent before uploading audio or enrolling voiceprints, and keep transcripts and voiceprint data under the deployment's data handling controls.

Risk: The skill supports non-local HTTP endpoints and command-line API key arguments, which can expose traffic or secrets if used carelessly.

Mitigation: Prefer HTTPS for any non-local VoScript server and provide API keys through environment variables instead of shell history or process-visible command-line arguments.

Risk: Voiceprint rename, delete, speaker assignment, and cohort rebuild operations can change persistent server data.

Mitigation: Review target transcription IDs, segment IDs, and speaker IDs before mutation; require explicit confirmation for destructive actions such as voiceprint deletion.

## Reference(s):

- [VoScript configuration guide](references/configuration.md)
- [VoScript job lifecycle](references/job-lifecycle.md)
- [VoScript voiceprint and AS-norm guide](references/voiceprint-guide.md)
- [VoScript export formats](references/export-formats.md)
- [VoScript skills homepage](https://github.com/MapleEve/voscript-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python script invocations, REST API examples, and JSON/SRT/TXT output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or retrieve transcription artifacts such as JSON results, SRT subtitles, TXT transcripts, and server-side voiceprint records.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
