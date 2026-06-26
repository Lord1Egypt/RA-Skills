## Description: <br>
Count words, lines, and characters in a file and return a single summary line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinwangmok](https://clawhub.ai/user/jinwangmok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to count lines, words, and bytes in a local text file when they need a quick document-length summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a user-provided local file path and reports that path in its output. <br>
Mitigation: Run it only on files intended for inspection and avoid sharing output when file paths reveal sensitive project or user information. <br>
Risk: The skill depends on the local wc command and local file permissions. <br>
Mitigation: Use it in environments where wc is available and treat missing-file or permission errors as normal execution failures, not successful counts. <br>


## Reference(s): <br>
- [Word Count ClawHub page](https://clawhub.ai/jinwangmok/word-count) <br>
- [Word Count user manual](artifact/MANUAL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text with labeled count fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns FILE, LINES, WORDS, BYTES, and STATUS fields for one input file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
