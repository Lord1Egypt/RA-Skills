## Description: <br>
Generate videos from text prompts or reference images using OpenAI Sora. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative operators use this skill to generate MP4 videos from text prompts or animate a reference image through OpenAI Sora, with controls for model, duration, resolution, and output file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images are sent to OpenAI for video generation. <br>
Mitigation: Avoid sensitive prompts or images and install only when this external API use is acceptable. <br>
Risk: An OpenAI API key is required and could be exposed if passed directly on the command line. <br>
Mitigation: Prefer the OPENAI_API_KEY environment variable over the --api-key argument. <br>
Risk: The requested output filename may overwrite an unintended local file. <br>
Mitigation: Set --filename to an intended output path before running the script. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PauldeLavallaz/sora) <br>
- [OpenAI Videos API Endpoint](https://api.openai.com/v1/videos) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated videos are saved as MP4 files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenAI API key, a text prompt, an output filename, and optional reference image, duration, model, size, and polling interval settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
