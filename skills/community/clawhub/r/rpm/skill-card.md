## Description: <br>
Provides RPM packaging guidance for writing and reviewing spec files, build commands, dependency declarations, macro usage, rpmlint checks, and build-system templates across RPM-based distributions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and build or release engineers use this skill to prepare, review, and validate RPM spec files and packaging workflows before running rpm, rpmbuild, mock, osc, or rpmlint commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RPM build, install, and uninstall commands can modify packages or system state if executed directly on a host. <br>
Mitigation: Review commands before execution and validate builds in a container, VM, mock build root, or other test environment. <br>
Risk: RPM packaging policies and macros can vary by distribution and change over time. <br>
Mitigation: Confirm the target distribution's current packaging policy before applying generated spec guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidongkl/rpm) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/weidongkl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with RPM spec snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
