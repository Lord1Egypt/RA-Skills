## Description:

Provides API-backed BaZi and Qi Men Dun Jia chart generation and interpretation through Xiaoqi Intelligent Calculation, requiring a XIAOQIZHISUAN_API_KEY credential.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colorwlof](https://clawhub.ai/user/colorwlof)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Xiaoqi Intelligent Calculation for BaZi and Qi Men Dun Jia chart generation, interpretation preparation, and full chart readings. It is suited for API-backed traditional calculation workflows where users provide birth or chart timing details and an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external API receives personal birth details, sex, and user questions.

Mitigation: Review the provider's privacy policy and terms before use, and avoid submitting sensitive details unless the user is comfortable sending them to xiaoqizhisuan.cn.

Risk: The connector uses pay-per-call billing and can spend account balance.

Mitigation: Require user confirmation for paid calls, keep the ¥2 per-session spend cap, and limit retries to the configured maximum of one retry per call.

Risk: The skill requires an API key credential for the external service.

Mitigation: Configure only the intended XIAOQIZHISUAN_API_KEY and avoid exposing the key in prompts, logs, or shared outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colorwlof/skills/skill-qimen-api)
- [Xiaoqi Intelligent Calculation homepage](https://www.xiaoqizhisuan.cn)
- [Xiaoqi API help](https://www.xiaoqizhisuan.cn/help.html)
- [API key account page](https://www.xiaoqizhisuan.cn/account.html)
- [BaZi Great Fortune example](https://www.xiaoqizhisuan.cn/examples/example_1_bazi_dayun.html)
- [Qi Men chart generation example](https://www.xiaoqizhisuan.cn/examples/example_2_qimen_paipan.html)
- [Qi Men chart webpage example](https://www.xiaoqizhisuan.cn/examples/example_3_qimen_paipan_image.html)
- [Immediate chart analysis preparation example](https://www.xiaoqizhisuan.cn/examples/example_4_qimen_jiepan.html)
- [Lifetime chart analysis preparation example](https://www.xiaoqizhisuan.cn/examples/example_5_qimen_jiepan_lifetime.html)
- [Complete immediate chart interpretation example](https://www.xiaoqizhisuan.cn/examples/example_6_qimen_full.html)
- [Complete lifetime chart interpretation example](https://www.xiaoqizhisuan.cn/examples/example_7_qimen_full_lifetime.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown instructions with JSON and shell command examples; tool calls return JSON data, HTML URLs, prompts, and text interpretations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XIAOQIZHISUAN_API_KEY; paid per-call usage requires confirmation with a ¥2 per-session spend cap.]

## Skill Version(s):

1.0.20 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
