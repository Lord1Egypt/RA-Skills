## Description: <br>
In a plant factory, a fixed thermal imaging camera continuously captures thermal images of the plant canopy leaves at night, analyzes leaf temperature trends, and combines optional ambient CO2 data to estimate relative plant respiration intensity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and plant factory operators use this skill to analyze nighttime thermal plant canopy images or video URLs, optionally with CO2 context, and receive respiration intensity estimates, activity levels, risk prompts, environment-control suggestions, and historical cloud report listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant imagery, video URLs, and report queries are sent to the Life Emergence cloud service for analysis and history retrieval. <br>
Mitigation: Use only media that is approved for that service, and avoid sensitive facility imagery unless privacy, retention, and access terms are acceptable. <br>
Risk: The skill may create or reuse an account-linked identity and store authentication material in local workspace data such as smyx-common-claw.db or smyx-api-key.txt. <br>
Mitigation: Review workspace data handling before installation, protect or remove local token files when appropriate, and run the skill in a workspace with suitable access controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-night-respiration-rate-analysis) <br>
- [Plant Night Respiration API Documentation](artifact/references/api_doc.md) <br>
- [SMYX Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-style text with JSON-derived structured analysis, report links, shell command examples, and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include cloud report export links and historical report listings; local file inputs are constrained by the artifact documentation to supported image/video formats and a 10 MB limit.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
