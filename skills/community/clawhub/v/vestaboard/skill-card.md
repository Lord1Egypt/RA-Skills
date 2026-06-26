## Description: <br>
Read and write messages on a Vestaboard using the Vestaboard Cloud API and optional legacy read-write endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SeidProjects](https://clawhub.ai/user/SeidProjects) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent preview, read, and update a Vestaboard with short text messages or predefined 6x22 numeric layouts. It is suited for status boards, simple signage, and small pixel-art displays backed by user-provided Vestaboard credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update a physical Vestaboard when valid credentials are present. <br>
Mitigation: Install it only for agents that should read and update that board, and review messages or layouts before write operations when board content matters. <br>
Risk: Vestaboard credentials could be exposed if tokens are pasted into prompts, logs, or committed files. <br>
Mitigation: Provide VESTABOARD_TOKEN or VESTABOARD_RW_KEY through environment secrets and keep credentials out of prompts, logs, and commits. <br>
Risk: Changing VESTABOARD_API_BASE or supplying unknown layout files can send board data to an unintended endpoint or display unexpected content. <br>
Mitigation: Keep VESTABOARD_API_BASE pointed at a trusted Vestaboard endpoint and use write-layout only with known 6x22 layout JSON files. <br>


## Reference(s): <br>
- [Vestaboard Cloud API](https://cloud.vestaboard.com/) <br>
- [Vestaboard Character Codes](https://docs.vestaboard.com/docs/characterCodes/) <br>
- [Formatting Notes](references/formatting.md) <br>
- [Character Codes Reference](references/character-codes.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/SeidProjects/vestaboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON layout files, and plain text board previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formats text for a 6 row by 22 column Vestaboard layout and can emit or send JSON layout payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
