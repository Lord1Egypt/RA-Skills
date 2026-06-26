## Description: <br>
How to generate video scripts for the Video Generator from user prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itspremkumar](https://clawhub.ai/user/itspremkumar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn storytelling prompts into video-generator script JSON with titles, orientation, voice selection, narration, and visual cue tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated video-script JSON can fail or produce unexpected narration if the local generator expects different file paths, voice IDs, orientation values, or visual tag syntax. <br>
Mitigation: Confirm the target generator's accepted schema and voice list before using the output, and review the generated script text so only intended narration is spoken. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itspremkumar/video-gen-script) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON entries for input/input-scripts.json with narrative text and visual tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes job fields such as id, title, orientation, voice, optional caption and fallback-video settings, and script content with [Visual: ...] tags.] <br>

## Skill Version(s): <br>
5.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
