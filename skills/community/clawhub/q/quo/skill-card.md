## Description: <br>
Quo API integration with managed OAuth for managing calls, messages, contacts, and conversations in a business phone system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, support teams, sales teams, and developers use this skill to access a connected Quo/OpenPhone account through Maton-managed OAuth. It helps agents send SMS, list calls and conversations, manage contacts, and retrieve call recordings, transcripts, summaries, and voicemails when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive communications data, including calls, messages, recordings, transcripts, voicemails, contacts, and conversations. <br>
Mitigation: Retrieve only data the user is authorized to access, treat communications records as sensitive, and avoid exposing them in prompts, logs, screenshots, or shared terminals. <br>
Risk: Write operations can send SMS messages, create or update contacts, delete contacts, or delete OAuth connections. <br>
Mitigation: Before any write or delete request, confirm the exact account, recipient or contact ID, and intended effect with the user. <br>
Risk: MATON_API_KEY grants access to the connected Quo/OpenPhone account through Maton. <br>
Mitigation: Keep MATON_API_KEY out of prompts, logs, and screenshots, and install the skill only when Maton is trusted with the connected account. <br>


## Reference(s): <br>
- [Quo API Introduction](https://www.quo.com/docs/mdx/api-reference/introduction) <br>
- [Quo API Authentication](https://www.quo.com/docs/mdx/api-reference/authentication) <br>
- [Quo Support Center API Integration](https://support.quo.com/core-concepts/integrations/api) <br>
- [Maton](https://maton.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/quo) <br>
- [Related API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API request examples, shell commands, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Quo OAuth connection.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
