## Description: <br>
Search your local filesystem and codebase semantically. Use instead of grep/find/ls/cat chains when looking for files, functions, symbols, or code patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Navneeth08k](https://clawhub.ai/user/Navneeth08k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Semanticfs to find files, functions, symbols, code patterns, and implementation concepts in indexed local workspaces without manually chaining grep, find, ls, and cat commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow relies on installing upstream code and running a local service. <br>
Mitigation: Review the installer before use, prefer pinned releases or checksums where available, and run the service only while needed. <br>
Risk: Indexing broad local directories may expose secrets or private data through searchable snippets. <br>
Mitigation: Index only specific project directories, exclude secrets and private data, and confirm where the local index is stored. <br>
Risk: Search results may be stale or incomplete if the index is outdated. <br>
Mitigation: Rebuild or update the SemanticFS index before relying on results for code changes. <br>


## Reference(s): <br>
- [Semanticfs on ClawHub](https://clawhub.ai/Navneeth08k/semanticfs) <br>
- [Navneeth08k publisher profile](https://clawhub.ai/user/Navneeth08k) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, and path/line/snippet result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying SemanticFS service is read-only and returns workspace-relative paths, line ranges, and snippets from indexed directories.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
