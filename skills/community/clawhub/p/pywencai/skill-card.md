## Description: <br>
同花顺问财自然语言数据查询工具 - 使用中文自然语言查询A股、指数、基金、港美股、可转债等市场数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and AI agents use this skill to query Wencai market data with Chinese natural-language prompts and return stock, index, fund, Hong Kong or U.S. equity, futures, insurance, wealth-product, and convertible-bond results for analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Wencai cookie, which should be treated like a password. <br>
Mitigation: Keep the cookie private, avoid hardcoding it in shared notebooks or repositories, avoid printing it in logs, and rotate the Wencai session if it may have been exposed. <br>
Risk: Unpinned or changing Python dependencies can affect install safety and reproducibility. <br>
Mitigation: Install the skill in an isolated Python environment and pin reviewed dependency versions where possible. <br>


## Reference(s): <br>
- [pywencai on ClawHub](https://clawhub.ai/coderwpf/pywencai) <br>
- [PyWenCai GitHub](https://github.com/zsrl/pywencai) <br>
- [Wencai](https://www.iwencai.com/) <br>
- [BossQuant Bilibili](https://space.bilibili.com/48693330) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated usage guidance may describe pandas DataFrame or dictionary results returned by the pywencai package.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
