## Description:

Build and deploy web apps from the command line with Tidepool's CLI and tp runtime API, including auth, payments, admin panels, email, data storage, custom domains, markdown, secrets, and real-time SSE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greydanus](https://clawhub.ai/user/greydanus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to create, configure, run, and deploy Tidepool web apps with features such as authentication, payments, storage, admin interfaces, email, custom domains, and real-time updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through production deployment workflows that affect live apps, secrets, databases, and files.

Mitigation: Install only from a trusted Tidepool package source, verify the target app before deployment, and review proposed commands before execution.

Risk: Push options can override secrets, replace database keys, delete remote files, or skip confirmation prompts.

Mitigation: Back up data first, avoid inline secrets when logs or shell history are captured, and use -y, --replace-db, or --sync only when those production changes are explicitly intended.

## Reference(s):

- [Tidepool Homepage](https://tidepool.sh)
- [Tidepool API Reference](https://tidepool.sh/api)
- [ClawHub Skill Page](https://clawhub.ai/greydanus/skills/tidepool)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tidepool CLI commands and tp runtime API usage for web app deployment.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
