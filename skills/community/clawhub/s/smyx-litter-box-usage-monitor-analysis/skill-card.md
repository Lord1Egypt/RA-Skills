## Description: <br>
Analyzes litter-box video or URL inputs to track cat entry and exit events, summarize usage frequency and visit duration against historical baselines, and return behavior-based urinary health alerts without providing a diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users in multi-cat homes, catteries, veterinary inpatient wards, and boarding centers use this skill to submit litter-box video for structured frequency and duration monitoring. Results support behavior monitoring and early warning workflows but do not replace veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends litter-box videos, files, or URLs to the provider cloud service for analysis. <br>
Mitigation: Use only footage you are authorized to process and review the provider's retention, deletion, and account controls before installation. <br>
Risk: The security summary reports local account state creation or reuse with stored tokens. <br>
Mitigation: Run the skill in an isolated workspace, review local account state handling, and remove stored credentials when the skill is no longer needed. <br>
Risk: The skill returns behavior-based urinary health alerts rather than medical diagnoses. <br>
Mitigation: Treat alerts as monitoring signals and route concerning results to a veterinarian for clinical interpretation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-litter-box-usage-monitor-analysis) <br>
- [Pet Litter Box Usage API Documentation](artifact/references/api_doc.md) <br>
- [Shared Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files] <br>
**Output Format:** [Structured analysis report as Markdown or JSON, with optional saved output file and report link.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [History queries return structured report lists from the provider cloud service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
