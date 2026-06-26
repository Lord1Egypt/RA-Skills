## Description: <br>
Speak responses aloud on macOS using the built-in `say` command when user input indicates Voice Wake/voice recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xadenryan](https://clawhub.ai/user/xadenryan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to have an agent speak voice-triggered responses aloud on macOS using local text-to-speech. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive responses may be overheard when spoken aloud. <br>
Mitigation: Use the skill only in settings where audible assistant responses are acceptable, and avoid it for sensitive content. <br>
Risk: The skill only works where the macOS `say` command is available. <br>
Mitigation: Confirm the agent is running on macOS before relying on spoken output; otherwise continue with text-only responses. <br>


## Reference(s): <br>
- [Voice Wake Say on ClawHub](https://clawhub.ai/xadenryan/voice-wake-say) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Text or Markdown response with optional local macOS `say` shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Spoken text should omit markdown and code blocks; long or code-heavy responses should be summarized aloud.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
