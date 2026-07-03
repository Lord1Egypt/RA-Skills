## Description: <br>
Re-anchor long-form video timeline segments to measured voiceover word timings, rewriting segment start and end times plus audio_duration after TTS so rendered visuals stay in sync with audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pushpendrachauhan](https://clawhub.ai/user/pushpendrachauhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video pipeline operators use this skill after TTS and before final long-form rendering to align timeline segments with measured word timings and update audio_duration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script overwrites timeline and audio_duration fields in the selected job's input.json. <br>
Mitigation: Keep a backup or use version control before running the skill, and review the changed input.json before final rendering. <br>
Risk: Running the skill on the wrong job type or before measured word timings exist will fail or leave the job unreconciled. <br>
Mitigation: Run it only after TTS on schema_version 3.0-long jobs that include subtitles[].words[] measured timings. <br>
Risk: The skill depends on the local jq binary. <br>
Mitigation: Confirm jq is installed and available on PATH before executing the reconciliation script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pushpendrachauhan/skills/reconcile-timeline) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration, Guidance] <br>
**Output Format:** [Shell command execution with plain-text status output and JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mutates the selected job's input.json timeline and audio_duration fields; requires jq and schema_version 3.0-long.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
