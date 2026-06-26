## Description: <br>
Generates videos with TensorsLab AI video models, supporting text-to-video and image-to-video workflows with prompt enhancement, progress tracking, and local file saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bob5-tensorslab](https://clawhub.ai/user/bob5-tensorslab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create short videos from text prompts or source images through TensorsLab's API, then monitor asynchronous generation and save the resulting files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a TensorsLab account key. <br>
Mitigation: Store the key in TENSORSLAB_API_KEY, avoid passing it on the command line, and do not print full key values in logs or chat. <br>
Risk: Prompts and selected source images are sent to TensorsLab for video generation. <br>
Mitigation: Use only content approved for processing by TensorsLab and avoid submitting sensitive or restricted data. <br>
Risk: Video generation may spend account credits. <br>
Mitigation: Confirm account credit availability and expected usage before starting generation, especially for longer or higher-resolution jobs. <br>
Risk: Generated videos are saved on local disk. <br>
Mitigation: Choose an appropriate output directory and review generated files before sharing or publishing them. <br>
Risk: The script uses a session-level proxy override. <br>
Mitigation: Review the proxy setting before use on networks that require an HTTP or HTTPS proxy. <br>


## Reference(s): <br>
- [TensorsLab Video API Reference](references/api_reference.md) <br>
- [TensorsLab Console](https://tensorslab.tensorslab.com/) <br>
- [TensorsLab API](https://api.tensorslab.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/bob5-tensorslab/tl-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated videos are saved as MP4 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses asynchronous TensorsLab video tasks, polls status, and writes results to a local output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
