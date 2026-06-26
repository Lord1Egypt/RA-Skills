## Description: <br>
Provides a simulated Linux terminal mode for browsing and operating on workspace files with commands such as cd, ls, cat, pwd, mv, cp, rm, touch, mkdir, find, grep, head, tail, and chmod. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eraycc](https://clawhub.ai/user/eraycc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to interact with accessible workspace files through familiar terminal-style commands without asking the agent to run arbitrary shell snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terminal-like commands can read or change files the agent can access. <br>
Mitigation: Use the skill in a sandboxed workspace and avoid granting access to sensitive directories. <br>
Risk: Commands such as rm, mv, cp, and chmod can alter or remove user data. <br>
Mitigation: Review commands before execution and require explicit confirmation for destructive actions unless the user intentionally supplies a force or confirmation flag. <br>
Risk: Recursive find or grep operations may expose sensitive file names or contents. <br>
Mitigation: Limit searches to intended paths and avoid using the skill on workspaces containing secrets or confidential data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eraycc/terminal-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal-style plain text with command prompts, command output, and confirmation questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file contents, directory listings, search matches, status messages, and deletion confirmations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
