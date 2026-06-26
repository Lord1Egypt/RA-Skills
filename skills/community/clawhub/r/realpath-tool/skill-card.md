## Description: <br>
Resolve relative paths and symbolic links to absolute canonical paths. Use for getting the full, unambiguous file path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to resolve supplied filesystem paths into canonical absolute paths before passing paths to scripts, commands, or diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resolving a user-supplied path can reveal absolute filesystem locations in agent output. <br>
Mitigation: Use the tool only for paths that are appropriate to disclose in the current workspace or conversation. <br>
Risk: The documentation lists options that the bundled script does not implement. <br>
Mitigation: Verify behavior before relying on option flags, or use the host system's realpath command when those options are required. <br>


## Reference(s): <br>
- [ClawHub listing for Realpath Tool](https://clawhub.ai/dinghaibin/realpath-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text path output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints one canonical path for the provided path argument; the bundled implementation does not implement every documented option.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
