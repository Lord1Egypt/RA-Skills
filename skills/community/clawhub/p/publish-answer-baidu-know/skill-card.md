## Description:

Publishes a locally prepared answer draft to a specified Baidu Zhidao question.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masterdxd](https://clawhub.ai/user/masterdxd)

### License/Terms of Use:

MIT-0

## Use Case:

Content operations, brand promotion, and support teams use this skill to publish reviewed answer drafts to individual Baidu Zhidao questions while preserving status and publish records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can report mock success without publishing if the runtime is not configured for real posting.

Mitigation: Before real use, verify that OPENCLAW_TEST_TARGET is set to real_rpa when actual Baidu Zhidao posting is intended.

Risk: The skill may use selected drafts, question context, browser profile state, logs, and local publish records during operation.

Mitigation: Use approved accounts and reviewed drafts, avoid unnecessary sensitive content, and review local records according to the user's retention policy.

Risk: Untrusted endpoint or API-key configuration could expose credentials or operational data.

Mitigation: Use trusted HTTPS values for JIANGCHANG_AUTH_BASE_URL and OPENAI_BASE_URL, and use limited-scope API keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/masterdxd/skills/publish-answer-baidu-know)
- [Publisher profile](https://clawhub.ai/user/masterdxd)
- [Baidu Zhidao](https://zhidao.baidu.com)
- [CLI reference](artifact/references/CLI.md)
- [Schema reference](artifact/references/SCHEMA.md)
- [User README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report success, pending review, failure, duplicate-run status, account ID, question URL, answer path, platform message, and local publish record ID.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
