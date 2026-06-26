## Description: <br>
Generates short AI-assisted music videos from melody audio, a photo, and a prompt using a local Node/Express app with Ollama scene descriptions and FFmpeg video rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GBlockChainNetwork](https://clawhub.ai/user/GBlockChainNetwork) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and operators can use this skill to scaffold and run a local media-generation service that accepts audio, image, and prompt inputs and returns scene text plus an MP4 clip. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The app exposes an unauthenticated network upload endpoint that runs FFmpeg on user-supplied media. <br>
Mitigation: Add authentication, upload type and size limits, rate limits, FFmpeg sandboxing, and cleanup for failed requests before VPS or network deployment. <br>
Risk: The browser UI renders generated response content with innerHTML. <br>
Mitigation: Use safe DOM rendering for generated scenes, links, and error messages before exposing the app to untrusted users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GBlockChainNetwork/vibeclip) <br>
- [Publisher profile](https://clawhub.ai/user/GBlockChainNetwork) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell commands; the generated app returns JSON containing scene text and MP4 video links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, Ollama, and FFmpeg; the app uses local file uploads and generated media files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
