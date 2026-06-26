## Description: <br>
Analyze real estate investments with conservative underwriting, financing stress tests, diligence gates, and exit planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investing-focused agents use this skill to compare real estate strategies, screen deals, underwrite rentals or value-add projects, stress financing assumptions, sequence diligence, and maintain local decision memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local investing memory may contain sensitive property, financing, or identity-adjacent details if the user chooses to save them. <br>
Mitigation: Keep lender logins, tax IDs, account numbers, full legal documents, and exact addresses out of ~/real-estate-investing/ unless the user deliberately decides otherwise; review the directory periodically. <br>
Risk: Real estate, tax, insurance, lending, and legal conclusions may be wrong or jurisdiction-specific. <br>
Mitigation: Treat the skill's output as decision support, verify assumptions with source documents and qualified professionals, and do not rely on it as licensed advice. <br>
Risk: The skill can produce shell commands to initialize local storage. <br>
Mitigation: Review commands before execution and confirm that local file permissions and storage scope match the user's intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/real-estate-investing) <br>
- [Skill homepage](https://clawic.com/skills/real-estate-investing) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with plain-language analysis, tables, formulas, and occasional bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local notes under ~/real-estate-investing/ when the user chooses recurring memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
