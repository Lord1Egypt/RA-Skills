## Description: <br>
Sort files, lines, and columns with custom ordering and dedup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to sort, deduplicate, rank, shuffle, and summarize local text, CSV, and JSON files during file review and lightweight data analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operation history is persisted locally and can include filenames or other command details. <br>
Mitigation: Avoid using the skill on sensitive filenames or private data unless local history in ~/.local/share/sort/history.log is acceptable. <br>
Risk: The JSON command's Python fallback can execute unintended local code with crafted input. <br>
Mitigation: Prefer environments with jq installed, and avoid the json command with untrusted file paths or keys until the fallback is rewritten to pass arguments safely. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Review and scan the skill before installing or deploying it. <br>


## Reference(s): <br>
- [Sort skill page](https://clawhub.ai/ckchzh/sort) <br>
- [ckchzh publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit sorted text, tabular summaries, JSON arrays, and status lines depending on the selected command.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
