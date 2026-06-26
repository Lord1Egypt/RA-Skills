## Description: <br>
Generate UGC-style promotional videos with AI lip-sync from a person-with-product image and pure dialogue script, using ElevenLabs voice synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and marketing teams use VEED UGC to turn a person-with-product image and pure dialogue script into a lip-synced promotional video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the selected image, image URL, dialogue script, and voice ID to ComfyDeploy for remote processing. <br>
Mitigation: Use only content that is approved for external processing, and avoid private likenesses, confidential marketing copy, or images of people without appropriate permission. <br>
Risk: A ComfyDeploy API key is required to run the skill. <br>
Mitigation: Provide the key through the documented environment variable or command option, and do not include credentials in prompts, scripts, or shared files. <br>
Risk: Local image files passed with --image are uploaded before video generation. <br>
Mitigation: Do not pass sensitive local files as --image; use only the intended image asset for the current generation task. <br>


## Reference(s): <br>
- [VEED UGC on ClawHub](https://clawhub.ai/PauldeLavallaz/veed-ugc) <br>
- [ComfyDeploy deployment queue API endpoint](https://api.comfydeploy.com/api/run/deployment/queue) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, API Calls, Guidance] <br>
**Output Format:** [MP4 video file with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ComfyDeploy API key and a user-provided image or image URL, script, and voice ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
