## Description: <br>
Evidence-first research workflow for evidence discovery, source verification, and citation grounding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheepxux](https://clawhub.ai/user/sheepxux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research teams use this skill to gather, verify, classify, and organize evidence before writing paper outlines, related work, experiment plans, abstracts, or draft sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and URLs may be sent to public services during evidence discovery. <br>
Mitigation: Avoid confidential project names, private research topics, private URLs, and sensitive unpublished details unless external disclosure is acceptable. <br>
Risk: The skill can read local source files or result directories that the user points it at. <br>
Mitigation: Provide only scoped project paths and review selected files or directories before running evidence ingestion workflows. <br>
Risk: Research outputs can become misleading if unverified notes are treated as final evidence. <br>
Mitigation: Keep verified facts, project evidence, inference, and unverified items separate, and review claim maps before using them in public writing. <br>


## Reference(s): <br>
- [Sopaper Evidence ClawHub Listing](https://clawhub.ai/sheepxux/sopaper-evidence) <br>
- [Evidence Schema](references/evidence-schema.md) <br>
- [Source Priority](references/source-priority.md) <br>
- [Input Schemas](references/input-schemas.md) <br>
- [Prior Work Search Playbook](references/prior-work-search-playbook.md) <br>
- [Claim Audit Rules](references/claim-audit-rules.md) <br>
- [Evidence Gap Triage](references/evidence-gap-triage.md) <br>
- [Benchmark Baseline Checklist](references/benchmark-baseline-checklist.md) <br>
- [OpenClaw Evidence Playbook](references/openclaw-evidence-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, CSV, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Evidence briefs, source notes, claim-to-evidence maps, gap reports, fairness reviews, and draft-safe writing guidance.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
