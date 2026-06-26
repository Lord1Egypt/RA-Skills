## Description: <br>
Convert spaces to tabs in text files. Use for consistent indentation and reducing file size by replacing spaces with tabs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert space-indented text or code into tab-indented output for formatting consistency and smaller files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Piped input may be interpreted as a filesystem path, causing the tool to read local files unexpectedly. <br>
Mitigation: Audit or fix stdin handling before installation, and use only explicit file-path arguments until the behavior is documented and corrected. <br>
Risk: The release has a suspicious security verdict from the authoritative scanner evidence. <br>
Mitigation: Review the helper script and scanner guidance before deployment, then prefer a version that clearly separates stdin text from file path inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/unexpand-tool) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transformation output with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transforms spaces to tabs using a local Python helper; review stdin behavior before installation because scanner evidence reports that piped input may be treated as a filesystem path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
