## Description: <br>
Real Estate Showing Brief helps real estate agents prepare reviewable showing briefs from buyer needs, property details, and viewing schedules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Real estate agents and client-facing teams use this skill to organize buyer profiles, property-specific concerns, showing routes, on-site questions, and post-showing notes before a property visit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Showing briefs may include personal or sensitive buyer and client details. <br>
Mitigation: Use only necessary input, avoid unnecessary sensitive data, and redact client details when possible. <br>
Risk: Generated notes can be misleading if property facts are missing, stale, or incorrect. <br>
Mitigation: Review the draft before use, keep missing facts in the to-confirm section, and do not treat the output as a formal legal disclosure. <br>
Risk: The bundled helper script can inspect directories when pointed at a directory, which may surface unrelated local file information. <br>
Mitigation: Run it only on intended buyer or property input files, choose output paths carefully, and do not repurpose it as a general directory or secret scanner. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/real-estate-showing-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown brief, with optional JSON output from the local script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reviewable drafts generated from user-supplied inputs; the local script can write results to a chosen output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
