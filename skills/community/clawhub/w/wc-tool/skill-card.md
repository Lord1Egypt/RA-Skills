## Description: <br>
Count lines, words, characters, and bytes in one or more files with per-file and total summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to get local word-count style statistics for documents, code, piped text, and simple data volume checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises byte counts, multiple files, JSON output, null-separated file lists, totals, and longest-line reporting that the included script does not implement. <br>
Mitigation: Verify required counting behavior before relying on advertised options, and treat unsupported options as documentation mismatch until the implementation is updated. <br>
Risk: The script reads local files supplied by the user and emits local count results. <br>
Mitigation: Run it only on files intended for local analysis and avoid using sensitive inputs where command output logs are retained. <br>


## Reference(s): <br>
- [Wc Tool ClawHub page](https://clawhub.ai/dinghaibin/wc-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included script supports one file or standard input and reports lines, words, and characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
