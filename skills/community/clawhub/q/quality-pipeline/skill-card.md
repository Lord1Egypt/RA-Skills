## Description: <br>
Runs a multi-layer cross-review pipeline for formal deliverables such as papers, official documents, and reports, using separate agents to check existence, authenticity, accuracy, subject-matter quality, and final readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luaqnyin](https://clawhub.ai/user/luaqnyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and review agents use this skill to validate finished documents before delivery. It guides staged checks for missing files, placeholders, off-topic content, formatting errors, citation and data hallucinations, statistical table quality, and final pass-or-rework decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may read private or regulated target documents during quality review. <br>
Mitigation: Limit the inspected files explicitly and use automatic post-task review only in an agent environment approved for that data. <br>
Risk: Cross-agent review can still produce incorrect findings or miss hallucinated citations, data, or formatting issues. <br>
Mitigation: Require concrete issue locations, source checks for data and references, and a final human review for high-stakes documents. <br>


## Reference(s): <br>
- [Anti-Hallucination Review Handbook](references/anti-hallucination.md) <br>
- [Statistical Table Standards](references/statistical-tables.md) <br>
- [Writing Standards](references/writing-standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown review instructions, checklists, scores, issue lists, and pass-or-rework recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include per-layer pass/fail results, concrete issue locations, revision directions, and reviewer scores.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
