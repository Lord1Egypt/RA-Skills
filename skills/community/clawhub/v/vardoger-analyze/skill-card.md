## Description: <br>
Runs the vardoger CLI to analyze OpenClaw conversation history and generate tailored assistant personalization instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dstrupl](https://clawhub.ai/user/dstrupl) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect prior assistant conversations, summarize behavioral preferences, and generate persistent personalization instructions for future assistant sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads broad past conversation history. <br>
Mitigation: Install and run it only when the user wants conversation-history analysis, verify the vardoger CLI source and version, and approve only expected vardoger commands. <br>
Risk: The skill writes persistent global assistant personalization outside the current workspace. <br>
Mitigation: Review the generated markdown before keeping it and remove or edit the personalization file if it captures sensitive or unwanted instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dstrupl/vardoger-analyze) <br>
- [vardoger project page](https://github.com/dstrupl/vardoger) <br>
- [pipx installation documentation](https://pipx.pypa.io/stable/installation/.) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown personalization guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the vardoger CLI and may read conversation history and write persistent assistant personalization outside the current workspace.] <br>

## Skill Version(s): <br>
0.3.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
