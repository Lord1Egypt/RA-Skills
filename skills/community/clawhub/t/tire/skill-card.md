## Description: <br>
Tire is a command-line assistant for tracking, searching, summarizing, and exporting local home-management activity logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use Tire to keep simple local records for home-management tasks, review recent entries, inspect summary statistics, search saved text, and export logs as JSON, CSV, or text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tire saves user-entered text in local log files under ~/.local/share/tire. <br>
Mitigation: Do not enter passwords, tokens, private account details, or sensitive personal information. <br>
Risk: The artifact does not clearly define installation behavior. <br>
Mitigation: Verify the CLI install path and review the shell script before installing or running it. <br>


## Reference(s): <br>
- [ClawHub Tire release](https://clawhub.ai/bytesagain3/tire) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain3) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local command-line guidance; the bundled shell script writes entries under ~/.local/share/tire and can export JSON, CSV, or text files.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
