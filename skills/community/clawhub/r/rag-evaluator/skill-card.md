## Description: <br>
Rag Evaluator is a local Bash CLI for logging, reviewing, searching, and exporting RAG evaluation experiments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI practitioners use this skill to track RAG configurations, benchmark results, prompt experiments, costs, usage, and reports from the command line. It is most useful for lightweight local experiment logging and exporting RAG evaluation records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered prompts, evaluation notes, costs, usage details, or other experiment data are saved locally and can be included in exports. <br>
Mitigation: Do not enter API keys, credentials, private customer data, or sensitive prompts unless local storage and export handling are acceptable. <br>
Risk: The package does not provide a clear install mechanism for the rag-evaluator command. <br>
Mitigation: Verify how the command is installed or linked before relying on it in a workflow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output and local log/export files in text, CSV, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores command entries under ~/.local/share/rag-evaluator by default.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
