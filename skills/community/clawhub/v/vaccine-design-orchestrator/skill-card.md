## Description: <br>
Use this skill when the user wants to evaluate a new nanoparticle vaccine candidate, redesign a computational screening workflow, define gate criteria, or produce a Go/Hold/Kill decision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barrett-cryptoDNA](https://clawhub.ai/user/barrett-cryptoDNA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational biologists, and vaccine research teams use this skill to organize nanoparticle vaccine candidate screening, define gate criteria, and produce Go/Hold/Kill recommendations from structure, exposure, dynamics, and manufacturability evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill concerns vaccine design research and may produce planning recommendations that are inappropriate for direct real-world use without domain review. <br>
Mitigation: Treat outputs as planning support only and require expert scientific, medical, biosafety, and compliance review before acting on them. <br>
Risk: The artifact is instruction-only and does not execute tools, but its scientific workflow guidance may still be incomplete if user-supplied antigen, carrier, linker, host, or compute-budget details are missing. <br>
Mitigation: Use the skill's missing information checklist and decision gates to collect required inputs, document uncertainty, and stop or hold candidates when evidence is insufficient. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with structured workflow sections and decision criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning support only; real-world vaccine design decisions require expert scientific, medical, biosafety, and compliance review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
