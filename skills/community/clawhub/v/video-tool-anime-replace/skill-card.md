## Description: <br>
Replace or move an element in an existing HTTPS video with WeryAI anime-style processing (video-anime-replace). Use when the user wants anime-style object replace or move on a video URL, not text-to-video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run WeryAI anime-replace or move processing on an existing public HTTPS video with a public HTTPS reference image. It is scoped to the video-anime-replace workflow and is not for text-to-video or image-to-video generation from scratch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeryAI jobs may consume credits when submitted or waited on. <br>
Mitigation: Use dry-run first and confirm the exact URLs, type, and resolution before submit or wait. <br>
Risk: The workflow sends the specified public video and image URLs to WeryAI for processing. <br>
Mitigation: Use only media URLs the user intends to share with WeryAI and confirm those URLs before submission. <br>
Risk: Exposure of WERYAI_API_KEY could allow use of the associated WeryAI account. <br>
Mitigation: Keep WERYAI_API_KEY out of files and prompts, and scope it only to the environment where the CLI is run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/video-tool-anime-replace) <br>
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt) <br>
- [Submit Video Anime Replace Task](https://docs.weryai.com/api-references/video-tools/submit-video-anime-replace-task) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown links and JSON command output from a Node.js CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, and public HTTPS video_url and image_url inputs; paid network API calls require explicit confirmation before submit or wait.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
