## Description:

Create and deploy single-page static websites to GitHub Pages using a workflow that initializes a project, builds responsive HTML, CSS, and JavaScript, and publishes with GitHub Actions automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomeksolutions](https://clawhub.ai/user/thomeksolutions)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate portfolio, CV, landing page, or other static web projects and publish them to GitHub Pages. It supports project initialization, local site implementation, GitHub repository setup, and automated deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment script can create public GitHub repositories, push project contents, and activate GitHub Pages.

Mitigation: Require explicit approval before repository creation, git pushes, and GitHub Pages activation; review the generated repository before publishing.

Risk: Project initialization and deployment can overwrite or commit unintended local files if run in a populated directory.

Mitigation: Run the skill in a new empty project directory, inspect files before commit, and add a conservative .gitignore before deployment.

Risk: Published static site contents may expose secrets, private documents, or unsuitable placeholder content.

Mitigation: Scan the project tree for secrets and private files, replace placeholder content, and confirm the final site contents before pushing.

## Reference(s):

- [Web Deploy GitHub Pages on ClawHub](https://clawhub.ai/thomeksolutions/skills/web-deploy-github)
- [Complete Workflow Documentation](artifact/references/workflow.md)
- [Design Patterns and Best Practices](artifact/references/design-patterns.md)
- [GitHub CLI](https://cli.github.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands and generated HTML, CSS, JavaScript, README, and GitHub Actions workflow files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project files and configure deployment for a public GitHub Pages repository.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
