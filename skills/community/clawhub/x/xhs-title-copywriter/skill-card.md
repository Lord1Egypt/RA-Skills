## Description: <br>
Generates 10 Xiaohongshu title candidates from a user topic by querying RedFox trend data, analyzing viral-title patterns, and returning scores, references, and rationales. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Xiaohongshu creators, brand operators, e-commerce teams, MCNs, and content strategists use this skill to turn product, topic, or niche inputs into data-informed title options for publishing and A/B testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and sends selected Xiaohongshu topic keywords to redfox.hk. <br>
Mitigation: Use it only for explicit title-generation tasks, avoid sensitive personal or confidential prompts, and confirm the key source, scope, expiry, and revocation path before use. <br>
Risk: The skill can create local Markdown reports containing fetched topic data and external content links. <br>
Mitigation: Run it in a workspace where generated reports and referenced links are acceptable, and review generated files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/xhs-title-copywriter) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown title recommendations with links, match scores, rationales, and optional Markdown or JSON trend reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates 10 title candidates and may write keyword-specific trend data Markdown files in the workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release.version and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
