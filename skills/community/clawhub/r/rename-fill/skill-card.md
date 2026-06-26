## Description: <br>
Rename files in a specified directory with a given prefix, using a Node.js script after the agent gathers inputs, shows a preview, and asks for confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[git-xyz](https://clawhub.ai/user/git-xyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to batch rename files in a selected directory by adding a consistent prefix, with an agent-mediated preview and confirmation step before changes are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included script can make persistent bulk filename changes and does not enforce its own interactive confirmation. <br>
Mitigation: Use the agent preview and explicit confirmation flow before running the script, and test on a copied folder or backup before applying changes to important files. <br>
Risk: Path-like prefixes or broad target directories can produce unintended rename results. <br>
Mitigation: Avoid prefixes containing slashes, backslashes, '..', or path-like text, and confirm the target directory before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/git-xyz/rename-fill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and text rename summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can invoke a Node.js script that performs persistent local file renames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
