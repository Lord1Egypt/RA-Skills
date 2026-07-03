## Description: <br>
Generate videos via Google Cloud Vertex AI predictLongRunning (Veo) using Application Default Credentials (ADC). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neogeosnk](https://clawhub.ai/user/neogeosnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to generate text-to-video or image-to-video outputs through Google Cloud Vertex AI using local Google Cloud credentials and curl. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw Google Vertex AI responses may be saved to predictable files in the shared temp directory, which can expose sensitive prompts, source-image data, response data, or generated-video details on shared machines. <br>
Mitigation: Use the skill only in trusted environments for sensitive work, remove temporary debug files after use, or modify the script to disable debug persistence or write debug files to private per-run locations with restrictive permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neogeosnk/vertex-video-adc) <br>
- [Publisher profile](https://clawhub.ai/user/neogeosnk) <br>
- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown usage guidance, JSON status responses, and generated video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gcloud and curl, Google Cloud authentication, a project ID, and prompt input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
