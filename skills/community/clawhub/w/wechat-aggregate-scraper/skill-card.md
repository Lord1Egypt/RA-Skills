## Description: <br>
A WeChat data assistant that uses MaxHub APIs to search, retrieve, and analyze WeChat Channels videos, Official Account articles, comments, users, and related metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use for WeChat content monitoring and analysis, including Official Account article discovery, article details and comments, Channels video search, video details, user lookup, trend review, and comparative reporting through the MaxHub API. <br>

### Deployment Geography for Use: <br>
No deployment geography is specified in the evidence. Users should deploy only where MaxHub, WeChat data access, and local privacy, platform, and content-use rules permit the intended workflow. <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends WeChat search terms, article URLs, video identifiers, and related metadata to MaxHub/aconfig.cn using a sensitive API key. <br>
Mitigation: Use only with data the user is permitted to query, protect MAXHUB_API_KEY as a secret, and avoid exposing credential values in prompts, logs, or outputs. <br>
Risk: The evidence security summary flags protected video download and decryption workflows involving video URLs, tokens, and decode_key values. <br>
Mitigation: Avoid video download or decryption workflows unless the user has clear rights to access and decrypt the media; prefer metadata-only analysis where rights are uncertain. <br>
Risk: The security guidance notes unrelated Douyin and Xiaohongshu routing material in the artifact. <br>
Mitigation: Keep use scoped to the documented WeChat and MaxHub workflows and treat non-WeChat fallback paths as out of scope for this release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/wechat-aggregate-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/new-ironman) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Conversational answers, markdown tables, summaries, comparisons, API-result analysis, setup guidance, and curl-based request examples.] <br>
**Output Parameters:** [User search terms, WeChat article URLs, video identifiers, account identifiers, pagination cursors or offsets, analysis mode, and the required MAXHUB_API_KEY credential.] <br>
**Other Properties Related to Output:** [Outputs may include third-party API data and metadata from WeChat-related queries. The skill should keep API key values out of responses and state limitations when endpoints fail, return empty data, or require permissions.] <br>

## Skill Version(s): <br>
3.6.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
