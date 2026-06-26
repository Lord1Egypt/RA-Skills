## Description: <br>
Record broadcast FM stations from an RTL-SDR using a reliable IQ-capture workflow with offline WBFM demodulation, RDS station-name extraction, and automatic MP3 naming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igrikxd](https://clawhub.ai/user/igrikxd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scan broadcast FM with RTL-SDR hardware, decode RDS station names, record selected stations, and return MP3 files with station, frequency, and timestamp naming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local SDR and media-processing commands and can save radio recordings and metadata to disk. <br>
Mitigation: Use an explicit output directory, monitor disk use during long or multi-station recordings, and review generated MP3 and JSON files before sharing them. <br>
Risk: RDS station naming depends on local tooling, especially redsea, and may fall back to UnknownStation when dependencies or signal quality are insufficient. <br>
Mitigation: Run the documented check and staged decode workflow before recording, and inspect diagnostic JSON when station naming fails. <br>


## Reference(s): <br>
- [Pipeline Notes](references/pipeline-notes.md) <br>
- [ClawHub Release Page](https://clawhub.ai/igrikxd/rtl-sdr-fm-rds-recorder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON command output descriptions, and generated MP3 file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local MP3 recordings and JSON metadata through the referenced scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
