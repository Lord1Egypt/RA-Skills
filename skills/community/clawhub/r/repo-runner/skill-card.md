## Description: <br>
Bootstrap and run a GitHub project by following its docs (README/docs), with safeguards for untrusted install/run steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyl-hub](https://clawhub.ai/user/zyl-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap GitHub or local projects for dev, build, or test workflows by following the repository's own documentation. It helps identify project types, dependencies, environment setup, run commands, and caveats while preserving confirmation steps for untrusted commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps run arbitrary user-chosen repositories, so dependency installs, postinstall hooks, Docker, or project commands may execute untrusted code. <br>
Mitigation: Review every proposed command and approve installs, Docker use, and shell execution only for trusted repositories or isolated environments. <br>
Risk: Repository setup may require environment variables or secrets. <br>
Mitigation: Do not paste or store secrets in the agent transcript; provide required values out of band only after understanding why they are needed. <br>
Risk: Suggested setup commands can be incorrect or unsafe if repository documentation is ambiguous. <br>
Mitigation: Prefer documented commands, inspect generated suggestions before execution, and confirm before changing existing workspaces or pulling updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zyl-hub/repo-runner) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports commands run, local URL or port, next steps, and known caveats.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
