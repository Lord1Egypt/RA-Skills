## Description:

Publish, submit, and verify local skills across public skill marketplaces, directories, and registries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjsxply](https://clawhub.ai/user/zjsxply)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to prepare one local skill folder for public marketplace distribution, including readiness planning, review bundle generation, live submission where supported, and post-submit verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live publish workflows submit skill data to public marketplaces and may expose metadata or create public listings.

Mitigation: Run inspect, plan, bundle, and dry-run publish first; use --execute only after reviewing the target marketplace, payload, repository scope, and verification path.

Risk: Some workflows use unpinned or PATH-resolved command-line tools.

Mitigation: Run from a minimal sandboxed environment, pin and trust the CLI path where possible, and avoid the skills.sh path unless the skills CLI is explicitly trusted.

Risk: Marketplace submissions can ingest more than the intended single skill when repository or folder scoping is ambiguous.

Mitigation: Use a dedicated public repository or mirror for the target skill and verify scope from submit responses, status APIs, or public listing pages.

## Reference(s):

- [Market Matrix](references/market-matrix.md)
- [Publish Playbook](references/publish-playbook.md)
- [Verification Playbook](references/verification-playbook.md)
- [Recon Playbook](references/recon-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON payloads, shell commands, and generated bundle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare marketplace-specific submission bundles and dry-run payloads before any live publish action.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
