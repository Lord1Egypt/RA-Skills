## Description: <br>
Manage TeraBox cloud storage operations including login, upload, download, share, and transfer. Use the terabox CLI tool for file management tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArthurPatten](https://clawhub.ai/user/ArthurPatten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage TeraBox cloud storage from an agent, including authentication, file upload and download, cloud file operations, sharing, and transfer from shared links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal use can trigger skill or CLI update paths that download packages and may replace local executables. <br>
Mitigation: Install only from trusted publisher and TeraBox update infrastructure, review install and update commands before execution, and use update-check-only or --no-check-update behavior where supported. <br>
Risk: TeraBox credentials and tokens are stored in the local terabox configuration file. <br>
Mitigation: Protect ~/.config/terabox/config.json, avoid login on shared or untrusted machines, and run terabox logout after use in public environments. <br>
Risk: Upload, download, move, rename, transfer, and public share operations can affect user cloud data or expose files. <br>
Mitigation: Confirm exact source and destination paths, review share settings before creation, keep operations within the documented sandbox, and back up important data. <br>


## Reference(s): <br>
- [Authentication Guide](reference/authentication.md) <br>
- [TeraBox Usage Examples](reference/examples.md) <br>
- [TeraBox Storage Skill - Beta Notes](reference/notes.md) <br>
- [terabox CLI Command Reference](reference/terabox-commands.md) <br>
- [Troubleshooting](reference/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command confirmation prompts, path checks, login guidance, and JSON-capable terabox CLI examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
