## Description: <br>
Speak responses aloud on macOS using the built-in `say` command when user input indicates Voice Wake/voice recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent speak responses aloud when the current message starts with the Voice Wake recognition phrase. It is intended for macOS local text-to-speech with an optional cloud TTS fallback when local `say` is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assistant response text may be sent to a third-party TTS API when the local macOS `say` command is unavailable. <br>
Mitigation: Prefer local `say` for speech output, keep the fallback disabled unless third-party processing is acceptable, and avoid fallback use for private, credential-related, business, legal, or medical content. <br>
Risk: The cloud fallback requires `SKILLBOSS_API_KEY`, which is a sensitive credential. <br>
Mitigation: Store the API key in a secure environment variable, do not include it in prompts or logs, and remove it when cloud fallback is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quincygunter/quincy-voice-wake-say) <br>
- [SkillBoss API Hub TTS endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash or Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce spoken text locally through macOS `say`; cloud fallback requires `SKILLBOSS_API_KEY` and may return an audio URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
