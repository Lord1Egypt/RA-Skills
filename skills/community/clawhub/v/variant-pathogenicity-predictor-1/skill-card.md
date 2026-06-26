## Description: <br>
Integrate REVEL, CADD, PolyPhen scores to predict variant pathogenicity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts can use this skill to run a local heuristic workflow that combines variant scoring signals into a pathogenicity classification and score breakdown. Results should support review, not replace clinical or diagnostic judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Variant pathogenicity output may be mistaken for medical or diagnostic advice. <br>
Mitigation: Treat results as a basic heuristic and require qualified clinical or genomic review before using them in decisions. <br>
Risk: Genomic or clinical inputs can be sensitive if placed in shared, synced, or retained workspaces. <br>
Mitigation: Run the script in a controlled local workspace and avoid identifiable genomic or clinical data unless appropriate access controls are in place. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text results and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local Python helper prints a composite score, classification, and individual score breakdown; outputs should be treated as heuristic and non-diagnostic.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
