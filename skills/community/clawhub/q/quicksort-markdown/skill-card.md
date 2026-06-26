## Description: <br>
Sort markdown file headings and nested content alphabetically to organize notes efficiently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and note maintainers use this skill to organize Markdown notes by alphabetizing headings and their nested content. It supports sorting a file to a chosen output path or reading Markdown from standard input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sorting can reorder important notes in unexpected ways if run directly against originals. <br>
Mitigation: Run it on a copy or write to a new output file first, then review the sorted Markdown before replacing originals. <br>
Risk: The documented command may need adjustment because the packaged file is tool.py. <br>
Mitigation: Run the packaged tool.py file when using this release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/quicksort-markdown) <br>
- [Skill usage documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands; the bundled tool writes sorted Markdown text or files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on user-provided Markdown; security evidence found no hidden network, credential, persistence, or privilege behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
