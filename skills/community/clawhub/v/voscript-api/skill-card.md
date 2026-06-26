## Description: <br>
VoScript API helps agents operate a self-hosted speech transcription service, including audio submission, job polling, result retrieval, subtitle export, voiceprint enrollment, speaker assignment, and AS-norm cohort rebuilds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapleeve](https://clawhub.ai/user/mapleeve) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an agent to a configured VoScript server for transcription workflows, subtitle or transcript export, and voiceprint-based speaker management. It is useful when audio processing and speaker identity data must remain on a self-hosted service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads audio and manages voiceprints, which can include sensitive personal or meeting data. <br>
Mitigation: Use only trusted VoScript servers, confirm data handling expectations before upload, and treat transcription results and voiceprint identifiers as sensitive. <br>
Risk: The skill requires an API key for the configured VoScript service. <br>
Mitigation: Prefer environment variables or request headers for the API key, avoid placing keys in URLs or shell history, and rotate the key if exposure is suspected. <br>
Risk: Voiceprint management can modify or delete speaker records. <br>
Mitigation: Confirm voiceprint IDs and intended actions before rename or delete operations, especially when multiple speakers have similar names. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mapleeve/voscript-api) <br>
- [Project Homepage](https://github.com/MapleEve/voscript-skills) <br>
- [Configuration Guide](artifact/references/configuration.md) <br>
- [Job Lifecycle](artifact/references/job-lifecycle.md) <br>
- [Voiceprint Guide](artifact/references/voiceprint-guide.md) <br>
- [Export Formats](artifact/references/export-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python script invocations, API request examples, and transcript outputs in SRT, TXT, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured VoScript server URL and API key; generated outputs may include transcription text, speaker labels, voiceprint identifiers, and exported transcript files.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence; artifact metadata lists 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
