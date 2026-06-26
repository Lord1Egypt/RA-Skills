## Description: <br>
Translate SRT subtitle files into any target language using AI while preserving SRT timing and format and writing a translated SRT output file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate movie or video subtitle files into a chosen target language while keeping subtitle IDs, timecodes, and SRT structure intact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subtitle files may contain private or sensitive dialogue that is sent through the user's configured AI translation provider. <br>
Mitigation: Review subtitle content and provider settings before translation, and avoid processing private files with providers that are not approved for that data. <br>
Risk: A translated output file could overwrite or be mistaken for an important subtitle file. <br>
Mitigation: Check the output filename and directory before running the helper scripts on important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcbaivn/subtitle-translator-mcbai) <br>
- [MCB AI publisher profile](https://clawhub.ai/user/mcbaivn) <br>
- [MCB AI](https://www.mcbai.vn) <br>
- [OpenClaw cheatsheet](https://openclaw.mcbai.vn) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python helper commands and generated SRT subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided SRT subtitle files, can parse subtitle text to JSON for translation, and writes translated UTF-8 SRT output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
