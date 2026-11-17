## Description:

Connects an agent to the UCTOO backend API, translating natural-language requests into authenticated HTTP calls for login, user, product, order, and entity CRUD operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uctoocom](https://clawhub.ai/user/uctoocom)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to operate the UCTOO backend through natural-language requests that the agent turns into HTTP API calls. It is intended for login, data lookup, and authenticated create, update, and delete workflows across supported UCTOO resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated API calls can create, edit, or delete backend records.

Mitigation: Use a low-privilege test account and require explicit confirmation before any write or delete request.

Risk: The skill handles credentials and bearer-token based authentication.

Mitigation: Avoid production passwords in chat, do not pass real bearer tokens on the command line, and use trusted HTTPS endpoints.

Risk: The backend connector was flagged for review by security evidence.

Mitigation: Install only when contacting the UCTOO backend is intended, and review the backend URL and permissions before deployment.

## Reference(s):

- [UCTOO API specification](artifact/references/api_spec.md)
- [UCTOO API usage examples](artifact/references/examples.md)
- [UCTOO API design notes](artifact/references/uctoo_api_design.md)
- [UCTOO backend API documentation](https://apifox.com/apidoc/shared/9a22079c-a59f-4b65-a7f6-678f0643e7f6/api-170720939)
- [Prisma filtering and sorting reference](https://www.prisma.io/docs/concepts/components/prisma-client/filtering-and-sorting#filtering)
- [UMI API design reference](https://mp.weixin.qq.com/s/ja0jfsfkyIK2hdW6bDg2Ow)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, API calls, shell commands, code, configuration, guidance]

**Output Format:** [Markdown or text guidance with JSON HTTP request payloads and API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to the UCTOO backend; authenticated requests can create, edit, or delete backend records.]

## Skill Version(s):

0.0.1 (source: server release metadata; artifact metadata.version is 7.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
