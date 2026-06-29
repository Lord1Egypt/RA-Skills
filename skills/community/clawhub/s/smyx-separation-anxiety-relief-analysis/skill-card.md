## Description: <br>
Analyzes pet home-camera video to identify separation-anxiety behaviors, estimate severity, and return comfort recommendations and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet owners, boarding center staff, and agents that support pet-care workflows use this skill to analyze owner-away videos, review separation-anxiety indicators, and generate intervention recommendations and historical report summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet or home video files and URLs may be sent to cloud analysis services. <br>
Mitigation: Use only footage appropriate for the provider, review privacy and retention terms, and avoid sensitive household footage unless approved. <br>
Risk: The skill may create or reuse an account identity with persistent local token storage. <br>
Mitigation: Run in a controlled environment, protect local token storage, and review account deletion and credential handling terms before deployment. <br>
Risk: Behavior analysis may be mistaken for medical diagnosis or may miss context. <br>
Mitigation: Present results as behavioral observation and intervention guidance only; consult a veterinarian or professional behaviorist for severe or persistent anxiety. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-separation-anxiety-relief-analysis) <br>
- [API interface documentation](artifact/references/api_doc.md) <br>
- [Shared SMYX analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [Skill usage demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown or JSON report text, with optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis output may include structured behavior findings, comfort recommendations, history summaries, and a report export link.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
