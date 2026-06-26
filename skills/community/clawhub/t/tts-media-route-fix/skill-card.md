## Description: <br>
Fix and verify OpenClaw TTS media-route behavior in installed dist builds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tralaleo-tralala](https://clawhub.ai/user/tralaleo-tralala) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to repair and verify OpenClaw gateway TTS media routes when generated audio URLs, MP3 serving, Bearer auth, Range requests, or temporary-file cleanup are broken. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repairing an installed OpenClaw gateway runtime can disrupt service behavior if the wrong dist file is patched or the diff is not reviewed. <br>
Mitigation: Patch only the active gateway-cli dist build, review the target file and diff, keep the .bak backup, restart deliberately, and verify with authenticated range curl. <br>
Risk: Bearer tokens used for media-route verification can be exposed through shell history, logs, or process-visible command arguments. <br>
Mitigation: Use care with real tokens during verification and avoid placing them in shell history, logs, or shared command transcripts. <br>


## Reference(s): <br>
- [TTS media-route patch checklist](references/patch-checklist.md) <br>
- [ClawHub release page](https://clawhub.ai/tralaleo-tralala/tts-media-route-fix) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tralaleo-tralala) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes backup, patch, restart, and authenticated curl verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
