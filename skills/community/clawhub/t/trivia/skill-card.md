## Description: <br>
Host trivia rounds with question banks, scoring, and boards. Use when running quizzes, checking answers, analyzing scores, generating rounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill as a local command-line activity tracker for trivia-related or general quiz workflow entries, including logging, searching, reviewing, and exporting recorded actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user-provided input in local plaintext logs and export files. <br>
Mitigation: Do not enter secrets, private personal data, or sensitive quiz material; periodically inspect or delete ~/.local/share/trivia. <br>
Risk: The public trivia description may overstate the artifact behavior, which primarily logs and retrieves text entries. <br>
Mitigation: Review the installed commands before use and treat the tool as a local activity log rather than a full trivia host. <br>


## Reference(s): <br>
- [Trivia on ClawHub](https://clawhub.ai/ckchzh/trivia) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local plaintext log and export files under ~/.local/share/trivia.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
