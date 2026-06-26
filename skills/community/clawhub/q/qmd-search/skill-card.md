## Description: <br>
qmd Search helps agents search local markdown files, notes, documentation, code, and indexed collections through the local qmd CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bheemreddy181](https://clawhub.ai/user/bheemreddy181) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to find files, search notes and documentation, retrieve snippets, and gather local context from qmd collections without relying on external APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index and retrieve local files through qmd, which may expose sensitive personal files, secrets, or private repositories if collections are too broad. <br>
Mitigation: Install qmd only from a trusted source, understand where local models and indexes are stored, and keep collections narrowly scoped before allowing agents to search or quote results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bheemreddy181/qmd-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline qmd shell commands and local search result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required; qmd runs locally and may use local indexes and models.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
