## Description: <br>
Generates a traceable SDLC R3 prototype document from a PRD, including task flows, page and dialog structure, ASCII wireframes, acceptance-criteria mappings, and walkthrough scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khalil](https://clawhub.ai/user/khalil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill in an SDLC requirements workflow to turn an approved PRD into a reviewable prototype specification. It focuses on requirements/prototype.md with task flows, page inventories, ASCII wireframes, AC traceability, and walkthrough scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes requirements/prototype.md as part of the SDLC workflow. <br>
Mitigation: Review the generated prototype document before relying on it for implementation or acceptance decisions. <br>
Risk: The workflow is designed to continue into using-aisdlc routing after prototype generation. <br>
Mitigation: Confirm that automatic SDLC routing is expected in the target workspace before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/khalil/zixunorg) <br>
- [Publisher profile](https://clawhub.ai/user/khalil) <br>
- [Prototype template](artifact/assets/prototype-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown file with Mermaid task flow, ASCII wireframes, traceability tables, and walkthrough scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes requirements/prototype.md after required context and PRD gates pass.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
