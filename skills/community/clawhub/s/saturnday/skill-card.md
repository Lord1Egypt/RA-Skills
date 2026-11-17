## Description:

Saturnday helps developers govern AI-built software from scan to build to repair with deterministic checks, LLM-assisted security triage, governed execution, document generation, release inspection, and auto-fix workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honouralexwill](https://clawhub.ai/user/honouralexwill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Saturnday to scan skills and repositories, run governance checks, build projects from briefs under per-commit governance, produce governed documents, inspect release artifacts, and repair findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guard and Run modes can modify a target repository, including creating commits and evidence directories.

Mitigation: Use Scan mode for read-mostly review work, and run Guard or Run only on repositories or branches prepared for automated changes.

Risk: Run mode can transmit repository contents to the selected AI backend for code generation.

Mitigation: Expose only the repository and backend credentials required for the task, and avoid using Run mode on sensitive code unless that data transfer is approved.

Risk: The skill depends on the external Saturnday package and optional AI backend credentials or CLI tools.

Mitigation: Install Saturnday in a virtual environment or container and provide only the API key or CLI access needed for the chosen backend.

## Reference(s):

- [Saturnday homepage](https://www.saturnday.dev)
- [ClawHub Saturnday skill page](https://clawhub.ai/honouralexwill/skills/saturnday)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Terminal output with JSON results, Markdown reports, evidence directories, generated code, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan mode is read-mostly; Guard and Run modes may create git commits, evidence directories, progress logs, review reports, and project files.]

## Skill Version(s):

1.8.1 (source: server release metadata; artifact frontmatter reports 1.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
