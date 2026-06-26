## Description: <br>
Verify and cross-sign the active Matrix device for one OpenClaw-managed account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlumeau](https://clawhub.ai/user/mlumeau) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to repair Matrix device trust, confirm that the current device is self-signed, or recover cross-signing with a recovery key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Matrix recovery keys, passwords, and access tokens. <br>
Mitigation: Use only in a trusted interactive terminal and enter secrets only through the hidden prompts. <br>
Risk: Successful execution changes Matrix account device trust state. <br>
Mitigation: Check the homeserver, Matrix user ID, and target device ID before running the verifier. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mlumeau/verify-matrix-device) <br>
- [Publisher profile](https://clawhub.ai/user/mlumeau) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and status reporting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an interactive terminal for hidden credential prompts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
