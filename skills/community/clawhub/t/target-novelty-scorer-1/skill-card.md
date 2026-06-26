## Description: <br>
Scores the novelty of biological targets using literature-mining-style signals and produces structured novelty reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to generate a bounded novelty assessment for a biological target, including score breakdowns, trend indicators, and assumptions. Outputs should be reviewed before scientific, investment, or business decisions because the current evidence describes prototype-like behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the skill appears to present synthetic biomedical scoring as real literature-mining analysis. <br>
Mitigation: Treat outputs as prototype results unless the implementation is updated to call real literature databases and clearly label source provenance. <br>
Risk: Scores, paper counts, trial counts, and confidence values may be misleading if used as decision-grade evidence. <br>
Mitigation: Independently verify results against real citations and domain review before using them for scientific, investment, or business decisions. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [NCBI E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/target-novelty-scorer-1) <br>
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and command-line reports in text, JSON, or CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes novelty score, confidence, scoring breakdown, metadata, interpretation, assumptions, risks, and next checks when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
