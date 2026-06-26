## Description: <br>
Audits changes between an installed skill and a pending ClawHub update, flagging new tool requests and risk changes before approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordo-tech](https://clawhub.ai/user/ordo-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review ClawHub skill updates before applying them, especially in environments where permission changes and update risk need lightweight triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The free audit is lightweight and may miss instruction changes or new endpoints and domains. <br>
Mitigation: Treat the verdict as triage and manually review updates that add exec, write, credentials, broad network access, or unfamiliar endpoints. <br>
Risk: The skill reads installed skill text and fetches the candidate version for comparison. <br>
Mitigation: Run it only where read and web_fetch access are acceptable, and apply updates only after reviewing the generated report. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ordo-tech/skill-diff-auditor) <br>
- [ClawHub Ops Pack](https://theagentgordo.gumroad.com/l/clawhub-ops-pack) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown audit report with verdict, new tool list, and risk profile] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free version omits full instruction diffs, endpoint/domain reporting, detailed rationale, and batch audit.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
