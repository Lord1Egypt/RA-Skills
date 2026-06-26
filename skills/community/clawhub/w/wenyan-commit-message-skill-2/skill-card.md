## Description: <br>
Drafts git commit messages in Classical Chinese (文言文) when explicitly requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xing-lin](https://clawhub.ai/user/xing-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to turn staged or unstaged git diffs into concise Classical Chinese commit messages when they explicitly request that style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect staged or unstaged git diffs, which can expose pending code changes to the agent. <br>
Mitigation: Use it only in repositories where the agent is allowed to read pending changes, and review the generated commit message before committing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xing-lin/wenyan-commit-message-skill-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text commit message, with optional body text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The output is intended to be copied directly into git commit tooling and should not include explanations or Markdown wrapping.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
