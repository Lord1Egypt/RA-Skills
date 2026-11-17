## Description:

Manages West.cn DNS records by adding, modifying, and deleting A, CNAME, MX, TXT, and AAAA entries through the West.cn API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misskivin](https://clawhub.ai/user/misskivin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DNS operators use this skill to manage live West.cn domain records from an agent workflow. It is intended for adding, updating, or deleting DNS records when the operator supplies West.cn API credentials and target record details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete live DNS records using sensitive API credentials.

Mitigation: Use scoped DNS API credentials where supported, confirm every modify or delete action against the intended domain and record, and record current DNS values before changes so they can be rolled back.

Risk: Credentials supplied to the skill could be exposed through prompts, logs, or mishandled runtime inputs.

Mitigation: Keep West.cn usernames and API passwords out of prompts and logs, and pass them only through the platform's intended secret or configuration path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/misskivin/skills/west-dns-manager)

## Skill Output:

**Output Type(s):** [JSON, API calls]

**Output Format:** [JSON object with success, message, data, and error fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires West.cn username and API password inputs; modify and delete actions can change live DNS records.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
