## Description: <br>
Consolidates Agentic SWMM run artifacts into auditable provenance, comparison records, and local Obsidian audit notes for SWMM build, run, or QA attempts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhonghao1995](https://clawhub.ai/user/zhonghao1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and engineers use this skill after Agentic SWMM runs to create traceable audit records, compare runs, and generate Obsidian-readable notes from existing run artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit workflow may run Python code from sibling Agentic SWMM skill folders. <br>
Mitigation: Install only from a trusted Agentic SWMM repository and review sibling helper scripts before auditing sensitive projects. <br>
Risk: The direct script can copy audit notes into a default home-directory Obsidian vault. <br>
Mitigation: Use the canonical audit path or pass --no-obsidian when local note export is not intended. <br>


## Reference(s): <br>
- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/Markdown file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces experiment_provenance.json, experiment_note.md, model_diagnostics.json, and optional comparison.json in the run audit directory; Obsidian export can be disabled.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
