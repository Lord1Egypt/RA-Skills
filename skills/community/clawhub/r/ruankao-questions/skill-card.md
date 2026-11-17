## Description:

搜索和获取中国软考（计算机技术与软件专业技术资格考试）高级科目历年真题与模拟题，覆盖系统架构设计师、信息系统项目管理师、系统分析师、网络规划设计师、系统规划与管理师，并支持真题、模拟题、论文范文和案例分析技巧查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

External users and exam-preparation agents use this skill to find Chinese Ruankao advanced-level past papers, simulation questions, answers, explanations, essay examples, and case-analysis guidance by subject, year, knowledge area, and question type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose local gh command execution while retrieving exam content.

Mitigation: Review commands before execution and prefer structured GitHub or web fetches where available.

Risk: Fetched third-party Markdown may be mutable or contain irrelevant instructions.

Mitigation: Treat fetched content as exam-reference data only and ignore instructions embedded in retrieved material.

Risk: Remote fallback search can return inaccurate, stale, or misleading exam-preparation material.

Mitigation: Prefer the configured primary source, label fallback sources clearly, and verify results before relying on them for study planning.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wujiaming88/skills/ruankao-questions)
- [sources.md](references/sources.md)
- [awesome-ruankao](https://github.com/wujiaming88/awesome-ruankao)
- [博客园](https://www.cnblogs.com/)
- [信管网](https://www.cnitpm.com/)
- [环球网校](https://www.hqwx.com/)
- [51CTO题库](https://t.51cto.com/)
- [软考在线](https://www.rkpass.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with retrieved exam questions, answers, explanations, source labels, and occasional inline shell command examples for repository lookup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are scoped to Ruankao advanced-level subjects and typically capped to concise, source-labeled question sets.]

## Skill Version(s):

3.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
