## Description: <br>
Multilingual TTS via Typecast CLI with emotion control. Plays audio aloud or saves to file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaebong-human](https://clawhub.ai/user/jaebong-human) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to generate or save multilingual Typecast text-to-speech audio with voice, model, language, and emotion controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external Typecast CLI and a Typecast API key. <br>
Mitigation: Install only if the Typecast CLI is trusted, keep TYPECAST_API_KEY protected, and remove stored credentials when no longer needed. <br>
Risk: Text passed to the CLI may be sent to a cloud service. <br>
Mitigation: Avoid submitting secrets, private documents, or regulated data unless Typecast's handling terms are acceptable. <br>
Risk: Credentials or defaults may be stored in ~/.typecast/config.yaml. <br>
Mitigation: Protect or remove ~/.typecast/config.yaml when the configuration is no longer required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaebong-human/typecast) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of the external Typecast CLI and TYPECAST_API_KEY; generated audio may be played aloud or saved as wav or mp3 by the CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
