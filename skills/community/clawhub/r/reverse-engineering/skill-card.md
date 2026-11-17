## Description:

Reverse engineer binaries, APIs, protocols, and workflows with evidence ladders, interface maps, and falsifiable hypotheses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and analysts use this skill to investigate authorized opaque systems, including binaries, APIs, protocols, file formats, devices, and legacy workflows. It helps them bound the target, map interfaces, test hypotheses, and produce reusable findings without overstating certainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reverse-engineering work can exceed lawful or authorized scope if targets, samples, systems, or access boundaries are unclear.

Mitigation: Require authorized access, define the boundary before probing, and prefer read-only inspection, offline copies, captures, stubs, or sandboxes.

Risk: Invasive actions such as patching, fuzzing, credential-bearing requests, or production probing can alter systems or expose sensitive data.

Mitigation: Ask for explicit approval before invasive, destructive, authenticated, or credential-bearing steps, and pause when regulated, customer, or third-party data is involved.

Risk: Local notes, traces, decoded payloads, and reproduction snippets may contain sensitive information.

Mitigation: Store only approved engagement notes, avoid credentials and sensitive payloads in durable memory, and keep sensitive target evidence in the workspace or target-specific files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/reverse-engineering)
- [Skill homepage](https://clawic.com/skills/reverse-engineering)
- [TRACE protocol](artifact/protocol.md)
- [Evidence ladder](artifact/evidence-ladder.md)
- [Interface map](artifact/interface-map.md)
- [Deliverables](artifact/deliverables.md)
- [Safety boundaries](artifact/boundaries.md)
- [Setup guide](artifact/setup.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise findings, evidence tags, tables, and inline code or shell commands when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce target briefs, interface maps, hypothesis ledgers, reproduction notes, and remaining-unknowns lists.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
