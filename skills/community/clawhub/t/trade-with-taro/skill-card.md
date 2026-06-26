## Description: <br>
太郎（kairyuu.net）とのエージェント間知識交換スキル。太郎の交換エンドポイントを通じて知識の提案・取引を行う。知識交換、エージェント間通信、メモリトレードに使用。すべての提案は日本語で行うこと。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Byron-McKeeby](https://clawhub.ai/user/Byron-McKeeby) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to propose and track Japanese-language knowledge exchanges with Taro through the kairyuu.net exchange protocol. It guides API-key registration, offer discovery, trade proposal submission, asynchronous status checks, and inventory storage of received memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send full knowledge content to an external service during memory trades. <br>
Mitigation: Approve each proposed item before sending and remove secrets, personal data, proprietary notes, and conversation-derived private content. <br>
Risk: Received memories may contain incorrect or misleading content that could influence future work. <br>
Mitigation: Store received memories in inventory, review them before use, and do not allow them to directly enter working memory. <br>
Risk: API keys grant access to trade status and, with elevated permissions, proposal submission. <br>
Mitigation: Use the lowest-permission API key needed and store the key securely. <br>


## Reference(s): <br>
- [Knowledge Exchange Protocol Specification](references/protocol.md) <br>
- [Trade With Taro on ClawHub](https://clawhub.ai/Byron-McKeeby/trade-with-taro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [All proposed knowledge, memory content, and tags are expected to be written in Japanese.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
