## Description: <br>
Rxtool helps agents test, extract, replace, split, and explain regular expressions with support for named groups, common regex flags, stdin input, and JSON extraction output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent workflows use this skill for local regular-expression testing, match extraction, text replacement, splitting, and lightweight regex explanation without external dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text passed through the tool may be printed in terminal output or captured by shell history, logs, or surrounding automation. <br>
Mitigation: Avoid running sensitive secrets or private data through shared terminals, CI logs, or persistent agent transcripts. <br>
Risk: Complex regular expressions evaluated against large inputs can run slowly or hang. <br>
Mitigation: Review patterns before use, test on small samples first, and apply runtime limits when processing untrusted or large text. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read input from stdin or inline text and may emit matched text, replacements, split fields, regex component guidance, or JSON extraction results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
