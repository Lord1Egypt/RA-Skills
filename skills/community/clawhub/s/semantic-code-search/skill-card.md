## Description: <br>
Semantic search engine for codebases that understands intent and finds functionally similar code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to index a local codebase and search for functions, classes, similar implementations, and possible duplicate logic by meaning rather than exact text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local index can contain copied source snippets from indexed repositories. <br>
Mitigation: Index only repositories whose contents may be stored locally, avoid codebases with sensitive secrets, and keep .code_index.json out of commits and shared folders. <br>
Risk: The documented CLI path differs from the included script name. <br>
Mitigation: Verify the actual CLI entrypoint in the installed artifact before running commands from the documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/semantic-code-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell command examples; Python APIs return lists of dictionaries and optional JSON index files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local .code_index.json file containing copied code snippets from repositories the user indexes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
