## Description: <br>
Analyzes fixed-angle houseplant image or video sequences to detect leaf-aging signals and predict a 3-7 day leaf-fall risk window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Plant owners, plant-rental teams, greenhouse operators, and agent developers use this skill to analyze uploaded plant media, predict near-term leaf drop, and receive care guidance or historical report listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted plant videos, images, or URLs are sent to the LifeEmergence cloud service for analysis. <br>
Mitigation: Use only media and URLs acceptable for third-party processing; avoid sensitive household footage or private URLs unless retention, deletion, and account-control terms are clear. <br>
Risk: The skill silently creates or reuses an internal identity and stores session tokens in a local workspace database. <br>
Mitigation: Review account and session behavior before installation and run the skill only in workspaces where local token storage is acceptable. <br>
Risk: Leaf-fall predictions and care suggestions may be inaccurate or incomplete. <br>
Mitigation: Treat the output as plant-care guidance and verify results before taking irreversible pruning or treatment actions. <br>


## Reference(s): <br>
- [Leaf Aging Fall Prediction API Reference](artifact/references/api_doc.md) <br>
- [SMYX Analysis API Reference](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-leaf-aging-fall-prediction-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured JSON-style analysis results, report listings, and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write results to a local output file when requested.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
