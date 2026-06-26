## Description: <br>
Documents the MTProto protocol handling layer in Teamgram Server, including handshake, AES-IGE decryption, QuickAck, auth_key caching, and message forwarding to the session service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihang9978](https://clawhub.ai/user/zhihang9978) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this reference skill to understand, debug, or extend Teamgram Server's Telegram-compatible MTProto gateway and session flow. It is documentation-only and helps readers reason about handshake handling, encrypted message processing, QuickAck behavior, auth_key caching, and related runtime components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Protocol constants and source snippets may become stale or differ from a production Teamgram deployment. <br>
Mitigation: Verify protocol details against the upstream Teamgram repository before relying on them for production changes. <br>
Risk: The skill discusses auth_key storage and caching concepts that could affect security-sensitive server changes if misapplied. <br>
Mitigation: Treat the content as reference material and review any implementation changes through the target project's security and code review process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhihang9978/teamgram-mtproto-protocol) <br>
- [Teamgram Server repository](https://github.com/teamgram/teamgram-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown reference guidance with code snippets and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no executable actions, credentials, network access, or system privileges are requested by the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
