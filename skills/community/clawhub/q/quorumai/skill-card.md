## Description: <br>
Run multi-model AI synthesis inquiries via QuorumAI. Four AI models (Claude, GPT, Gemini, Grok) compete to answer your question from specialized perspectives, get scored by an arbiter, and the best elements are synthesized into one ultimate answer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shokatma-oss](https://clawhub.ai/user/shokatma-oss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to send selected questions to QuorumAI, choose inquiry depth and academy, and present the synthesized answer, top voice, scores, and share URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected questions are sent to the external QuorumAI service and may produce a public result link. <br>
Mitigation: Avoid submitting secrets, credentials, private documents, regulated data, or sensitive personal information unless that external data flow is acceptable. <br>
Risk: The skill depends on a bearer API key for QuorumAI access. <br>
Mitigation: Store QUORUMAI_API_KEY only in the agent environment or approved secret storage and do not expose it in user-facing messages. <br>


## Reference(s): <br>
- [QuorumAI homepage](https://quorumai.io) <br>
- [QuorumAI account and API keys](https://quorumai.io/account) <br>
- [QuorumAI inquiry API endpoint](https://quorumai.io/api/v1/inquiry) <br>
- [ClawHub skill page](https://clawhub.ai/shokatma-oss/quorumai) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/shokatma-oss) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, markdown, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QUORUMAI_API_KEY and curl; sends user-selected questions to an external QuorumAI API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
