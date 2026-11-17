## Description:

Thoth Standard -- Auto-Documentation Engine. Reads your entire project and generates README, API reference, and usage guide. Saved to .md files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan a project directory and generate project documentation, including a README, API reference, and usage guide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads substantial project source files into the agent context, which can expose secrets or sensitive implementation details.

Mitigation: Run it on a copy or limited project path, remove secrets before use, and review generated documentation before sharing.

Risk: The artifact includes a system-wide pip install command using --break-system-packages.

Mitigation: Use a virtual environment with pinned dependencies instead of installing packages into the system Python environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/occupythemilkyway/skills/thoth)
- [Thoth Homepage](https://clawhub.ai/occupythemilkyway/thoth)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown files: README.md, API_REFERENCE.md, and USAGE_GUIDE.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PROJECT_PATH and LICENSE_KEY; writes generated documentation to OUTPUT_DIR.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
