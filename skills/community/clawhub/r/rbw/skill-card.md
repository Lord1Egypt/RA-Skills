## Description: <br>
Securely interact with Bitwarden/Vaultwarden vaults using rbw CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TriplEight](https://clawhub.ai/user/TriplEight) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and operators use this skill to retrieve and manage Bitwarden or Vaultwarden vault items through rbw, including scripted and systemd service workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional non-interactive setup can expose the vault master password when stored in plaintext. <br>
Mitigation: Prefer interactive unlocks or systemd LoadCredential; if a credential file is used, restrict ownership and permissions tightly. <br>
Risk: Automated credential retrieval can use or transmit secrets for unintended vault items or services. <br>
Mitigation: Limit scripts to explicit trusted folders, items, fields, and service endpoints, and fail closed when lookups are missing or empty. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and systemd configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for rbw CLI workflows; no files or commands are executed by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
