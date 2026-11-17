## Description:

Deploy local web projects to live URLs by automating GitHub repository creation, Vercel or Netlify deployment, and optional custom domain setup with SSL and CI/CD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to publish local web projects or static sites to production URLs through GitHub plus Vercel or Netlify, with optional custom-domain guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned runtime package execution and broad update commands can change the deployment toolchain unexpectedly.

Mitigation: Use pinned, reviewed ClawHub tooling versions and avoid `update --all` unless the update set has been reviewed.

Risk: The skill can create or modify repositories, hosting deployments, CI/CD links, and optional DNS records.

Mitigation: Run it with least-privilege GitHub, Vercel or Netlify, Maton, and DNS credentials scoped to the target project.

Risk: Missing or invalid credentials can block repository, gateway, hosting, or custom-domain stages.

Mitigation: Perform explicit credential checks before deployment and treat blocked stages as partial results with concrete next actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h4gen/skills/web-hosting)
- [ClawHub homepage](https://clawhub.ai)
- [Inspected upstream skills](references/inspected-skills.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with structured deployment status sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports project detection, repository status, infrastructure gate status, deployment status, custom-domain plan, and next actions.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
