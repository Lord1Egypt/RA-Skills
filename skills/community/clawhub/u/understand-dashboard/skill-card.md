## Description: <br>
Launch the interactive web dashboard to visualize a codebase's knowledge graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lum1104](https://clawhub.ai/user/Lum1104) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to open a local dashboard for exploring an existing Understand Anything knowledge graph for a project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs Node dependencies and runs dashboard code that was not included in the reviewed artifact. <br>
Mitigation: Use it only from a trusted source, inspect the dashboard directory and lockfile before installation, and run it in a controlled project workspace. <br>
Risk: The dashboard reads the selected project's knowledge graph and opens a local browser session. <br>
Mitigation: Confirm the selected project path before launch and avoid using it on sensitive projects unless the local dashboard environment is approved. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Starts a background local Vite dashboard for the selected project when dependencies and graph files are available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
