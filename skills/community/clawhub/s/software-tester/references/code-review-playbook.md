# 代码审查（Code Review）Playbook

> 对 diff / PR 做结构化评审：聚焦正确性、安全、性能、可读性与测试覆盖，输出带严重级的可执行意见。改编自社区高安装量技能 addyosmani/agent-skills@code-review-and-quality（30.9K）等多作者实践。本 playbook 是增量方法论（决策树 + 命令 + 坑 + 清单），非子技能内容的复制。

## 何时使用

- 用户说「review 这个 PR」「帮我看下这段代码」「cr 一下」「上线前代码评审」
- 收到 PR 需要评审意见，或提交前自检

## 评审范围决策树（先看变更类型，再定重点）

```
变更类型?
├─ 纯文档/配置        → 只查拼写/格式/是否泄露密钥(secret)，不深究逻辑
├─ Bug 修复           → 追根因：真修复还是掩盖？是否引入回归？补回归测试了吗？
├─ 新功能             → 正确性 + 边界 + 错误处理 + 安全 + 可测性 全过
├─ 重构               → 行为是否等价（无功能变更）？diff 是否纯搬移而非改写？
├─ 性能相关           → 复杂度 / N+1 / 锁 / 内存 / 缓存失效
└─ 安全相关           → 输入校验 / 鉴权 / 注入 / 越权 / 日志脱敏
```

补充铁律：**单 PR 控制在 <400 行改动**，过大难审 → 建议拆 PR 再评审。

## 命令（取 diff / 看 PR / 跑验证）

```bash
git diff main...HEAD                 # 本次分支相对主干的全部改动
git diff --stat                       # 改动文件清单与行数概览
gh pr view <n> --json files,body,additions,deletions
gh api repos/<owner>/<repo>/pulls/<n>/files --jq '.[].filename'
pre-commit run                       # 项目有 pre-commit 时跑本地 lint/format
pytest -q                            # 跑受影响测试，确认绿后再给意见
```

## 评审维度清单（逐项过，不跳项）

- **正确性**：空值 / 边界值、off-by-one、并发竞态、异步未 await、异常路径是否覆盖
- **安全**：未校验输入、SQL/命令/OS 注入、越权、硬编码密钥、日志打印 token/密码
- **性能**：循环内查询（N+1）、全表扫描、无缓存或缓存击穿、大对象不必要拷贝、锁粒度
- **可读性**：命名清晰、函数过长、魔法数、注释解释 why、重复代码是否提取
- **测试**：关键路径有测试吗？修 bug 是否带回归测试？mock 是否过度导致假绿
- **契约**：对外 API / 接口变更是否破坏兼容性？是否需迁移计划与文档同步

## 严重级判定

| 级别 | 含义 | 处置 |
|------|------|------|
| Blocker | 安全漏洞、数据丢失风险、必然崩溃 | 必须改，阻塞 merge |
| Major | 正确性或性能缺陷、缺关键测试 | 应改，merge 前解决 |
| Minor | 可读性、非关键边界遗漏 | 建议改，可不阻塞 |
| Nit | 风格、命名偏好 | 可选，勿刷屏阻塞 |

## 常见坑（评审者与作者双方）

- **评审者**：只扫风格 nitpick 忽略逻辑 bug；缺上下文妄下结论；一次塞 50 条评论压垮作者
- **作者**：把临时调试代码 / 密钥提交进 diff；巨型 PR（>400 行）难审
- **双方**：把 AI 评审当替身不复核 —— AI 也会漏安全与业务上下文，人必须最终拍板
- **遗漏链**：改了 API 没同步文档与调用方；删了字段没做兼容；改了配置没核对环境变量

## 提交评审意见模板

```
### <文件:行> · <严重级>
问题：<一句话说清>
影响：<为什么重要 / 会出什么事>
建议：<具体改法或代码片段示例>
```

## 与软件测试的关系

- 本 playbook 聚焦「评审已有代码的正确性与风险」，与 [references/unit-testing.md](unit-testing.md) / [references/e2e-testing.md](e2e-testing.md) 等「写测试」正交
- 评审发现缺测试 → 转对应 playbook 补齐，不在此写测试代码

## 相关子技能与层次边界（L2 → L3）

| 走向 | 目标 | 边界 |
|------|------|------|
| 轻量执行入口 | [skills/code-review/SKILL.md](../skills/code-review/SKILL.md) | 只给评审维度与意见模板；判定尺度与决策树回本文 |
| 缺测试 | [references/unit-testing.md](unit-testing.md)、[references/e2e-testing.md](e2e-testing.md) | 评审只标「缺测试」，补测试动作交给它们 |
| 安全类 diff | [references/security-testing.md](security-testing.md) | 越权/注入的验证手法在那里，本文只判严重级 |
| 评审后 CI 仍红 | [references/failure-triage.md](failure-triage.md) | 区分代码缺陷 / 环境问题 / flaky，避免误提缺陷 |

本文是 L2 方法论（**怎么判**），[skills/code-review/](../skills/code-review/SKILL.md) 是 L3 执行入口（**照着做**）；两者不重复，判定尺度冲突时以本文为准。

## 限制

- 不等于静态分析 / SAST；深度漏洞与架构债需配合工具与资深评审
- AI 评审缺业务上下文，最终结论由人拍板
