## Description: <br>
Produce modular scene-based videos from slide deck source and per-scene narration audio, including Playwright slide rendering, Kokoro narration generation, per-scene clip generation, and final stitching through an editable order file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media-production teams use this skill to turn a slide deck and per-scene narration manifest into modular video scenes that can be reordered, spliced, and stitched without rerendering the full video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local media scripts read from and write to project directories, including generated audio, scene clips, order files, and final video outputs. <br>
Mitigation: Run the skill only on trusted project directories and review manifest.csv plus scene-order.txt before execution. <br>
Risk: The Kokoro narration step may make outbound network requests on first run if model weights are not already cached. <br>
Mitigation: Pre-cache or verify Kokoro model weights before use in environments that must avoid outbound network access. <br>
Risk: ffmpeg commands overwrite generated media outputs during scene building and stitching. <br>
Mitigation: Keep source slide, narration, and manifest files separate from generated output directories and preserve backups of outputs that must not be replaced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/scene-video-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/nissan) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and directory conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local generation of audio files, scene clips, scene-order files, and a stitched first-cut video.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
