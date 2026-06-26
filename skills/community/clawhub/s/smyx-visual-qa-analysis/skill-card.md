## Description: <br>
Conducts open-ended question answering on image content using computer vision and large language model capabilities, returning natural language responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users can use this skill to ask natural language questions about provided images, request scene descriptions, inspect visual details, or summarize image content. History lookup is also described for prior visual question-answering records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review flagged under-disclosed account, token, history, remote-management, and unrelated video or health-analysis behavior beyond the advertised visual question-answering use case. <br>
Mitigation: Review before installing, confirm the provider's retention, deletion, and authorization model, and enable only behavior that is intended for the deployment. <br>
Risk: Image files, image URLs, questions, account identifiers, and history queries may be sent to remote provider APIs. <br>
Mitigation: Use only non-sensitive images and questions unless provider handling is acceptable, and avoid regulated or confidential media without a separate approval path. <br>
Risk: The skill asks for an open-id and documentation allows usernames or phone numbers for that identifier. <br>
Mitigation: Use a dedicated non-sensitive identifier, and avoid supplying a phone number unless account linking is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-visual-qa-analysis) <br>
- [Skill instructions](SKILL.md) <br>
- [API documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-like text containing questions, answers, record lists, and optional command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include links to remote report pages and may write an optional local output file when requested.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release metadata; artifact SKILL.md frontmatter lists 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
