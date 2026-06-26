## Description: <br>
RAGFlow Workbench automates local Windows RAGFlow setup and day-to-day knowledge-base, document parsing, retrieval, model configuration, and chat workflows through Python helper scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiejingke](https://clawhub.ai/user/jiejingke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and operate a local RAGFlow instance on Windows, including admin bootstrap, model defaults, knowledge-base management, document ingestion and parsing, search, and chat creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or uses RAGFlow admin credentials and API keys, and server security evidence reports weak disclosure around local secret handling. <br>
Mitigation: Change the default admin password before use, keep .env out of source control and screenshots, restrict local file permissions where possible, and avoid exposing credential-bearing endpoints over plain HTTP except for strictly local-only use. <br>
Risk: The skill can delete knowledge bases and documents from a RAGFlow instance. <br>
Mitigation: List candidate resources first, require explicit user confirmation, and delete only by explicit dataset_id or document_id. <br>
Risk: Bootstrap and model-configuration scripts require Docker container access and can modify local RAGFlow configuration. <br>
Mitigation: Run setup actions only after confirming the target local instance, container name, API URL, and intended model configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiejingke/ragflow-workbench-1-0-0-en) <br>
- [Command Reference](references/command-reference.md) <br>
- [Windows Quick Start Guide](references/quickstart_windows.md) <br>
- [Output Format Reference](references/output-format.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses structured --json output for automation-friendly script results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
