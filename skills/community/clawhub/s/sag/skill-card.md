## Description: <br>
ElevenLabs text-to-speech with mac-style say UX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Sag to turn text responses into ElevenLabs speech, preview voices, and produce local audio playback or MP3 output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated text and prompts may be sent to ElevenLabs for text-to-speech processing. <br>
Mitigation: Avoid sending secrets or confidential text unless ElevenLabs processing and retention terms are acceptable for the intended use. <br>
Risk: The skill requires a local sag CLI installed from a Homebrew tap and an ElevenLabs API key. <br>
Mitigation: Verify the Homebrew tap and CLI before installation, use a revocable API key, and monitor account usage or billing. <br>


## Reference(s): <br>
- [Sag homepage](https://sag.sh) <br>
- [ClawHub skill page](https://clawhub.ai/steipete/sag) <br>
- [Publisher profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and audio file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local MP3 output through the sag CLI when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
