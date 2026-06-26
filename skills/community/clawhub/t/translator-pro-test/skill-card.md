## Description: <br>
Test translation quality with built-in dictionaries and comparison tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and translation evaluators use this skill to run local translation quality checks, dictionary lookups, glossary queries, comparisons, and batch translation test stubs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local bash script and creates a local data directory. <br>
Mitigation: Review the script before use and run it in an environment where creating ~/.local/share/translator-pro-test/ is acceptable. <br>
Risk: The reviewed commands are basic stubs rather than a full translation engine. <br>
Mitigation: Use the outputs as translation testing helpers, not as authoritative translation quality results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/translator-pro-test) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local bash command stubs and may create ~/.local/share/translator-pro-test/.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
