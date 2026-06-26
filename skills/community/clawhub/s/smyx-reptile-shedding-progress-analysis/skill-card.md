## Description: <br>
Analyzes full-body reptile images or video to classify shedding phase, identify stuck-shed risk signals, and produce care recommendations for keepers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to assess reptile shedding progress from enclosure camera media, review structured risk signals, and generate keeper-facing care guidance and history reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send reptile images, videos, remote media URLs, and a username, phone number, or open-id to configured LifeEmergence services. <br>
Mitigation: Install only when external media processing is acceptable, use a dedicated identifier where possible, and avoid using the skill in workspaces containing sensitive media or credentials. <br>
Risk: Cloud report history and local token caching may extend exposure of account identity and analysis records beyond the immediate reptile image analysis task. <br>
Mitigation: Use the minimum account identifier needed for the workflow and review workspace storage and cloud-history expectations before deployment. <br>
Risk: Visual care guidance could be mistaken for veterinary diagnosis or treatment advice. <br>
Mitigation: Treat outputs as visual shedding-stage assessments only, preserve the documented disclaimers, and contact a reptile veterinarian for persistent Level 4 stuck-shed warnings or high-risk eye, toe, or tail-tip involvement. <br>


## Reference(s): <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-reptile-shedding-progress-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON report text, with optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include shedding phase, high-risk retained-shed zones, recommended care actions, disclaimers, and history/report links when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
