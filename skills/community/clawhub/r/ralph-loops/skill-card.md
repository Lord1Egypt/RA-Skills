## Description: <br>
Runs autonomous iterative AI loops for requirements, planning, or building phases using structured prompts and fresh context per iteration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qlifebot-coder](https://clawhub.ai/user/qlifebot-coder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run iterative AI development loops for requirements interviews, implementation planning, and build execution with persistent file state and dashboard monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous loop execution can edit files, run commands, and continue until stopped. <br>
Mitigation: Run it only in an isolated development workspace with a disposable branch, limited credentials, explicit iteration or time limits, and human review of outputs. <br>
Risk: Permission prompts are bypassed during loop execution. <br>
Mitigation: Use a sandboxed environment such as a VM or container and provide only the API keys and local files required for the task. <br>
Risk: Automatic git push can publish unintended changes to a remote branch. <br>
Mitigation: Review or disable automatic push behavior and use a throwaway or protected branch until changes have been inspected. <br>
Risk: The check command option runs shell commands and can be unsafe with untrusted input. <br>
Mitigation: Use only trusted, fixed check commands and do not pass user-controlled strings into --check-cmd. <br>
Risk: The dashboard exposes local loop status and process controls. <br>
Mitigation: Run the dashboard only on a trusted local machine and avoid exposing it on shared or public networks. <br>


## Reference(s): <br>
- [Ralph Loops on ClawHub](https://clawhub.ai/qlifebot-coder/ralph-loops) <br>
- [Ralph Wiggum Technique](https://ghuntley.com/ralph/) <br>
- [Clayton Farr Ralph Playbook](https://github.com/ClaytonFarr/ralph-playbook) <br>
- [Geoffrey Huntley how-to-ralph-wiggum](https://github.com/ghuntley/how-to-ralph-wiggum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, prompt templates, shell commands, configuration files, and code or file changes produced by autonomous loop iterations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Loop runs may create or edit files, run commands, record local state, commit changes, push to git remotes, and expose status through a local dashboard.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
