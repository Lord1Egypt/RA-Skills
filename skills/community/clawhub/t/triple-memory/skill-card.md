## Description: <br>
Complete memory system combining LanceDB auto-recall, Git-Notes structured memory, and file-based workspace search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ktpriyatham](https://clawhub.ai/user/ktpriyatham) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up persistent memory across sessions, combining automatic conversation recall, structured decision memory, and workspace file search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables automatic persistent memory and silent context reuse, which may retain sensitive preferences, decisions, or facts longer than intended. <br>
Mitigation: Install only when persistent memory is intended, define what categories may be stored, constrain auto-capture for sensitive work, and ensure saved memories can be inspected, edited, and deleted. <br>
Risk: The workspace search behavior can surface contents from memory files and other workspace documentation. <br>
Mitigation: Avoid placing API keys or other secrets in shared memory files, and review workspace memory files before enabling broad search. <br>
Risk: The skill depends on external memory components and an embedding API key for the LanceDB setup. <br>
Mitigation: Review the dependent memory tools and plugin configuration before deployment, and keep API keys in environment variables or secret storage rather than committed files. <br>


## Reference(s): <br>
- [Triple Memory Setup Reference](references/SETUP.md) <br>
- [Triple Memory on ClawHub](https://clawhub.ai/ktpriyatham/triple-memory) <br>
- [ktpriyatham ClawHub Profile](https://clawhub.ai/user/ktpriyatham) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps, configuration snippets, memory usage guidance, and file-search command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
