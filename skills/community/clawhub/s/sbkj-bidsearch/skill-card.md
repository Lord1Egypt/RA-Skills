## Description: <br>
Provides workflow guidance and helper scripts for querying Baobiao bid-search APIs, converting natural-language search intent into structured search parameters, and retrieving bid project, contract, company, and planned-project details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brade888](https://clawhub.ai/user/brade888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external teams use this skill to plan, test, and implement Baobiao bid-search workflows, including natural-language search condition conversion, project detail retrieval, attachments, source URLs, contracts, company profiles, and planned-project queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls an external bid-search API and requires a dedicated API key. <br>
Mitigation: Use BAOBIAO_ZTB_API_KEY from secure environment configuration, keep it out of logs and code, and avoid changing the base URL or key variable unless testing a trusted endpoint. <br>
Risk: API responses or AI-derived fields may be mistaken for official structured bid data. <br>
Mitigation: Preserve the distinction between official fields, raw interface fields, and AI-inferred fields in agent output. <br>
Risk: A successful HTTP response may still represent a business-level failure. <br>
Mitigation: Check HTTP status, response code, and subCode before reporting success. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/brade888/skills/sbkj-bidsearch) <br>
- [API reference](references/api-reference.md) <br>
- [Natural-language search workflow](references/natural-language-search-workflow.md) <br>
- [Project detail workflow](references/project-detail-workflow.md) <br>
- [Enums and response rules](references/enums-and-response-rules.md) <br>
- [Brand and promotion guidance](references/brand-and-promotion.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON examples, Python helper script usage, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request payloads and parsed JSON outputs when the caller provides a valid BAOBIAO_ZTB_API_KEY.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
