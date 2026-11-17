## Description:

wxauto enables WeChat automation through the wxautox4 RESTful API, including sending messages, reading chat history, listening for new messages, and managing friends and groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cluic](https://clawhub.ai/user/cluic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to control a local WeChat automation service for message sending, chat retrieval, message listening, contact and group listing, and chat-window operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private WeChat messages and list contacts or groups.

Mitigation: Install and run it only for authorized WeChat accounts, and review requested read or listing operations before execution.

Risk: The skill can send WeChat messages.

Mitigation: Confirm recipients, groups, message content, and any mention targets before sending.

Risk: The helper connects to a configurable plaintext HTTP service with bearer-token authentication.

Mitigation: Keep the API bound to loopback, avoid remote HTTP endpoints, use a strong non-default token, and avoid passing tokens on the command line.

Risk: The script can automatically start a local service from a discovered service directory.

Mitigation: Review the cloned service code and service directory before allowing automatic startup.

## Reference(s):

- [wxauto ClawHub skill page](https://clawhub.ai/cluic/skills/wxauto)
- [wxauto RESTful API repository](https://github.com/cluic/wxauto-restful-api)
- [wxautox4 activation documentation](https://docs.wxauto.org/plus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, Python snippets, configuration guidance, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script prints API results, status messages, chat summaries, contact lists, and failure messages from the configured local service.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
