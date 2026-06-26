## Description: <br>
Guide for SenseAudio voice selection, plan-level voice entitlement checks, and cloned voice usage constraints in TTS calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support agents use this skill to troubleshoot SenseAudio TTS voice availability, account-tier entitlements, cloned voice usage, and dictionary/model constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice entitlement or model compatibility guidance may become stale as SenseAudio account tiers, voice lists, and TTS model behavior change. <br>
Mitigation: Verify current voice entitlements and model compatibility against official SenseAudio materials before changing production TTS behavior. <br>
Risk: Troubleshooting TTS accounts can expose unnecessary account details or secrets if users overshare context. <br>
Mitigation: Ask only for the minimum voice ID, account tier, and model information needed, and avoid collecting account secrets. <br>


## Reference(s): <br>
- [SenseAudio Voice ClawHub page](https://clawhub.ai/scikkk/senseaudio-voice) <br>
- [Voice and Cloning Reference](references/voice.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown guidance with configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference-only guidance; no code, shell commands, credential handling, or installation scripts are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
