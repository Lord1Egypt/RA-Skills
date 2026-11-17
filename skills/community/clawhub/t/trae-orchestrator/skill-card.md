## Description:

Orchestrates TRAE IDE for automated software development with multi-agent collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vichard998](https://clawhub.ai/user/vichard998)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to prepare project requirements, launch TRAE IDE, send development prompts, and monitor progress through signal files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch a local TRAE IDE session and write project files.

Mitigation: Run it only in a dedicated project directory that is under version control.

Risk: The skill can auto-submit clipboard text through desktop automation without strong focus safeguards.

Mitigation: Prefer manual paste or verify the active TRAE window before enabling automated prompt submission.

Risk: Project requirements and prompts may be copied into files or the clipboard.

Mitigation: Do not include secrets, credentials, or sensitive data in requirements or prompts.

Risk: Optional desktop automation dependencies affect the local Python environment.

Mitigation: Install dependencies in a virtual environment with reviewed versions, and avoid running as Administrator unless necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vichard998/skills/trae-orchestrator)
- [Artifact documentation: INNOVATIONS.md](artifact/INNOVATIONS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python examples and generated local project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create requirements, prompts, progress files, signal files, and local configuration for TRAE orchestration.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
