## Description: <br>
Helps agents generate MiniMax videos from text prompts, source images, or first and last frames, query generation status, and save completed videos locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turbos7](https://clawhub.ai/user/turbos7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to create or query MiniMax video-generation jobs from text prompts, uploaded images, or first and last frames. The helper workflow polls job status and saves generated MP4 videos to local storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or images are sent to the MiniMax cloud video-generation service. <br>
Mitigation: Do not submit confidential, regulated, or private content unless MiniMax processing is approved for the use case. <br>
Risk: The skill requires a MiniMax API key. <br>
Mitigation: Store MINIMAX_API_KEY as a protected environment variable or scoped secret, avoid sharing it in prompts or logs, and rotate it if exposed. <br>
Risk: Generated videos remain on local disk after download. <br>
Mitigation: Review and clean the output directory when generated videos are no longer needed. <br>


## Reference(s): <br>
- [MiniMax video generation API endpoint](https://api.minimaxi.com/v1/video_generation) <br>
- [MiniMax video generation status endpoint](https://api.minimaxi.com/v1/query/video_generation?task_id={task_id}) <br>
- [MiniMax file retrieval endpoint](https://api.minimaxi.com/v1/files/retrieve?file_id={file_id}) <br>
- [ClawHub listing](https://clawhub.ai/turbos7/turbos7-minimax-video) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Files] <br>
**Output Format:** [Markdown guidance with Python and bash examples; generated MP4 files when the helper script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; generated videos are saved under ~/.openclaw/workspace/assets/videos by default.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
