## Description: <br>
Official VeriClaw helps operators verify AI claims against observable evidence, identify missing proof, choose corrective action, and re-check completion before accepting generated work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheygoodbai](https://clawhub.ai/user/sheygoodbai) <br>

### License/Terms of Use: <br>
LicenseRef-VeriClaw-Source-Available-1.1 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill as an evidence-first checklist for hallucination correction, fake-completion diagnosis, output verification, and done-gate review in OpenClaw workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the checklist outcome as proof by itself. <br>
Mitigation: Require supporting files, logs, links, tests, screenshots, or other observable evidence before accepting a claim as complete. <br>
Risk: A public note could expose private task details. <br>
Mitigation: Keep public feedback factual and omit confidential prompts, files, customer data, and internal incident details. <br>
Risk: Reuse or modification may be subject to separate license terms. <br>
Mitigation: Review the listed license terms before commercial reuse, redistribution, or publishing modified copies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sheygoodbai/vericlaw) <br>
- [OpenClaw companion plugin page](https://clawhub.ai/plugins/vericlaw) <br>
- [Public product overview](https://sheygoodbai.github.io/vericlaw/) <br>
- [Download page](https://sheygoodbai.github.io/vericlaw/download/) <br>
- [correction-loop.txt](references/correction-loop.txt) <br>
- [review-template.txt](references/review-template.txt) <br>
- [route-map.txt](references/route-map.txt) <br>
- [search-intents.txt](references/search-intents.txt) <br>
- [symptom-map.txt](references/symptom-map.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown checklist and concise review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces claim, evidence, missing-proof, failure-mode, corrective-action, and done-gate review structure.] <br>

## Skill Version(s): <br>
0.1.27 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
