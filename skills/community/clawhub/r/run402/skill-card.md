## Description:

Provision Postgres databases, deploy static sites, generate images, and build full-stack webapps on Run402 using x402 micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majortal](https://clawhub.ai/user/majortal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build and operate Run402-backed web applications, including database provisioning, static site deployment, serverless functions, image generation, billing flows, and project management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Run402 actions can create resources, renew projects, generate images, create checkout sessions, or send paid feedback messages.

Mitigation: Require explicit user confirmation before paid actions and use idempotency keys for provisioning, deployment, renewal, image generation, and other chargeable requests.

Risk: The skill relies on persistent wallet, project, and service credentials that can grant broad access to deployed resources.

Mitigation: Keep wallet files and service keys isolated, avoid exposing service keys in client-side code, and prefer a pinned or locally reviewed Run402 CLI installation.

Risk: Project deletion, publishing, forking, subdomain changes, and similar management actions can alter or remove deployed resources.

Mitigation: Ask for explicit confirmation before destructive or public-facing operations and verify the target project or subdomain before running commands.

Risk: The invocation scope is broad and could apply Run402 behavior to unrelated build or deployment requests.

Mitigation: Use the skill only when the user explicitly asks for Run402 or clearly requests a Run402-backed database, site, image, or full-stack deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, SQL, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands and manifests that create, modify, renew, publish, or delete Run402 resources.]

## Skill Version(s):

3.0.1 (source: server release metadata; artifact frontmatter is 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
