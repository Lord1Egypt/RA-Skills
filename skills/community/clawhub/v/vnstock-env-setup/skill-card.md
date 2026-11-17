## Description:

Provides environment diagnostics, setup guidance, and agent guide installation for the Vnstock Free and Sponsor ecosystems, including OS, Python, virtual environment, package, and migration checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinh-vu](https://clawhub.ai/user/thinh-vu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to diagnose and set up Python environments for Vnstock or vnstock_data, install required packages, and guide migration from legacy imports when Sponsor-tier packages are present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke remote installers and package indexes that are not pinned in the bundled artifact.

Mitigation: Review the scripts and remote sources before installation, and avoid curl/wget-to-shell Sponsor setup unless the installer is pinned and verified.

Risk: The Agent Guide installer can rewrite repository files, docs, and selected agent skills.

Mitigation: Run it only with a clean Git status, a separate backup, and explicit approval before replacing existing docs or skills.

Risk: Setup commands may change the user's Python environment and installed packages.

Mitigation: Use the required virtual environment workflow and run diagnostics before and after package installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thinh-vu/skills/vnstock-env-setup)
- [Vnstock Requirements](https://vnstocks.com/files/requirements.txt)
- [Vnstock Sponsor Installer](https://vnstocks.com/files/vnstock-cli-installer.run)
- [Vnstock Package Index](https://vnstocks.com/api/simple)
- [Vnstock Agent Guide Repository](https://github.com/vnstock-hq/vnstock-agent-guide.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that install packages, run diagnostics, clone guide content, or update local files after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
