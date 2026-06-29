## Description: <br>
Analyzes fixed-camera reptile enclosure video to produce 24-hour circadian activity reports, including hourly motion patterns, peak activity periods, rhythm alignment, alert level, and non-medical husbandry guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External reptile keepers, breeders, husbandry teams, researchers, and app developers use this skill to analyze 24-hour or multi-day enclosure videos and compare reptile motion patterns with species-specific day, night, or crepuscular rhythms. It helps produce structured rhythm reports and non-medical recommendations for checking lighting schedules, disturbances, observation quality, and follow-up needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may upload reptile enclosure videos, public video URLs, and a user identifier to configured remote API services. <br>
Mitigation: Use only authorized footage, avoid private household or facility video unless the service is trusted, and confirm retention and sharing practices before installation. <br>
Risk: The bundled api-key/open-id flow and local token database are sensitive credential handling surfaces. <br>
Mitigation: Protect open-id and API-key values, review configuration files before use, and limit access to any local token storage. <br>
Risk: The skill provides health-adjacent husbandry guidance based on motion statistics. <br>
Mitigation: Treat outputs as non-medical rhythm analysis; persistent abnormalities or visible health signs should be reviewed by a qualified reptile veterinarian. <br>


## Reference(s): <br>
- [API Interface Documentation](artifact/references/api_doc.md) <br>
- [ClawHub Release Page](https://clawhub.ai/18072937735/smyx-reptile-circadian-activity-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown summaries and JSON-like structured analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include hourly activity arrays, peak hours, consistency scores, alert levels, report links, and non-medical recommended actions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
