## Description:

Sage CPO is an AI chief product officer for 1-30 person startup teams that pairs with humans on user insight, MVPs, product-market fit, roadmaps, and service productization while maintaining product memory under ~/.sage/product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billzhuang6569](https://clawhub.ai/user/billzhuang6569)

### License/Terms of Use:

MIT-0

## Use Case:

Startup founders and small product teams use Sage CPO as a product strategy partner to frame customer problems, prioritize MVP and roadmap choices, evaluate product-market fit, and turn services into repeatable product systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bootstrap behavior can persistently change workspace agent-instruction files.

Mitigation: Review the target files and keep a backup or manual diff before running the bootstrap script.

Risk: Business memory in ~/.sage or sage-mirror/ can be duplicated into a project workspace.

Mitigation: Avoid storing secrets in ~/.sage, keep mirrors out of version control, and inspect generated mirrors before sharing a repository.

Risk: Product guidance may affect roadmap, pricing, and prioritization decisions when company evidence is incomplete.

Mitigation: Have a human product owner review assumptions and proposed memory updates before treating them as authoritative.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/billzhuang6569/skills/sage-cpo)
- [CPO Identity](references/cpo-identity.md)
- [CPO Product Operating System](references/cpo-product-operating-system.md)
- [CPO Scenarios](references/cpo-scenarios.md)
- [Sage DNA Protocol](references/sage-dna-protocol.md)
- [Write Routing](references/write-routing.md)
- [Review Cadence](references/review-cadence.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional shell commands and file-update recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write local product-memory updates after reviewing the skill's write-routing guidance.]

## Skill Version(s):

3.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
