## Description: <br>
Taku Think helps agents clarify ambiguous development requests, choose an appropriate planning mode, and prepare an approved design handoff before implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kkenny0](https://clawhub.ai/user/kkenny0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to clarify vague feature, product, design, or idea-stage requests before planning or building. It selects Quick, Design, Explore, or Design System mode so implementation starts only after scope, risks, success criteria, and handoff requirements are explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Planning notes may include sensitive project context if users place secrets or confidential details in design artifacts. <br>
Mitigation: Avoid putting secrets in planning notes and review generated DESIGN.md or .taku files before approving a build handoff. <br>
Risk: Implementation could proceed from an incomplete design if open questions, scope boundaries, or success criteria are not resolved. <br>
Mitigation: Use the skill's handoff contract: require an approved design or mini design, a selected approach, concrete success criteria, explicit scope boundaries, and accepted or resolved open questions. <br>
Risk: Placeholder text in a design document can leave behavior for the build step to invent. <br>
Mitigation: Run the placeholder check described by the skill and remove TBD, TODO, vague, or unresolved entries before asking for approval. <br>


## Reference(s): <br>
- [Design Document Scaffold](artifact/references/design-doc.md) <br>
- [Design System Mode](artifact/references/design-system.md) <br>
- [Taku Think on ClawHub](https://clawhub.ai/kkenny0/taku-think) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown planning guidance, mini designs, design documents, exploration notes, and handoff instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local planning documents such as DESIGN.md or .taku exploration notes when the selected mode calls for durable records.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
