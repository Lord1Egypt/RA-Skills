## Description: <br>
UniSkill V4 provides a minimalist agent workflow for keyword-triggered requirement clarification and heuristic multi-option debate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add requirement-clarification and lightweight decision-review behavior to agents. It is aimed at CNC quoting prompts, open-versus-closed strategy choices, and other multi-option decisions where a clarifying question or recommendation with confidence can help the user proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Keyword-based automatic activation can apply the workflow to prompts where it is not intended. <br>
Mitigation: Review trigger keywords before deployment and give the host agent or user a clear way to bypass the workflow. <br>
Risk: Heuristic scoring can produce incomplete or misleading CNC, business, or strategy recommendations. <br>
Mitigation: Treat outputs as advisory and require domain review before taking operational, purchasing, or business action. <br>
Risk: The bundled release script can add unrelated files if run from the wrong directory. <br>
Mitigation: Run release automation only in the intended project directory after reviewing staged files and excluding secrets or private artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timo2026/uniskill-v4) <br>
- [Publisher profile](https://clawhub.ai/user/timo2026) <br>
- [README](artifact/README.md) <br>
- [Full README](artifact/README_FULL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Python dataclasses and dictionaries containing clarification prompts, recommendations, scores, confidence values, and optional Markdown or code examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a clarifying question when required information is missing, or a heuristic recommendation with score and confidence when candidate options are available.] <br>

## Skill Version(s): <br>
4.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
