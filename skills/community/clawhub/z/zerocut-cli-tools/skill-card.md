## Description: <br>
Use ZeroCut CLI media and document tools. Invoke when user needs generate media, run ffmpeg/pandoc, sync resources, or save outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smartdiana](https://clawhub.ai/user/smartdiana) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to request ZeroCut CLI commands for generating images, videos, music, and speech audio, converting media and documents with ffmpeg or pandoc, syncing resources, and saving generated outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files or URLs may be synced to ZeroCut storage for processing. <br>
Mitigation: Review resource paths and URLs before running commands, and avoid syncing private or sensitive documents unless that processing is intended. <br>
Risk: Generated commands can write output files to local paths and create missing parent directories. <br>
Mitigation: Confirm output filenames and destination paths before execution. <br>
Risk: ffmpeg and pandoc argument strings can change media or document conversion behavior. <br>
Mitigation: Inspect ffmpeg, ffprobe, and pandoc arguments before running generated commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smartdiana/zerocut-cli-tools) <br>
- [Publisher profile](https://clawhub.ai/user/smartdiana) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated media or document output paths and resource sync guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
