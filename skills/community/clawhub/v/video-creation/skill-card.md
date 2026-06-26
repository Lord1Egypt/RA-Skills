## Description: <br>
Generates short videos from a topic or voiceover script by planning copy and storyboards, using Chanjing TTS, avatar, and AI video APIs, and assembling a local MP4 with ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyuting214](https://clawhub.ai/user/zuoyuting214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and developers use this skill to turn a topic or prepared narration into a publishable short-form video with script, storyboard, digital-human narration, AI-generated scenes, and a final local MP4. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends scripts, prompts, audio, and generated media through Chanjing services. <br>
Mitigation: Use it only where Chanjing provider use is approved, and avoid confidential or regulated content unless that use is explicitly permitted. <br>
Risk: The workflow writes generated media and intermediate files to a local output directory. <br>
Mitigation: Run it in a controlled output location and apply normal retention, access control, and cleanup practices for generated assets. <br>
Risk: Default avatar, age, cultural, or ethnicity choices may be unsuitable for neutral, global, or sensitive content. <br>
Mitigation: Review and explicitly set avatar and voice selections for the audience, topic, and cultural context before publishing. <br>


## Reference(s): <br>
- [Chanjing Open API](https://open-api.chanjing.cc) <br>
- [ClawHub skill page](https://clawhub.ai/zuoyuting214/video-creation) <br>
- [README](README.md) <br>
- [Render rules](templates/render_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON workflow inputs, shell commands, and local MP4/JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Chanjing credentials plus ffmpeg and ffprobe; outputs include final_one_click.mp4, workflow_result.json, and local work files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
