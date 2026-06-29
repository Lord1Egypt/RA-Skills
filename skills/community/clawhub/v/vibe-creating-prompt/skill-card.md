## Description: <br>
Vibe Creating Prompt helps an agent decide whether a user's video-prompt request fits a Vibe Creating rewrite and, when appropriate, turns rough, emotional, single-scene, or multi-shot ideas into clearer text-to-video prompts while preserving explicit user constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alisa0808](https://clawhub.ai/user/alisa0808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, prompt engineers, and video-model users use this skill to judge whether a creative prompt benefits from Vibe Creating and to rewrite suitable ideas into concise, emotionally coherent text-to-video prompts. It is not intended for strict shot-list execution, functional demos, tutorials, or long-form dialogue synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may remove or translate technical camera parameters during a Vibe Creating rewrite. <br>
Mitigation: Tell the agent which parameters or structure must be preserved when exact execution details matter. <br>
Risk: Prompt rewriting can change emphasis in a creative brief even when no code or data access is involved. <br>
Mitigation: Review the rewritten prompt before sending it to a video model, especially for required dialogue, sound, brand, or continuity constraints. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/Alisa0808/vibe-creating-skill/tree/main/skills/vibe-creating-prompt) <br>
- [ClawHub skill page](https://clawhub.ai/alisa0808/skills/vibe-creating-prompt) <br>
- [Atlas Cloud](https://www.atlascloud.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style response with judgment, action, result, and optional notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves explicit dialogue, voiceover, music, sound effects, structure, and parameter-keep requests when the user states them.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
