## Description: <br>
Skill for agents managing terminal Python scripts by requiring end-of-file summaries, generating script documentation, and recording common pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaibazax-dev](https://clawhub.ai/user/kaibazax-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to organize reusable local Python scripts, consult generated documentation before creating new scripts, and log recurring failures in a pitfall file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may lead an agent to run or edit existing local Python scripts. <br>
Mitigation: Install only in workspaces where local script management is intended, and review unfamiliar scripts before execution. <br>
Risk: The bundled helper writes py_docs.md while the skill text refers to pyscripts_docs.md. <br>
Mitigation: Confirm the expected documentation filename before relying on generated script indexes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaibazax-dev/pyscripts-org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples; generated documentation files are Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update local Markdown documentation files and Python script summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
