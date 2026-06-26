## Description: <br>
三角洲行动随机地图 + 随机装备组合生成器 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fushisanlang](https://clawhub.ai/user/fushisanlang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can run this skill to generate a random 三角洲行动 map and equipment loadout for entertainment sessions, streaming interactions, or random challenge play. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends two HTTPS requests to sanjiaozhou.fushisanlang.cn each time it runs. <br>
Mitigation: Use it only in environments where outbound access to that service is approved and expected. <br>
Risk: The generated result depends on external API availability and response shape. <br>
Mitigation: Expect the skill to return a failure JSON with an error message if either API is unavailable or changes format. <br>
Risk: The skill requires installing the PyPI requests package. <br>
Mitigation: Install dependencies from a trusted package index and apply the same dependency review used for other Python skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fushisanlang/sanjiaozhou-random) <br>
- [Random map API endpoint](https://sanjiaozhou.fushisanlang.cn/api/random_map_status) <br>
- [Random equipment API endpoint](https://sanjiaozhou.fushisanlang.cn/api/random_arm_equipment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON object with status, result text, and optional error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The result text is Chinese and depends on two external sanjiaozhou.fushisanlang.cn API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
