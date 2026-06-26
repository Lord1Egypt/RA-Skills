## Description: <br>
Create, extract, list, and compress tar archives with format support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage local tar archives: create and append archives, extract contents, list entries, inspect metadata, compare archives, verify integrity, and search member names. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracting unfamiliar archives can place files into unexpected locations or sensitive working directories. <br>
Mitigation: List or verify unfamiliar archives before extraction, then extract untrusted archives into a fresh temporary directory. <br>
Risk: Archive creation or append commands can include unintended local files if broad file arguments are used. <br>
Mitigation: Review input paths before running create or add, then inspect the resulting archive with list or info. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/tar) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bytesagain1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text with shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, read, extract, append, compare, or inspect local archive files depending on the selected command.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
