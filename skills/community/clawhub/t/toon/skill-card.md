## Description: <br>
Compress JSON data to TOON format for ~40% context savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bonk-moltbot](https://clawhub.ai/user/bonk-moltbot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to compress JSON API responses or JSON files into TOON format before adding them to context. It is intended for token-saving summaries of structured data while preserving access to raw JSON when exact machine-readable output is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends installing or invoking a toon executable through npm tooling. <br>
Mitigation: Verify the actual toon executable or @toon-format/cli npm package before adding it to PATH. <br>
Risk: TOON compression may be unsuitable when downstream tooling requires exact raw JSON. <br>
Mitigation: Request or retain raw JSON whenever exact machine-readable output is required. <br>


## Reference(s): <br>
- [TOON format specification](https://toonformat.dev) <br>
- [ClawHub skill page](https://clawhub.ai/bonk-moltbot/toon) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and TOON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for piping JSON through the toon CLI; non-JSON command output is described as passing through unchanged.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
