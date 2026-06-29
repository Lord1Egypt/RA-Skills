## Description: <br>
Sofagent FDE guides deployment experts through enterprise AI deployment discovery, workflow mapping, AI node identification, value quantification, solution design, and handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongfangxun](https://clawhub.ai/user/kongfangxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External FDE consultants, enterprise CIOs, IT leads, and engineers use this skill to structure on-site AI deployment work, translate business conversations into implementation plans, and prepare deployment, knowledge-base, audit, and handoff materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide enterprise workflow automation that touches business systems, approvals, contracts, finance, legal, security, or customer-impacting outputs. <br>
Mitigation: Require human review and approval before acting on sensitive or customer-impacting recommendations, and define checkpoint rates up to full review for high-sensitivity nodes. <br>
Risk: Deployment documents and knowledge-base outputs may include secrets, personal data, regulated data, or confidential business information. <br>
Mitigation: Redact sensitive data before generating or storing documents, restrict knowledge-base access to authorized users, and use least-privilege credentials for connected systems. <br>
Risk: The README references installing an external sofagent package and script outside the submitted artifact. <br>
Mitigation: Review the external install script, source repository, and dependency behavior before running installation commands in an enterprise environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongfangxun/skills/sofagent-fde) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown prose, checklists, tables, and occasional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces enterprise profiles, platform inventories, workflow node maps, AI-node classifications, value tables, deployment plans, knowledge-base documents, audit/checkpoint guidance, and handoff checklists.] <br>

## Skill Version(s): <br>
0.95.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
