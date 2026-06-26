## Description: <br>
Generates Chinese speech with Qwen3-TTS through ComfyUI, supporting voice cloning, designed character voices, multi-role dialogue workflows, and Edge TTS fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to synthesize role-based Chinese speech for agent workflows, stories, and dialogue. It is especially suited to workflows that need local Qwen3-TTS generation with a configurable fallback path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synthesis text can leave the local machine through a configurable ComfyUI endpoint or the automatic cloud fallback. <br>
Mitigation: Keep COMFYUI_URL set to localhost or a trusted ComfyUI server, and use --fallback-edge false for sensitive text. <br>
Risk: Voice cloning can process reference audio that may require authorization or consent. <br>
Mitigation: Use voice cloning only with audio you are authorized to process and publish. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/tts-qwen3) <br>
- [Publisher profile](https://clawhub.ai/user/vincentlau2046-sudo) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Voice preset configuration](artifact/presets/voices.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration details; runtime generation produces WAV audio files and optional SRT subtitle paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configurable ComfyUI endpoint and can fall back to Edge TTS when local Qwen3-TTS generation fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
