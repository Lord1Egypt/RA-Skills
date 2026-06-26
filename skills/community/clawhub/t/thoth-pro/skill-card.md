## Description: <br>
Thoth Pro is a full auto-documentation suite that generates a README, API reference, usage guide, architecture document, changelog, and optional Python docstring suggestions for a project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to document a codebase by scanning source files and project metadata, then producing project documentation and optional docstring updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project source code and recent commit messages may be placed into the agent session during documentation generation. <br>
Mitigation: Run on a clean copy of the repository, avoid sensitive source trees, and set GENERATE_CHANGELOG=no when private commit history should not be shared. <br>
Risk: The skill modifies source by default when docstring injection is enabled. <br>
Mitigation: Set INJECT_DOCSTRINGS=no unless source edits are intended, and review generated docstring changes before keeping them. <br>
Risk: The artifact installs Python dependencies with a system-package override. <br>
Mitigation: Install dependencies in a virtual environment instead of using --break-system-packages. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/occupythemilkyway/thoth-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents, JSON docstring mapping, and inline shell or Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PROJECT_PATH and LICENSE_KEY; optional settings control output directory, docstring injection, project name, and changelog generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
