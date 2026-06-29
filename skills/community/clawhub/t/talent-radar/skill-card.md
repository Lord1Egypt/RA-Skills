## Description: <br>
Talent Radar analyzes Chinese-language resumes against specific job descriptions to produce match reports, gap diagnostics, and improvement suggestions for hiring or job-search workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taotao52](https://clawhub.ai/user/taotao52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External HR users, recruiters, and job seekers use the skill to compare a provided Chinese-language resume with a specific target job description, generate match or gap reports, and produce improvement suggestions. It should be used as human-reviewed decision support, not as the sole basis for hiring decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hiring-match outputs may be mistaken for automated screening decisions despite accuracy and fairness limitations. <br>
Mitigation: Use outputs only as human-reviewed assistance; confirm decisions through interviews and other evaluation methods, and avoid protected or proxy attributes. <br>
Risk: Artifact guidance contains inconsistent fairness and weighting details, including older references that discuss cultural fit or school-related signals. <br>
Mitigation: Prefer the current SKILL.md and bundled matcher behavior: culture is interview reference only and final scoring excludes school prestige, age, and gender. <br>
Risk: PDF extraction guidance includes commands for installing and running local Python libraries against user files. <br>
Mitigation: Run extraction only on intentionally provided files after reviewing the exact command and file path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/taotao52/talent-radar) <br>
- [Project README](references/README.md) <br>
- [Matching Algorithm](references/matching_algorithm.md) <br>
- [ClawHub Audit Checklist](references/clawhub_audit_checklist.md) <br>
- [PDF Extraction Guide](references/pdf_extraction_guide.md) <br>
- [Windows PDF Extraction Guide](references/windows_pdf_extraction.md) <br>
- [Skill Matrix](references/skill_matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with optional JSON structures and shell or Python command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for Chinese-language resumes and job descriptions; analysis requires both a resume and a target job or JD.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
