## Description: <br>
Generates a complete story video from images, text prompts, or mixed inputs, with selectable duration and visual style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and teams use this skill to turn one or more images, a text description, or mixed inputs into a short story video with generated script, reference imagery, video segments, background music, and a composed final MP4. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct the agent to install FFmpeg with system package managers, including sudo paths, without explicit user approval. <br>
Mitigation: Require explicit user approval before installing or changing system packages, or run the skill in an environment where FFmpeg is already installed. <br>
Risk: The skill writes generated assets under output/ and may overwrite existing files in that directory. <br>
Mitigation: Run it in a dedicated workspace or confirm that files under output/ can be replaced before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/yq-story-video-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown responses with deliver_assets blocks plus generated JSON, image, audio, and MP4 files under output/.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a 48-second 768P video made from six-second segments; 24-second and 72-second durations are also supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
