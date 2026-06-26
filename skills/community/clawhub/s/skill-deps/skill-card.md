## Description: <br>
Track and manage dependencies between OpenClaw skills, including scanning installed skills, visualizing dependency trees, detecting conflicts, and assisting with skill installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myrodar](https://clawhub.ai/user/myrodar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect OpenClaw skill dependencies, identify missing or conflicting skills, view dependency trees, search ClawHub, and plan skill installations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can persistently add multiple skills from ClawHub through dependency resolution. <br>
Mitigation: Review the dependency list and exact skill versions before running skill-install.sh, and prefer the read-only scan, tree, conflict, and search commands when installation is not required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local OpenClaw skill directories and ClawHub registry queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
