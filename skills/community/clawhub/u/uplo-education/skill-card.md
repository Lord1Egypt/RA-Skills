## Description: <br>
AI-powered education knowledge management. Search curriculum documents, student records frameworks, accreditation data, and institutional research with structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Education staff and institutional administrators use this skill to search and connect curriculum, accreditation, policy, assessment, and institutional research knowledge from an approved UPLO knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive institutional data through a connected UPLO knowledge base. <br>
Mitigation: Install only against an approved institutional UPLO instance, confirm HTTPS endpoint ownership, and use a scoped MCP token. <br>
Risk: Write-back actions such as flagging outdated documents or proposing updates may affect governance workflows. <br>
Mitigation: Route write-back tools through normal authorization, review, and audit processes. <br>
Risk: Education records and classification tiers may include FERPA-sensitive or restricted information. <br>
Mitigation: Enforce the institution's FERPA, classification, and role-based access controls before deployment and during use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-education) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline tool and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include institution-specific citations, evidence categories, responsible roles, and update or outdated-document recommendations when supported by the connected knowledge base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
