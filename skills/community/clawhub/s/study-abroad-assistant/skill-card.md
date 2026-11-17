## Description:

A Chinese-language assistant for U.S. STEM graduate applications that helps users assess competitiveness, plan applications, shortlist schools and professors, review essays, draft outreach, and generate reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and advising agents use this skill to organize U.S. graduate school application work for CS, EE, data, and adjacent STEM programs. It supports competitiveness assessment, timeline planning, school and professor shortlisting, essay feedback, outreach drafting, progress tracking, and decision reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applicant profile data, essay text, anonymous IDs, and API keys can be sent to the engine endpoint selected by STUDY_ENGINE_URL.

Mitigation: Use the default compliancehub.cn engine or a trusted local loopback engine only, and avoid custom endpoints for sensitive applicant data.

Risk: The skill stores anonymous IDs and registered API keys under ~/.study-abroad on the local machine.

Mitigation: Install on a single-user trusted machine and verify local file permissions and backup behavior before saving an API key.

Risk: Admissions requirements, deadlines, tuition, GRE policies, and professor availability may be stale or marked for verification.

Mitigation: Confirm program details and faculty status against official university pages before submitting applications or outreach.

Risk: Essay feedback and outreach content are drafts and could be mistaken for final application material.

Mitigation: Keep AI-draft labeling, require applicant review and finalization, and do not use the skill to guarantee admission or replace official advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wwumit/skills/study-abroad-assistant)
- [Publisher Profile](https://clawhub.ai/user/wwumit)
- [Production Study Engine](https://compliancehub.cn)
- [Skill Source Overview](artifact/SKILL.md)
- [Agent-Generated Output Examples](artifact/AGENT_GENERATED.md)
- [Professor Candidate Evidence](artifact/PROFESSOR_CANDIDATES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include AI-draft labels for essay feedback and outreach; CLI flows may use a cloud engine and local user configuration.]

## Skill Version(s):

1.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
