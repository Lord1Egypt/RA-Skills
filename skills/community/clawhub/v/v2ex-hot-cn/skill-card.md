## Description: <br>
Provides V2EX hot-topic monitoring prompts and formatted sample topic summaries for nodes, replies, and active users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for V2EX trending-topic summaries, node-filtered topics, and discussion signals in Chinese and English community contexts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged helper returns built-in sample V2EX topics rather than confirmed live community data. <br>
Mitigation: Treat results as example summaries unless the publisher updates live fetching or clearly labels outputs as sample data; verify current topics on V2EX before relying on them. <br>
Risk: Broad triggers such as "v2" may activate the skill unintentionally. <br>
Mitigation: Narrow or disable broad triggers in environments where accidental activation would be disruptive. <br>


## Reference(s): <br>
- [V2ex Hot Cn on ClawHub](https://clawhub.ai/guohongbin-git/v2ex-hot-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown-style topic summaries or JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script supports optional limit and node filtering; bundled topic data is sample data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
