## Description:

Provides a startup scaffold helper for a React and Node.js SaaS project with documented landing page, authentication, payments, analytics, and marketing features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and startup builders use this skill to create an initial SaaS project scaffold and receive quick-start guidance for launching a startup application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold helper accepts a project name that is used as a filesystem path, so unusual values can create confusing paths or unintended shell behavior.

Mitigation: Pass a simple project slug such as my-startup; avoid spaces, path separators, wildcards, and option-like values.

Risk: The skill description lists authentication, payments, analytics, Docker, and CI/CD capabilities that the bundled script does not implement.

Mitigation: Treat these claims as aspirational unless the generated files are separately verified before production use.

## Reference(s):

- [Startup Toolkit on ClawHub](https://clawhub.ai/sunshine-del-ux/skills/startup-toolkit)
- [Publisher profile](https://clawhub.ai/user/sunshine-del-ux)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Shell output plus generated project directories and brief next-step instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a project name and optional documented feature flags.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
