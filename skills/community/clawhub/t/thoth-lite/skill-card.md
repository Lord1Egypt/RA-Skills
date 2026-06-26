## Description: <br>
Thoth Lite -- Auto-Documentation. Point Thoth at a file or folder and get a clean README instantly. Free tier. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Thoth Lite to inspect a selected file or folder and generate a clean README from the discovered project structure and file previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can expose selected project files to the agent during documentation generation. <br>
Mitigation: Review PROJECT_PATH before use and avoid secrets, credentials, private keys, .env files, and highly confidential source unless those contents are approved for processing. <br>
Risk: The install step uses pip with --break-system-packages, which can alter the system Python environment. <br>
Mitigation: Run the install step in an isolated virtual environment or disposable development environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/thoth-lite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads up to 20 selected files and up to the first 3000 characters from each file before asking the agent to draft a README.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
