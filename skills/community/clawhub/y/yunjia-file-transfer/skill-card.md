## Description: <br>
When a user asks for a file, this skill helps an agent find the requested local file and emit JSON that sends it to the current chat channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billyang1222](https://clawhub.ai/user/billyang1222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user requests a local file by name or location. It guides the agent to locate an absolute file path across Windows, macOS, or Linux, then produce a sendFileToChat JSON instruction without reading the file contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may search broad personal folders while trying to locate a requested file. <br>
Mitigation: Use exact filenames or paths and avoid broad recursive searches of the whole user profile unless necessary. <br>
Risk: A discovered file can be sent without a mandatory confirmation step. <br>
Mitigation: Require the agent to show the exact file path and receive confirmation before sending sensitive or ambiguous files. <br>
Risk: File paths and request text may be written to /tmp/yunjia-file-transfer.log. <br>
Mitigation: Clear or disable the local log when file names, paths, or request text are sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billyang1222/yunjia-file-transfer) <br>
- [Publisher profile](https://clawhub.ai/user/billyang1222) <br>
- [WINDOWS_GUIDE.md](references/WINDOWS_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON object with filePaths, text, and mode fields, plus guidance for file search commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires absolute file paths; supports multiple --file arguments; writes operational logs to /tmp/yunjia-file-transfer.log.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
