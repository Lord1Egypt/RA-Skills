## Description: <br>
xAI Studio - generate and edit images and videos via the xAI API. Image: text-to-image, batch generation, multi-image editing, concurrent style transfers, multi-turn chaining. Video: text-to-video, image-to-video, video editing, concurrent video edits. All from a single expandable CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[H0llyW00dzZ](https://clawhub.ai/user/H0llyW00dzZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and teams use this skill to generate, edit, batch, and chain image and video work through xAI models from an agent-driven CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, videos, and URLs selected by the user are sent to xAI for processing. <br>
Mitigation: Avoid confidential, regulated, client-owned, or personal media unless the user is authorized to send it to xAI. <br>
Risk: Generated outputs are saved locally and may contain sensitive or unintended media. <br>
Mitigation: Review the output directory after use and clean local files after sensitive work. <br>
Risk: The skill requires XAI_API_KEY to call the xAI API. <br>
Mitigation: Protect the API key and avoid exposing it in prompts, logs, shell history, or shared configuration. <br>


## Reference(s): <br>
- [xAI Studio ClawHub listing](https://clawhub.ai/H0llyW00dzZ/xai-studio) <br>
- [xAI Studio project homepage](https://github.com/H0llyW00dzZ/xai-studio-skills) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with CLI commands; generated media is saved as image or MP4 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY; sends selected prompts and media to xAI; saves outputs under media/xai-output by UTC date.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
