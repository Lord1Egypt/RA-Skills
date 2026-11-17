## Description:

Zadig provides an agent-facing Node.js client for managing Zadig DevOps platform projects, workflows, environments, services, builds, tests, releases, clusters, users, and logs through the Zadig OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilianzhu](https://clawhub.ai/user/lilianzhu)

### License/Terms of Use:

MIT

## Use Case:

Developers and DevOps engineers use this skill to automate Zadig platform operations such as CI/CD workflow execution, environment and service inspection, deployment image updates, and log retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Zadig API token and can perform high-impact administration actions.

Mitigation: Use a dedicated least-privilege Zadig token and review delete, update, user, and cluster functions before enabling production or admin workflows.

Risk: A committed or shared ZADIG_API_KEY could expose Zadig platform access.

Mitigation: Keep ZADIG_API_KEY out of version control and provide it only through the local environment configuration.

Risk: Using a non-HTTPS Zadig endpoint could expose credentials or operational data in transit.

Mitigation: Require an HTTPS ZADIG_API_URL before installing or running the skill.

## Reference(s):

- [Zadig official documentation](https://docs.koderover.com)
- [ClawHub skill page](https://clawhub.ai/lilianzhu/skills/zadig)

## Skill Output:

**Output Type(s):** [API Calls, Code, JSON, Text, Shell commands, Configuration guidance]

**Output Format:** [JavaScript API results, JSON objects, log text, and Markdown guidance with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZADIG_API_URL and ZADIG_API_KEY; optional defaults include ZADIG_DEFAULT_PROJECT and ZADIG_DEFAULT_ENV.]

## Skill Version(s):

4.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
