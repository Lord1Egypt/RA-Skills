## Description: <br>
Create and deploy single-page static websites to GitHub Pages with autonomous workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThomekSolutions](https://clawhub.ai/user/ThomekSolutions) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create static website projects, generate complete HTML/CSS/JavaScript pages, and publish them to GitHub Pages with GitHub Actions automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment can publish project files to a public GitHub Pages site. <br>
Mitigation: Review the generated files, git status, and repository contents before deployment, and confirm no secrets or private content are included. <br>
Risk: Deployment uses the currently authenticated GitHub CLI account. <br>
Mitigation: Run gh auth status and confirm the intended GitHub account before creating or pushing the repository. <br>


## Reference(s): <br>
- [Complete Workflow Documentation](references/workflow.md) <br>
- [Design Patterns and Best Practices](references/design-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ThomekSolutions/web-deploy-github) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated HTML, CSS, JavaScript, README, and GitHub Actions files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates static website project files and deployment configuration; deployment can create a public GitHub repository and publish the selected project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
