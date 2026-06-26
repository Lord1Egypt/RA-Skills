## Description: <br>
Activates when a user explicitly asks for Chinese voice chat or Chinese voice mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liang9886703](https://clawhub.ai/user/liang9886703) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users enable this skill when they want assistant replies rewritten into natural spoken Chinese suitable for TTS or voice-model output. It focuses on short, conversational phrasing, optional local emotion tags, and mode persistence until the user disables voice mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent voice mode may continue rewriting replies after activation. <br>
Mitigation: Enable it only when the user explicitly asks for Chinese voice output, and disable it when the user asks for text replies or says to stop voice mode. <br>
Risk: A spoken style rewrite could obscure required safety refusals, warnings, or policy-sensitive guidance. <br>
Mitigation: Keep host-level safety rules authoritative; refusal and warning requirements should take priority over the voice style. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liang9886703/voice-chat-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text with optional short emotion tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contains only spoken body text and local emotion tags; no explanations, stage directions, style commentary, or analysis process.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
