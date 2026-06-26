## Description: <br>
仅适用于北京市企业职工基本养老保险退休金测算。支持依据北京政策参数计算基础养老金、个人账户养老金、过渡性养老金，并对未退休用户做未来缴费策略优化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[park-william](https://clawhub.ai/user/park-william) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect Beijing enterprise employee pension inputs, parse contribution records, calculate pension components, and compare future contribution strategies. It is scoped to Beijing enterprise employee basic pension rules, including flexible employment users under that pension framework. <br>

### Deployment Geography for Use: <br>
China (Beijing pension policy context) <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive pension, employment, and contribution records in local files. <br>
Mitigation: Provide only files intended for calculation, keep processing local, and remove generated temporary JSON or Markdown outputs after use. <br>
Risk: Pension policy parameters can become outdated or differ from the user's exact eligibility context. <br>
Mitigation: Verify updated policy parameters against official Beijing or national sources before relying on a calculation. <br>
Risk: OCR or table ingestion can misread contribution records and produce incorrect pension estimates. <br>
Mitigation: Review low-confidence fields and confirmation forms before running final calculations or using strategy recommendations. <br>
Risk: Running local scripts with broader permissions than needed could expose personal records or generated outputs. <br>
Mitigation: Run without elevated privileges and store input and output files only in controlled local directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/park-william/retirecalc-beijing) <br>
- [Beijing pension policy links](references/policy-links.md) <br>
- [Beijing Basic Pension Insurance Regulation](https://www.beijing.gov.cn/gongkai/zfxxgk/zc/gz/202112/t20211216_2562734.html) <br>
- [Beijing implementation notice for Basic Pension Insurance Regulation](https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/200804/t20080414_567067.html) <br>
- [Beijing 2025 social insurance treatment parameters](https://rsj.beijing.gov.cn/xxgk/2024zcwj/202511/t20251107_4265291.html) <br>
- [National gradual retirement age decision](https://www.gov.cn/yaowen/liebiao/202409/content_6974294.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, plus local JSON calculation outputs and Markdown confirmation forms.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local input files and writes generated JSON or Markdown outputs to user-selected paths or temporary working directories.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
