## Description: <br>
VerifyGuard is a Python-based pre-publication checker for Markdown outputs that flags completeness, link-format, sensitive-data, and formatting issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxr-666](https://clawhub.ai/user/lxr-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and agents use this skill before publishing or submitting Markdown content to check for unfinished markers, possible sensitive information, Markdown formatting issues, and links that need review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Link checks may flag HTTP links for review but do not confirm external URL reachability. <br>
Mitigation: Treat link results as review prompts and verify important URLs with a network-capable checker before publication. <br>
Risk: Secret findings may print matching file snippets to the terminal or logs. <br>
Mitigation: Run the tool locally in a trusted environment, avoid sharing captured logs, and rotate any exposed secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxr-666/verifyguard) <br>
- [Publisher profile](https://clawhub.ai/user/lxr-666) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text diagnostics with severity labels and suggested command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; runs locally against a user-provided file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
