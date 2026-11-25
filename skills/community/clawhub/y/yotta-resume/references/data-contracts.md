# 数据契约

元简从 `0.1.2` 起随包提供机器可读契约及其 JSON Schema，`0.2.0`
起提供来源指纹状态与候选更新流水线：

- `data/industry-registry.json`：行业注册表、关键词、证据维度和扩展接口。
- `data/security-role-map.json`：6 个安全岗位族、软件研发、数据与 AI、
  业务运营、1 个 `generic` 通用岗位族与 4 个职级。
- `data/evidence-ledger.json`：简历证据账本，记录责任、动作、规模、结果和边界。
- `data/source-registry.json`：来源层级、日期、刷新周期、失效周期和许可复核状态。
- `data/source-watch-state.json`：来源内容哈希、ETag、Last-Modified 和最近检查日期。
- `data/question-bank.json`：270 项结构化原创题库；10 个岗位族各 27 项；
  合计 200 道知识题、50 条简历追问和 20 个情景案例。
- `data/dual-role-contract.json`：求职者和 HR 的数据访问、导出及受保护属性边界。
- `data/interview-session.schema.json`：本地模拟面试的会话、题目、回答和复盘结构。

`data/evidence-ledger.json` 中的唯一条目为 `EXAMPLE_ONLY` 公开示例，明确
`user_confirmed=false`、`export_allowed=false`，不属于任何真实候选人。

`data/source-watch-state.json` 只保存内容指纹，不保存网页正文。

## 行业扩展接口

新增行业时在 `industry-registry.json` 中追加对象，并保持：

- `id` 唯一且使用小写字母、数字和下划线；
- 非兜底行业提供可区分的关键词；
- 提供 `evidence_dimensions`、`question_dimensions` 和可选 `role_map_ref`；
- 全表只保留一个 `is_fallback=true` 的兜底行业；
- 扩展后运行 `contracts` 和 `doctor`。

网络安全行业有 6 个详细岗位族；软件研发、数据与 AI、业务运营各有一个
27 题岗位族，并在行业信号明确时自动映射。`generic` 只作受控回退；
行业信号冲突时仍要求确认。

## 校验

离线校验随包契约：

```bash
python scripts/yotta_resume.py contracts --format json
```

直接运行独立校验器：

```bash
python scripts/contract_validate.py --root data --format json
```

成功返回退出码 `0`；主 CLI 的契约校验失败返回 `6`。独立校验器失败返回非零退出码。
当前共校验 7 个实际契约与 8 个 JSON Schema，共 15 个文件。

面试会话由 `scripts/interview_engine.py` 额外执行实例级校验：schema 版本、
题目 ID 唯一性、当前问题、当前阶段、答案数组、题库版本漂移和原子写入。
会话不保存整份简历原文，回答中的手机号和邮箱会在落盘前打码。

## 安全边界

- 默认策略为 `deny`。
- HR 默认不能读取候选人私有证据账本、原始简历或分析报告。
- 跨角色导出必须提供字段清单并确认，默认只导出投递版简历。
- 年龄、性别、婚育、民族、宗教、籍贯、残障和照片等受保护属性不得进入评分字段。
- 来源许可未确认时只允许事实提炼、链接引用和自主改写，不复制长段原文。
- 发布包不包含来源抓取能力；运行流程只读取随包版本化来源 registry 和数据。
- 社区面经只可作练习提示，不能作为标准答案。
- 示例证据不得改写为候选人经历，也不得进入导出简历或分析报告。
