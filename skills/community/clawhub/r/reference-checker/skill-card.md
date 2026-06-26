## Description: <br>
Helps agents exhaustively verify English and Chinese manuscript references for authenticity, metadata accuracy, traceability, duplication, source-type risks, and formatting consistency before submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxiangjian-ai](https://clawhub.ai/user/liuxiangjian-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, academic authors, editors, reviewers, and manuscript-preparation assistants use this skill to audit reference lists item by item before journal or thesis submission. It guides agents to verify English and Chinese sources through appropriate identifiers, scholarly databases, publisher pages, official sources, and manual-check paths when evidence is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reference verification can be incomplete when scholarly databases, Chinese databases, paywalled records, or official sources are inaccessible or conflicting. <br>
Mitigation: Require manual review for references marked Critical, Major, or Manual check, especially when paywalled Chinese databases are involved. <br>
Risk: An agent could overstate verification confidence when authoritative metadata is unavailable. <br>
Mitigation: Use the skill's required verification-route, match-quality, status, and confidence fields, and mark ambiguous or inaccessible cases as Manual check instead of verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuxiangjian-ai/reference-checker) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit tables with concise summaries and suggested fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes per-reference verification route, match quality, status, confidence, issue description, and continuation or completion notes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
