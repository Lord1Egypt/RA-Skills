## Description: <br>
Generates a single chat-ready meme image from speech-recognition text or polished text, choosing a meme style from the text tone and using doubao-seedream-4-5-251128 as the default image model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hei-MaoM](https://clawhub.ai/user/Hei-MaoM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn short voice-input text into a single meme, sticker, or caption-ready image for chat experiences. It can produce an image with embedded Chinese caption text or a caption-free image with a separate caption template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text is sent to the configured image model provider. <br>
Mitigation: Use a dedicated model API key, review the configured base URL before running it, and avoid sending private, confidential, or credential-like text unless the provider is trusted. <br>
Risk: Generated meme images are saved locally and may contain user text. <br>
Mitigation: Choose an output directory where saved meme images are acceptable for the deployment environment. <br>
Risk: Dependency resolution may change runtime behavior over time. <br>
Mitigation: Install from pinned or locked dependencies in stricter environments. <br>


## Reference(s): <br>
- [Image model API integration notes](references/api_cn.md) <br>
- [Input-method integration notes](references/integration_cn.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the generation script plus a saved JPEG image path; template mode also includes caption-template JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEME_MODEL_API_KEY for the configured OpenAI-compatible image API. Defaults to saving one .jpg image under meme_outputs or a caller-provided output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
