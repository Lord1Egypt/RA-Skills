## Description: <br>
安全加密工具-免费版 guides an agent through personal file encryption and decryption with SAFE CLI, passphrase protection, ML-KEM-512, embedded encryption metadata, and cross-platform command examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to encrypt, decrypt, verify, and transfer personal files with SAFE CLI commands. It is intended for local file protection workflows where the user controls the passphrase, file paths, and backup process. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes optional irreversible deletion commands for original files. <br>
Mitigation: Keep backups and verify that encrypted files can be decrypted successfully before running shred, srm, or any command that overwrites originals. <br>
Risk: The skill asks agents to execute encryption and decryption commands against user-supplied paths. <br>
Mitigation: Confirm every input path, output path, and operation mode with the user before execution. <br>
Risk: Passphrases may be exposed if copied into reusable scripts, logs, or prompts. <br>
Mitigation: Avoid storing real passphrases in reusable automation and follow the agent platform's secret-handling guidance. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce file encryption or decryption commands that operate on local input and output paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
