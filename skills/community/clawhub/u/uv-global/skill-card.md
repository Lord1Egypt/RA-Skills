## Description:

Provision and reuse a global uv environment for ad hoc Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqiao](https://clawhub.ai/user/guoqiao)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up and reuse a shared uv-managed Python environment for quick scripts that need extra packages without creating a full project environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer creates a persistent shared Python environment with a broad, unpinned dependency bundle.

Mitigation: Review the dependency list before installing, pin or reduce packages for managed environments, and update the environment deliberately.

Risk: If uv is unavailable, the installer can fetch and run the uv installer through a curl fallback.

Mitigation: Install uv through a trusted package manager before running the skill, or audit the installer path before allowing the fallback.

Risk: Prepending ~/.uv-global/.venv/bin to PATH can make persistent helper commands and packages affect later shell sessions.

Mitigation: Use explicit uv --project ~/.uv-global commands where possible, or scope PATH changes to controlled shells.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqiao/skills/uv-global)
- [Metadata homepage](https://github.com/guoqiao/skills/blob/main/uv-global/uv-global/SKILL.md)
- [uv installer referenced by artifact](https://astral.sh/uv/install.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and usage guidance for a persistent uv environment at ~/.uv-global.]

## Skill Version(s):

0.1.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
