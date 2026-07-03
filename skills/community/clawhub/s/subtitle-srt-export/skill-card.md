## Description: <br>
Export a standard .srt subtitle file from measured word timings in a job's input.json, grouping words into readable subtitle cues and writing subtitles.srt without making API calls or modifying input.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pushpendrachauhan](https://clawhub.ai/user/pushpendrachauhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to turn measured OpenClaw job word timings into a ready-to-upload SRT subtitle file for platforms such as YouTube. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the script on a job folder can create or overwrite subtitles.srt in that folder. <br>
Mitigation: Run it only on job folders where updating subtitles.srt is intended, as noted in the security guidance. <br>
Risk: The skill depends on measured word timings already being present in input.json. <br>
Mitigation: Run the timing-producing workflow first and treat a missing-timings error as a precondition failure rather than a successful export. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pushpendrachauhan/skills/subtitle-srt-export) <br>
- [Input timing producer: elevenlabs-tts](../elevenlabs-tts/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [SRT subtitle file plus a short shell status message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and awk. Reads <job>/input.json and writes or overwrites <job>/subtitles.srt in the same job folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
