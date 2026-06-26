## Description: <br>
Xdrop helps agents upload local files or directories to an Xdrop server and download encrypted share links from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixu-me](https://clawhub.ai/user/xixu-me) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate Xdrop file-transfer workflows, including uploading files or directories, generating share links, and downloading encrypted transfers when the full fragment key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may upload the wrong files or send data to an unintended Xdrop server. <br>
Mitigation: Verify the exact input files, directories, server URL, and API URL before running an upload. <br>
Risk: Full Xdrop share links containing the #k= fragment can decrypt the transfer. <br>
Mitigation: Treat complete share links as secrets and avoid exposing them in logs or shared command output. <br>
Risk: Downloaded transfers may contain untrusted files. <br>
Mitigation: Download into a fresh directory and inspect the contents before opening or using them. <br>


## Reference(s): <br>
- [Xdrop ClawHub page](https://clawhub.ai/xixu-me/xdrop) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce share URLs, saved file paths, transfer IDs, expiry timestamps, and output directory paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
