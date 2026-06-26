## Description: <br>
TRIZ Innovation Solution Analysis Assistant that identifies the root causes of technical problems through causal chain analysis and generates innovative solutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwt1995](https://clawhub.ai/user/wwt1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and R&D teams use this skill to structure non-sensitive technical problems through TRIZ analysis, identify root causes, and generate candidate solution concepts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TRIZ problem statements, solution summaries, and image prompts may contain sensitive invention or product information and are sent to remote services. <br>
Mitigation: Use only non-sensitive, non-regulated, non-confidential inputs unless the endpoints and data handling terms are approved by the organization. <br>
Risk: Remote TRIZ and image-generation services may fall outside an organization's approved data boundary or retention policy. <br>
Mitigation: Review and approve the referenced service endpoints, retention terms, and data policies before using the skill in commercial workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wwt1995/triz-problem-solver) <br>
- [Eureka RD](https://eureka.patsnap.com/rd-home?search-type=triz) <br>
- [System Component Analysis](references/01_system_component_analysis.md) <br>
- [Contact Relationship Analysis](references/02_component_touch_analysis.md) <br>
- [Functional Modeling](references/03_functional_modeling.md) <br>
- [Problem Description and Core Problem Selection](references/04_functional_modeling_problem_summary.md) <br>
- [Causal Chain Analysis](references/05_causal_chain_analysis.md) <br>
- [Causal Chain Problem Filtering](references/06_causal_chain_problem_summary.md) <br>
- [Solution Generation](references/07_solution.md) <br>
- [Solution Detail Generation](references/08_solution_detail.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with JSON-derived tables, solution summaries, and optional Mermaid flowcharts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; sends staged TRIZ analysis, solution, and image prompts to remote Eureka RD services.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
