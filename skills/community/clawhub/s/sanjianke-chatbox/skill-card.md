## Description:

Guides Chatbox users through connecting to the A7W model gateway, generating importable provider settings, and troubleshooting the connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Chatbox users and developers use this skill to set up their own A7W API credentials, select supported chat models, and diagnose configuration or authentication errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill offers an API key through private contact, despite advising users not to accept or share reusable keys this way.

Mitigation: Create your own key at the provider, apply a low spending quota, and never accept or send reusable keys through private chat or WeChat.

Risk: Verification and configuration scripts may read a local A7W key and send authenticated requests to api.a7w.cn.

Mitigation: Review scripts before running them, use a limited key you control, and enter the key in Chatbox rather than sharing it through import links.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-chatbox)
- [Chatbox provider setup](https://docs.chatboxai.app/en/guides/providers)
- [Chatbox provider import configuration](https://docs.chatboxai.app/en/guides/providers/import-config)
- [A7W API documentation](https://api.a7w.cn/docs.html)
- [Configuration guide](artifact/references/configure.md)
- [Model selection guide](artifact/references/models.md)
- [Troubleshooting guide](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Configuration guidance, JSON configuration, Shell commands]

**Output Format:** [Markdown guidance, Chatbox provider JSON, and chatbox:// import link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated provider configuration and import link omit the API key; users add their own key in Chatbox.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
