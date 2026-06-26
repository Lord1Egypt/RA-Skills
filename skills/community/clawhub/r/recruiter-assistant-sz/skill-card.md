## Description: <br>
A professional recruitment workflow assistant that evaluates resumes against dynamic requirements and AI proficiency, provides critical pros and cons analysis, and performs Shenzhen-specific market salary benchmarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gakkiismywife](https://clawhub.ai/user/gakkiismywife) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Recruiters and hiring teams use this skill to screen technical resumes, benchmark salary expectations for Shenzhen roles, generate follow-up interview questions, and summarize interview notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the skill processes untrusted resume files through unsafe shell commands. <br>
Mitigation: Run the scripts only in an isolated or trusted environment, review commands before execution, and avoid batch-processing resumes with attacker-controlled filenames. <br>
Risk: The security review reports under-scoped instructions for sharing candidate data. <br>
Mitigation: Require explicit human review before saving candidate reports or sending candidate summaries to HR. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gakkiismywife/recruiter-assistant-sz) <br>
- [Publisher profile](https://clawhub.ai/user/gakkiismywife) <br>
- [Stricter Hiring Criteria (Shenzhen 2026)](references/hiring-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and console text with screening prompts, candidate analysis, interview questions, and report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Resume screening can include candidate scores, pros and cons, hire recommendations, salary benchmark notes, and HR summary guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
