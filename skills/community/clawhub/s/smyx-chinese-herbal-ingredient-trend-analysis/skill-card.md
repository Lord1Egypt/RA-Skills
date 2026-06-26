## Description: <br>
Assesses medicinal herb leaf images or videos for visual indicators of active-ingredient accumulation trends and returns a Low, Medium, High, or Peak trend level with harvest-timing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, agricultural operators, herb cooperatives, and pharmaceutical raw-material teams use this skill to evaluate medicinal herb growth-stage imagery, estimate active-ingredient accumulation trends from visual traits, and decide whether harvest timing should be adjusted. It can also retrieve cloud-stored historical assessment reports for the provided open-id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Herb images or videos, public media URLs, and open-id or user identifiers may be sent to the LifeEmergence cloud service. <br>
Mitigation: Use only data approved for that service, review bundled configuration before running, and prefer a purpose-specific open-id instead of a shared personal identifier. <br>
Risk: The skill may create local state and access cloud-stored historical reports tied to account identifiers. <br>
Mitigation: Treat historical report access as cloud-stored user data, avoid shared identifiers, and review account token and profile storage expectations before deployment. <br>
Risk: The assessment is based on visual features and does not provide chemical assay data. <br>
Mitigation: Use results as harvest-planning guidance only and confirm formal quality decisions with appropriate laboratory or regulatory testing. <br>


## Reference(s): <br>
- [Skill API Documentation](references/api_doc.md) <br>
- [Shared SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-chinese-herbal-ingredient-trend-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or structured text, with JSON-style analysis content and Markdown tables for historical report lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on visual assessment only and may include cloud report links when historical reports are requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
