## Description: <br>
Generate images & videos with ZenMux. Support multiple image models (Gemini, Qwen, Hunyuan, etc.) and video models (Veo, Seedance) via one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theopenbase](https://clawhub.ai/user/theopenbase) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to generate images and video tasks through ZenMux's unified API, configure ZENMUX_API_KEY, and run the bundled CLI for image generation, video task creation, status polling, and media download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a ZenMux API key and sends prompts or optional reference image URLs to ZenMux. <br>
Mitigation: Use a dedicated key, monitor billing or quota, and avoid sensitive prompts or private signed URLs. <br>
Risk: Generated images or videos can be written to local paths chosen by the user or agent. <br>
Mitigation: Choose output paths deliberately and review generated or downloaded media before reuse. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/theopenbase/zenmux-media-gen) <br>
- [Publisher profile](https://clawhub.ai/user/theopenbase) <br>
- [ZenMux homepage](https://zenmux.ai) <br>
- [ZenMux API base endpoint](https://api.zenmux.ai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API calls, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with bash and Python command examples; generated media can be saved as image or video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, and ZENMUX_API_KEY; image/video generation sends prompts and optional reference image URLs to ZenMux.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
