## Description: <br>
Convert text to natural speech with DIA TTS, Kokoro, Chatterbox, and more via inference.sh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, content teams, and accessibility workflows use this skill to generate voiceovers, audiobooks, podcasts, IVR prompts, video narration, and other speech outputs from text through the inference.sh CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing a remote CLI can expose users to supply-chain or installer trust risk. <br>
Mitigation: Install only if inference.sh and the infsh CLI are trusted; prefer manual installation with checksum verification when stronger assurance is needed. <br>
Risk: Text, private URLs, media inputs, or cloned voices may be submitted to a hosted inference service. <br>
Mitigation: Avoid confidential text, regulated data, private URLs, or cloned voices without permission and an acceptable data-handling arrangement. <br>


## Reference(s): <br>
- [Text To Speech on ClawHub](https://clawhub.ai/okaris/text-to-speech) <br>
- [inference.sh](https://inference.sh) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Apps Overview](https://inference.sh/docs/apps/overview) <br>
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide remote inference runs that return generated audio URLs or JSON responses through the infsh CLI.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
