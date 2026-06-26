## Description: <br>
Step Audiobook helps agents build and run a local audiobook workflow for voice-library management, Step official voice sync, clone voice analysis, LLM casting, replayable TTS requests, segment synthesis, and final audio export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[praanmichael](https://clawhub.ai/user/praanmichael) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent workflows use this skill to turn story text and reviewed voice-library assets into structured scripts, casting plans, replayable Step TTS requests, audio segments, and final audiobook files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story text, role and casting metadata, TTS text, and reference voice audio may be sent to Step or a configured LLM endpoint. <br>
Mitigation: Use a test or limited STEP_API_KEY, run in a private workspace, and install only when the external API data flow is acceptable. <br>
Risk: Generated voice and audio artifacts are stored locally and may contain sensitive manuscript or voice material. <br>
Mitigation: Keep generated artifacts in a private workspace and review local output locations before sharing or publishing results. <br>
Risk: Paid voice cloning can incur billing if explicitly confirmed. <br>
Mitigation: Review voice-library.yaml and clone-review.yaml, then run clone_selected_voices.py --dry-run before any paid clone. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/praanmichael/step-audiobook) <br>
- [Audiobook Workflows](artifact/references/workflows.en.md) <br>
- [Audiobook Voice Library](artifact/references/voice-library.en.md) <br>
- [Audiobook Script Format](artifact/references/script-format.en.md) <br>
- [Audiobook Casting](artifact/references/casting.en.md) <br>
- [Audiobook Synthesis](artifact/references/synthesis.en.md) <br>
- [Audiobook Editing Guide](artifact/references/editing.en.md) <br>
- [Security And External Access](artifact/references/security.en.md) <br>
- [Step reasoning endpoint](https://api.stepfun.com/step_plan/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Audio files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML and JSON artifacts, script stdout JSON, and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STEP_API_KEY plus ffmpeg and ffprobe; major intermediate artifacts are written locally for review and reruns.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
