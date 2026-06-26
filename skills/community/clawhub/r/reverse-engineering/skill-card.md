## Description: <br>
Reverse engineer binaries, APIs, protocols, and workflows with evidence ladders, interface maps, and falsifiable hypotheses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate opaque binaries, APIs, protocols, file formats, devices, or workflows by bounding the target, mapping external interfaces, testing hypotheses, and documenting evidence-backed findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reverse engineering work can affect unauthorized, production, credential-bearing, or third-party systems if scope is unclear. <br>
Mitigation: Require authorized access, define boundaries before probing, and default to read-only offline copies, captures, stubs, or sandboxes when the environment or blast radius is unclear. <br>
Risk: Invasive actions such as fuzzing, patching, authentication, replay, or live-system testing can alter state or expose sensitive data. <br>
Mitigation: Ask for explicit user approval before any invasive, destructive, credential-bearing, or remote-state-changing step. <br>
Risk: Reverse engineering findings can overstate certainty when based on a single log, trace, sample, or decompiled path. <br>
Mitigation: Tag claims with evidence levels, separate observation from inference, and raise confidence only through controlled replay or independent cross-checks. <br>
Risk: Local notes and captured artifacts can include sensitive target details. <br>
Mitigation: Tell the user before creating the local workspace, store only approved workflow notes in ~/reverse-engineering/, and keep sensitive evidence in the active workspace or target-specific files. <br>


## Reference(s): <br>
- [Reverse Engineering on ClawHub](https://clawhub.ai/ivangdavila/reverse-engineering) <br>
- [Reverse Engineering homepage](https://clawic.com/skills/reverse-engineering) <br>
- [Safety boundaries](artifact/boundaries.md) <br>
- [TRACE protocol](artifact/protocol.md) <br>
- [Evidence ladder](artifact/evidence-ladder.md) <br>
- [Interface map](artifact/interface-map.md) <br>
- [Deliverable templates](artifact/deliverables.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with structured notes, tables, hypotheses, reproduction steps, and optional inline commands or code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local reverse-engineering notes only after user approval; no external data transfer by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
