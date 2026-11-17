## Description:

Deploy a full-stack app to a live public URL in one command with SettleMesh login, a managed database, a runtime API key, and billing wired automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[structureintelligence](https://clawhub.ai/user/structureintelligence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to deploy a generated app, site, or API to a public SettleMesh URL with optional auth, database, runtime secrets, and billing setup. It is intended for shipping Node, Python, Go, static, Next.js, or Dockerfile-based applications without manually wiring multiple hosting and service accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a mutable global SettleMesh CLI install and authenticated deployment authority.

Mitigation: Use a reviewed pinned CLI version and narrowly scoped or short-lived credentials where possible.

Risk: Deployments may publish source-backed applications to public URLs and consume metered resources.

Mitigation: Confirm deployments and spending explicitly before execution, and avoid running the skill in directories containing unrelated private files or secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/structureintelligence/skills/ship-paid-app)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger authenticated SettleMesh CLI operations that deploy source code to a public URL and use metered resources.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
