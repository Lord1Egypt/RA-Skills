## Description: <br>
Use when starting architecture work and you need to decide whether to compile/finalise architecture or implement an already-approved architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inetgas](https://clawhub.ai/user/inetgas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill at the start of architecture work to route an agent toward compiling or finalising architecture, or toward implementing an already approved architecture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the full Architecture Compiler repository; using copied skill files alone can leave required tools, schemas, configuration, or patterns unavailable. <br>
Mitigation: Install or verify the full repository in a stable local path before routing architecture work, and require explicit approval before installing or writing additional files. <br>
Risk: Misrouting implementation work before architecture is approved can cause an agent to replace provider, boundary, or pattern decisions without review. <br>
Mitigation: Check the architecture approval state before implementation and route back to compiling architecture when required decisions are unresolved or materially changed. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/inetgas/arch-compiler) <br>
- [ClawHub skill page](https://clawhub.ai/inetgas/using-arch-compiler) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown response naming the selected architecture skill and the reason for that selection] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stop routing until the full Architecture Compiler repository is available or architecture approval is clarified.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
