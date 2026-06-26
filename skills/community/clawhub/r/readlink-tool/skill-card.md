## Description: <br>
Display the target of a symbolic link. Use for resolving symlinks to find the actual file or directory they point to. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect the target of a symbolic link when tracing file paths or resolving symlink chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documented -f, -e, and -n options are not implemented by the bundled script, so relying on canonicalization or newline suppression can create incorrect expectations. <br>
Mitigation: Use the release as a basic readlink-style symlink target checker unless the option behavior is implemented and retested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/readlink-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single symlink target path; documented canonicalization flags are not implemented by the bundled script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
