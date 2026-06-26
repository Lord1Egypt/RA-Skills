## Description: <br>
Generate videos using TensorsLab's AI video generation models, including text-to-video and image-to-video workflows with prompt enhancement, progress tracking, and local file saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bob5-tensorslab](https://clawhub.ai/user/bob5-tensorslab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to generate short videos from text prompts or source images through the TensorsLab API. It is suited for cinematic clips, social-format videos, animated still images, and quick previews when the user has a TensorsLab API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected source images may be sent to TensorsLab for video generation. <br>
Mitigation: Use the skill only with content that is appropriate to share with TensorsLab. <br>
Risk: Passing an API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Set TENSORSLAB_API_KEY as an environment variable instead of using the --api-key flag. <br>
Risk: Generated MP4 files are saved locally and may consume significant disk space. <br>
Mitigation: Choose an output directory with enough available storage and remove unneeded generated files. <br>


## Reference(s): <br>
- [TensorsLab Video API Reference](references/api_reference.md) <br>
- [TensorsLab API](https://api.tensorslab.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/bob5-tensorslab/tensorslab-video) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Files] <br>
**Output Format:** [Markdown guidance with shell commands and locally saved MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated videos are saved to a local output directory; task completion may take several minutes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
