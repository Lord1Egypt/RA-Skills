## Description: <br>
Generates instrumental music, vocal songs, or lyrics with Tianpuyue AI, tracks task status, and saves the results locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showtimewalker](https://clawhub.ai/user/showtimewalker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to generate background music, full songs with vocals, or lyrics for videos, games, and content workflows, then retrieve local output files and JSON metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, and voice-selection details are sent to Tianpuyue during generation. <br>
Mitigation: Use the skill only when Tianpuyue is an acceptable provider for the content, and avoid including sensitive or confidential material in prompts. <br>
Risk: Generated files, prompts, and task metadata may be written to local output and log directories. <br>
Mitigation: Set a dedicated OUTPUT_ROOT for this skill and manage that directory according to the user's retention and access-control requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/showtimewalker/tianpuyue-music) <br>
- [Voice ID map](artifact/references/voice_id_map.md) <br>
- [Tianpuyue voice selection](https://www.tempolor.com/create/song) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [JSON result objects, Markdown lyrics, and downloaded audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TIANPUYUE_API_KEY; writes generated files and logs under OUTPUT_ROOT.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
