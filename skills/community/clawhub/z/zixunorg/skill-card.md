## Description:

PrototypeSkill helps SDLC teams generate a traceable requirements/prototype.md prototype document from an existing PRD, including task flows, page and dialog structure, ASCII wireframes, acceptance-criteria mappings, and walkthrough scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khalil](https://clawhub.ai/user/khalil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill during the R3 prototype step of an SDLC requirements flow to turn an existing PRD into a reviewable text prototype with interaction coverage and validation scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes a requirements/prototype.md file in the resolved feature directory.

Mitigation: Confirm FEATURE_DIR and review the file diff before accepting generated prototype changes.

Risk: The generated prototype can be misleading if the PRD lacks scenarios, acceptance criteria, or validation checklist entries.

Mitigation: Use the skill only after PRD gates pass; when required PRD evidence is missing, route back to R2 rather than generating a speculative prototype.

Risk: The workflow may continue SDLC routing after prototype generation.

Mitigation: Use it in teams that intentionally rely on using-aisdlc routing, and review the ROUTER_SUMMARY before downstream work proceeds.

## Reference(s):

- [Prototype template](artifact/assets/prototype-template.md)
- [ClawHub skill page](https://clawhub.ai/khalil/skills/zixunorg)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown document with Mermaid task flows, ASCII wireframes, tables, and walkthrough steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes requirements/prototype.md only after FEATURE_DIR and PRD gates pass; may continue SDLC routing after the prototype is created.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
