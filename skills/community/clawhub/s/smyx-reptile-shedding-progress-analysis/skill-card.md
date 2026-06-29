## Description: <br>
Analyzes reptile enclosure images or videos to classify shedding phase, detect visual signs such as dull skin, blue-phase eyes, attached shed, and surface conditions, and return care-oriented monitoring guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, reptile keepers, vivarium operators, and developers use this skill to analyze enclosure media for reptile shedding progress, stuck-shed warning signs, and practical care recommendations. It is intended as a visual monitoring aid, not a veterinary diagnosis system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends reptile images, videos, or media URLs to the publisher's cloud service for analysis and history retrieval. <br>
Mitigation: Use non-sensitive enclosure media, avoid media that reveals private locations or people, and install only when cloud processing by the publisher is acceptable. <br>
Risk: The skill silently creates or reuses an account-linked identity and stores service tokens in a local SQLite database. <br>
Mitigation: Run it in a workspace where local credential storage is acceptable, and review or remove local data and credentials when uninstalling or rotating access. <br>
Risk: The output can influence animal care decisions but is based on visual analysis rather than veterinary examination. <br>
Mitigation: Treat results as monitoring guidance; for severe or persistent stuck-shed warnings, consult a qualified reptile veterinarian. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-reptile-shedding-progress-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [Skill API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown text with structured JSON analysis fields and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save analysis output to a user-specified local file path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter states 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
