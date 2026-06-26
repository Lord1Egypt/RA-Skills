## Description: <br>
Smart Hardware Reference is a smart hardware development reference library that provides lifecycle task catalogs, structural requirement slots, exemplar frameworks, and dependency topology for UTOS-driven planning and document generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, hardware engineers, firmware engineers, and product teams use this skill to look up smart hardware task structures and, when Universal Task OS is available, generate structured plans and documents across requirements, architecture, hardware, firmware, validation, manufacturing, operations, and project management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to automatically install and load Universal Task OS when it is not present. <br>
Mitigation: Review before installing; require UTOS to be installed through an explicit trusted flow or use the bundled material as read-only reference content. <br>
Risk: Hardware, manufacturing, and compliance outputs may depend on project-specific validation and local certification requirements. <br>
Mitigation: Have qualified hardware, firmware, manufacturing, and compliance reviewers verify outputs before using them for design, certification, or production decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangjiaocheng/smart-hardware-reference) <br>
- [Development task catalog and dependency topology](references/hardware-catalog.md) <br>
- [Structure requirements catalog](references/structure-requirements.md) <br>
- [Exemplar framework library](references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or structured text, with optional code, configuration, and shell snippets when UTOS executes a requested hardware workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only reference mode is available without UTOS; full document generation and pipeline orchestration are delegated to UTOS when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
