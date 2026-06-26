## Description: <br>
Knowledge Base Pro helps Russian-speaking teams build and maintain an internal knowledge base with FAQ search, role-based onboarding, SOP templates, audits, gap analysis, and export workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
HR, operations, support, and leadership teams use this skill to organize recurring company knowledge, answer routine questions, guide new employees through role-specific onboarding, and identify stale or missing internal documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the package under-discloses networked indexing, query logging, exports, and record-changing actions that can affect internal company data. <br>
Mitigation: Review before installing, require corrected network declarations, and confirm local-only versus cloud behavior before using it with sensitive company knowledge. <br>
Risk: Indexing, export, delete, and update workflows can change or expose internal knowledge-base records. <br>
Mitigation: Require confirmation for delete, export, and indexing operations; enforce access controls; and review generated records before relying on them. <br>
Risk: Query logs and knowledge-base exports may contain sensitive internal information. <br>
Mitigation: Define logging retention and redaction controls before deployment, and limit credentials to the minimum integrations needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/raaipro/raai-knowledge-base-pro) <br>
- [README](README.md) <br>
- [Onboarding guide](docs/onboarding.md) <br>
- [ROI guide](docs/roi.md) <br>
- [Anti-fail guide](docs/anti-fail.md) <br>
- [Quick start example](examples/quick-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with optional JSON, YAML, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces search answers, FAQ and SOP drafts, onboarding plans, audit reports, taxonomy guidance, and export-ready knowledge-base content.] <br>

## Skill Version(s): <br>
3.5.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
