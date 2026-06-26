## Description: <br>
Extract comments and split symbols from source files. Use when users want to extract inline comments, docstrings, or block comments from code files to understand structure or generate documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turinfohlen](https://clawhub.ai/user/turinfohlen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to extract comments, docstrings, and block comments from source files as a quick entry point for code review, legacy-code understanding, or documentation summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads local source files and emits extracted comments, which may expose sensitive information present in those comments. <br>
Mitigation: Run it only on files that are appropriate to inspect and share in the current agent session. <br>
Risk: Custom symbol configurations are regex-based and may produce incorrect or incomplete extraction results if patterns are too broad or malformed. <br>
Mitigation: Review custom symbols.json patterns before use and verify extracted output against the source file when accuracy matters. <br>
Risk: The README mentions installing via pip, which may differ from the provided artifact. <br>
Mitigation: Verify the package source before installing from a package index, or run the provided artifact directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/turinfohlen/splitsym) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text comment listings with line numbers and optional Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves indentation and marks extracted block comments with a PAIR: prefix.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
