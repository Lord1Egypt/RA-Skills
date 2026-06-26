## Description: <br>
AI-powered clinical operations intelligence spanning pharmaceutical development and healthcare delivery, with unified search across clinical trials, protocols, and patient care documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RooJenkins](https://clawhub.ai/user/RooJenkins) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical, pharmaceutical, and healthcare operations teams use this skill to search organizational clinical knowledge, retrieve directives, investigate adverse event signals, prepare formulary reviews, and surface knowledge gaps across trials, protocols, SOPs, and patient care documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a remote clinical knowledge endpoint and may access sensitive PHI, PII, personnel data, and system inventory. <br>
Mitigation: Install only in an approved clinical or enterprise environment where the UPLO endpoint is trusted, HTTPS is enforced, and API tokens are least-privilege. <br>
Risk: Organization-wide exports and broad clinical searches can disclose sensitive operational or patient-related information. <br>
Mitigation: Limit, log, and review exports; respect classification tiers and restrict access to users with appropriate clearance. <br>
Risk: Clinical answers may affect safety, pharmacovigilance, regulatory, or care workflows if investigational and approved information is confused. <br>
Mitigation: Require users to verify outputs against source protocols, guidelines, regulatory status, and responsible clinical or regulatory owners before action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RooJenkins/uplo-clinical) <br>
- [UPLO](https://uplo.ai) <br>
- [UPLO schemas](https://uplo.ai/schemas) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use configured UPLO MCP tools to return clinical search results, directives, organizational context, proposals, and knowledge-gap reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
