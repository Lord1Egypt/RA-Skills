## Description: <br>
A CLI for searching and invoking services on the UnifAI network across DeFi, token data, social media, web search, news, travel, sports, and utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yilunzhang](https://clawhub.ai/user/yilunzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use UnifAI to search for service actions, inspect exact payload schemas, and invoke UnifAI network services from a CLI. Typical workflows include DeFi operations, token and market data lookup, wallet and chain queries, social and web search, news, travel, sports, and utility tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys can enable the CLI to sign and submit real blockchain transactions. <br>
Mitigation: Keep wallet private keys unset unless actively signing, use dedicated low-balance wallets, and avoid storing keys in shared configuration or shell history. <br>
Risk: Incorrect action payloads or guessed field names can create failed, misleading, or unintended service invocations. <br>
Mitigation: Search first, inspect the returned payload schema, and manually review every payload before using transaction signing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yilunzhang/unifai) <br>
- [UnifAI SDK project homepage listed in artifact metadata](https://github.com/unifai-network/unifai-sdk-js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke external UnifAI services and, when wallet private keys are configured, sign and submit blockchain transactions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
