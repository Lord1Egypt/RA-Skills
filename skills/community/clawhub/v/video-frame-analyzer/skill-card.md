## Description: <br>
Video Frame Analyzer helps an agent extract key frames from short-form drama videos, analyze them with a multimodal model, and produce structured markdown reports covering plot, cinematography, characters, dialogue, and adaptation suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roseryztzhoutong](https://clawhub.ai/user/roseryztzhoutong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content analysts, creators, and developers use this skill to deconstruct short-drama or AI-generated videos into key frames, scene notes, dialogue timelines, narrative summaries, and business adaptation recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs local Python video-processing scripts and creates frame and report files in the workspace. <br>
Mitigation: Review the output directory before execution, run the scripts in an appropriate workspace, and install dependencies from trusted package sources. <br>
Risk: Extracted frames may be provided to a multimodal model provider during analysis. <br>
Mitigation: Use only videos and frames the user is allowed to analyze, and avoid sending sensitive content to providers the user does not trust. <br>
Risk: Analyzing too many frames at once can exceed model context limits or lose intermediate observations. <br>
Mitigation: Analyze frames in small batches and write incremental markdown results before continuing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/roseryztzhoutong/video-frame-analyzer) <br>
- [smart_extract.py](artifact/references/smart_extract.py) <br>
- [extract_frames.py](artifact/references/extract_frames.py) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown reports with frame-analysis tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates frame image directories and incremental analysis files in the workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
