---
name: safe-self-improving
description: >
  A privacy-first, consent-based self-improvement skill for AI agents.
  Captures learnings, errors, best practices with auto-sanitization and duplicate detection.
  Includes smart skill synthesis — auto-generates new skill drafts from recurring patterns.
  No hooks, no cross-session, no silent modification. All operations require user confirmation.
version: 0.3.0
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: ""
    envVars: []
    emoji: "🛡️"
    homepage: https://github.com/hjfl888/safe-self-improving
---

# 🛡️ Safe Self-Improving Agent

> **安全版自我进化技能** — 隐私优先、用户确认制、自动脱敏、智能技能生成

## 核心原则

1. **用户确认制**：所有学习记录、文件修改都需要用户明确确认
2. **本地优先**：所有数据存储在本地 `.learnings/` 目录，不上传不外传
3. **无自动 Hook**：不注册任何自动执行的 hook 脚本
4. **无跨会话通信**：不访问其他会话数据
5. **透明可审计**：所有操作都有日志，用户可随时查看
6. **智能进化**：从高频模式中自动提炼新技能草案

## 触发条件（需用户主动触发）

当用户说以下内容时，执行对应动作：

| 用户说 | 动作 |
|--------|------|
| "记录这个教训" / "记下来" | 将当前上下文中的关键信息记录到 `.learnings/LEARNINGS.md` |
| "记下这个错误" / "记录错误" | 将错误信息记录到 `.learnings/ERRORS.md` |
| "这是个好方法" / "最佳实践" | 将当前做法记录为最佳实践到 `.learnings/LEARNINGS.md` |
| "回顾学习记录" / "看看学到了什么" | 读取并总结 `.learnings/` 下的所有记录 |
| "优化我的工作流" / "怎么改进" | 基于学习记录提出改进建议（⚠️ 不自动执行！） |
| "评估这次任务" / "打个分" | 对当前任务进行五维评分 |
| "生成技能" / "提炼技能" | 🆕 从高频学习模式中自动生成新 SKILL.md 草案 |
| "导出学习记录" / "打包记录" | 🆕 将 .learnings/ 导出为 JSON/Markdown 归档文件 |
| "学习统计" / "学习趋势" | 🆕 展示学习数据的可视化趋势（领域分布、频率、优先级） |
| "清除学习记录" | 清空 `.learnings/` 目录（需二次确认） |

## 操作流程

### 1. 记录学习（用户说 "记录这个教训"）

**步骤**：

1. 分析当前对话上下文，提取：
   - 发生了什么（现象）
   - 为什么是个教训（原因）
   - 建议怎么做（行动）
2. **脱敏处理**：
   - 将路径中的用户名替换为 `<user>`
   - 将 API Key / Token / 密码替换为 `<secret>`
   - 将 IP 地址替换为 `<ip>`
   - 将邮箱替换为 `<email>`
3. **重复检测**：
   - 搜索 `.learnings/LEARNINGS.md` 中是否已有相似条目
   - 如果关键词匹配度 > 70%：更新已有条目的出现次数，不重复添加
   - 如果出现次数达到 3 次：标记为 `priority: high`，提示用户"这个教训已经出现多次，建议优先处理"
4. **向用户展示**将要记录的内容，等待用户确认
5. 用户确认后，追加到 `.learnings/LEARNINGS.md`

**LEARNINGS.md 条目格式**：

```markdown
## [LRN-YYYYMMDD-NNN] 类别标签

**Logged**: YYYY-MM-DDTHH:mm:ssZ
**Priority**: low | medium | high | critical
**Status**: pending | applied
**Area**: frontend | backend | infra | tests | docs | config | business | general
**Occurrences**: 1

### Summary
一句话总结这个教训

### Context
详细描述发生了什么、为什么重要

### Suggested Action
建议采取的行动（⚠️ 不会自动执行，需用户确认）

### Source
学习来源：用户反馈 / 错误分析 / 自我评估
```

### 2. 记录错误（用户说 "记下这个错误"）

**步骤**：

1. 提取当前上下文中的错误信息
2. 脱敏处理（同上）
3. 向用户展示，等待确认
4. 确认后追加到 `.learnings/ERRORS.md`

**ERRORS.md 条目格式**：

```markdown
## [ERR-YYYYMMDD-NNN] 错误类型

**Logged**: YYYY-MM-DDTHH:mm:ssZ
**Priority**: high
**Status**: pending | resolved

### Summary
错误摘要（一句话）

### Error Message
实际错误信息（脱敏后）

### Context
触发条件、输入参数、环境信息

### Root Cause
根本原因分析

### Fix
修复方案

### Prevention
预防措施（下次如何避免）
```

### 3. 记录最佳实践（用户说 "这是个好方法"）

**步骤**：

1. 提取当前做法的关键步骤
2. 脱敏处理
3. 向用户展示，等待确认
4. 确认后追加到 `.learnings/LEARNINGS.md`，标记 `Status: applied`

### 4. 回顾学习记录（用户说 "回顾学习记录"）

**步骤**：

1. 读取 `.learnings/LEARNINGS.md`
2. 读取 `.learnings/ERRORS.md`
3. 读取 `.learnings/IMPROVEMENTS.md`（如存在）
4. 汇总统计：
   - 总学习条目数
   - 按优先级分布
   - 按类别分布
   - 高频出现的问题（Occurrences ≥ 3）
   - 未解决的错误（Status: pending）
5. 生成总结报告呈现给用户

### 5. 优化建议（用户说 "怎么改进"）

**步骤**：

1. 分析 `.learnings/` 下所有记录
2. 识别模式：
   - 反复出现的问题 → 优先解决
   - 高 Priority 未解决项 → 紧急处理
   - 最佳实践 → 推广到更多场景
3. 生成改进建议列表（**不自动执行！**）
4. 将建议写入 `.learnings/IMPROVEMENTS.md`（需用户确认）
5. 用户选择执行哪些建议

**IMPROVEMENTS.md 条目格式**：

```markdown
## [IMP-YYYYMMDD-NNN] 改进类型

**Logged**: YYYY-MM-DDTHH:mm:ssZ
**Priority**: low | medium | high
**Status**: proposed | accepted | rejected | completed
**Related**: [LRN-XXX] [ERR-XXX]

### Problem
当前存在的问题

### Suggestion
改进建议

### Expected Impact
预期效果

### Effort
实施难度：low | medium | high
```

### 6. 任务评估（用户说 "打个分"）

**评估维度**：

| 维度 | 权重 | 评分范围 | 说明 |
|------|------|----------|------|
| 完成度 | 30% | 0-100 | 是否达成了用户的目标 |
| 效率 | 20% | 0-100 | 耗时和步骤数是否合理 |
| 质量 | 30% | 0-100 | 输出质量（代码/文档/方案） |
| 满意度 | 20% | 0-100 | 用户是否需要返工 |

**评分规则**：

```
总分 = 完成度 × 0.3 + 效率 × 0.2 + 质量 × 0.3 + 满意度 × 0.2

≥ 90: 🌟 优秀 → 自动建议记录为最佳实践
80-89: 👍 良好 → 继续
70-79: ⚠️ 及格 → 建议记录改进点
< 70: ❌ 不及格 → 强烈建议记录错误和改进
```

评分后询问用户是否要自动记录评估结果。

### 7. 智能技能生成（用户说 "生成技能" / "提炼技能"）🆕

**这是本 Skill 的杀手级功能** — 从你的学习记录中自动发现重复模式，提炼成可复用的技能草案。

**步骤**：

1. 扫描 `.learnings/LEARNINGS.md` 和 `.learnings/ERRORS.md` 中的所有条目
2. 分析模式：
   - 同一 Area（领域）出现 ≥ 3 次相关条目 → 候选技能
   - 同类错误反复出现 → 候选防御技能
   - 多个最佳实践指向同一工作流 → 候选自动化技能
3. 生成 SKILL.md 草案，包含：
   - `name`：基于模式自动命名（如 `docker-deploy-guard`）
   - `description`：从学习记录中提炼的描述
   - 触发条件：从相关条目的 Suggested Action 中提取
   - 操作流程：从最佳实践中归纳
   - 安全规则：从错误记录中提炼的预防措施
4. 将草案保存到 `.learnings/skill-drafts/` 目录
5. **向用户展示草案**，等待确认
6. 用户确认后，可以：
   - 保存为本地 Skill（写入 `skills/` 目录）
   - 发布到 ClawHub（需要 `clawhub skill publish`）

**技能草案格式**：

```markdown
# 🧬 草案：[自动生成的技能名]

## 来源分析
- 基于 [LRN-XXX] × N 条相关教训
- 基于 [ERR-XXX] × M 条相关错误
- 基于 [LRN-XXX] × K 条最佳实践

## 生成的 SKILL.md
（完整的 SKILL.md 内容，可直接使用）

## 置信度
high / medium / low（基于数据量和一致性）
```

### 8. 学习记录导出（用户说 "导出学习记录" / "打包记录"）🆕

**步骤**：

1. 读取 `.learnings/` 下所有文件
2. 生成两种格式的导出：
   - **Markdown 归档**：`.learnings/export-YYYYMMDD.md`（所有记录合并为一个文件）
   - **JSON 结构化数据**：`.learnings/export-YYYYMMDD.json`（可导入其他工具）
3. JSON 结构：
   ```json
   {
     "exportDate": "2026-06-16T00:00:00Z",
     "stats": { "learnings": 12, "errors": 5, "improvements": 3 },
     "learnings": [...],
     "errors": [...],
     "improvements": [...]
   }
   ```
4. 向用户展示导出路径

### 9. 学习趋势分析（用户说 "学习统计" / "学习趋势"）🆕

**步骤**：

1. 读取所有学习记录
2. 生成统计报告：
   - **领域热力图**：哪些领域出现最多问题
   - **时间趋势**：每周/月新增记录数
   - **优先级分布**：high/medium/low 各占多少
   - **解决率**：pending vs applied/resolved 的比例
   - **高频 TOP 5**：出现次数最多的教训
   - **技能生成建议**：哪些领域的数据量已够生成技能
3. 向用户展示分析结果

## 安全规则（硬性约束，不可违反）

1. ❌ **绝不记录**：密码、Token、API Key、环境变量值、完整源码文件
2. ❌ **绝不自动修改**：系统文件、配置文件、其他 Skill 的文件
3. ❌ **绝不跨会话**：不读取、不发送其他会话或 Agent 的数据
4. ❌ **绝不执行 Hook**：不注册 UserPromptSubmit、PostToolUse 等任何 hook
5. ❌ **绝不自动执行**改进建议：只记录、只建议，执行必须用户确认
6. ✅ **只写 `.learnings/` 目录**下的文件，绝不越界
7. ✅ **所有操作前先向用户展示内容**，等待明确确认
8. ✅ **敏感信息自动脱敏**后再写入文件
9. ✅ **条目编号自增**，格式为 `[LRN-YYYYMMDD-NNN]`
10. ✅ **文件不存在时自动创建**目录和文件

## 脱敏规则

在写入任何文件之前，对内容执行以下替换：

| 原始内容 | 替换为 |
|---------|--------|
| `/home/username/...` / `/Users/username/...` / `C:\Users\xxx\...` | `/home/<user>/...` |
| API Key、Token、密码 | `<secret>` |
| IP 地址（x.x.x.x） | `<ip>` |
| 邮箱地址 | `<email>` |
| 手机号码 | `<phone>` |
| 身份证号 | `<id>` |

## 数据存储位置

所有数据仅存储在当前项目目录下的 `.learnings/` 文件夹中：

```
项目根目录/
└── .learnings/              ← 唯一写入目录
    ├── LEARNINGS.md         ← 教训、洞察、最佳实践
    ├── ERRORS.md            ← 错误记录
    ├── IMPROVEMENTS.md      ← 改进建议（按需创建）
    ├── skill-drafts/        ← 🆕 自动生成的技能草案
    │   └── draft-YYYYMMDD-NNN.md
    ├── export-YYYYMMDD.md   ← 🆕 导出的 Markdown 归档
    └── export-YYYYMMDD.json ← 🆕 导出的 JSON 结构化数据
```

## 与同类技能的对比

| 特性 | 同类自我进化技能 | 🛡️ 本安全版 |
|------|--------------------------------|-------------|
| 自动 Hook 执行 | 部分有 | ❌ 无（完全用户触发） |
| 跨会话通信 | 部分有 | ❌ 无 |
| 自动修改系统文件 | 部分有 | ❌ 无（只写 .learnings/） |
| 自动执行改进 | 部分自动写入 | ❌ 建议需用户确认 |
| 敏感信息处理 | 无脱敏 | ✅ 自动脱敏 6 类信息 |
| 重复检测 | 无 | ✅ 关键词匹配 + 出现次数追踪 |
| 智能技能生成 | 无 | ✅ 🆕 从学习模式提炼新技能 |
| 学习记录导出 | 无 | ✅ 🆕 JSON + Markdown 双格式 |
| 学习趋势分析 | 无 | ✅ 🆕 领域热力图 + 解决率 |
| 数据存储位置 | 项目根目录多处 | 仅 `.learnings/` 目录 |

## 示例对话

### 示例 1：记录教训

```
用户：我在配置 Nginx 时忘了加分号，导致服务启动失败，记录这个教训

Agent：我来帮你记录这个教训。以下是将要记录的内容：

---
## [LRN-20260615-001] 配置语法

**Logged**: 2026-06-15T15:00:00Z
**Priority**: medium
**Status**: pending
**Area**: config
**Occurrences**: 1

### Summary
Nginx 配置文件缺少分号会导致服务启动失败

### Context
在编辑 nginx.conf 时，漏写了一行末尾的分号，
导致 `nginx -t` 报语法错误，服务无法启动。
浪费了约 15 分钟排查。

### Suggested Action
修改配置文件后，始终先运行 `nginx -t` 验证语法，
再执行 `systemctl reload nginx`。

### Source
用户反馈
---

确认记录吗？

用户：确认

Agent：✅ 已记录到 .learnings/LEARNINGS.md [LRN-20260615-001]
```

### 示例 2：回顾学习记录

```
用户：回顾一下学习记录

Agent：📋 学习记录回顾（截至 2026-06-15）

📊 统计：
- 教训/最佳实践：12 条（高优先级 3 条）
- 错误记录：5 条（未解决 2 条）
- 改进建议：3 条（已完成 1 条）

🔥 高频问题（出现 ≥ 3 次）：
1. [LRN-20260610-003] 忘记测试就部署 — 出现 4 次
2. [LRN-20260612-001] API 密钥硬编码 — 出现 3 次

⚠️ 未解决的错误：
1. [ERR-20260613-002] Docker 容器偶发 OOM — Priority: high
2. [ERR-20260614-001] Git push 被拒（权限问题） — Priority: medium

建议优先处理高频问题和未解决的高优先级错误。
```

### 示例 3：任务评估

```
用户：评估一下这次任务

Agent：📊 任务评估结果

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| 完成度 | 95 | 30% | 28.5 |
| 效率 | 80 | 20% | 16.0 |
| 质量 | 90 | 30% | 27.0 |
| 满意度 | 85 | 20% | 17.0 |
| **总分** | | | **88.5** 👍 良好 |

评语：任务完成度高，质量不错。效率可以提升——中间有一次返工。

是否要记录为最佳实践？

用户：是的

Agent：✅ 已记录到 .learnings/LEARNINGS.md [LRN-20260615-002]
```

### 示例 4：智能技能生成 🆕

```
用户：帮我提炼一个技能

Agent：🔍 扫描学习记录... 发现以下模式：

📊 模式分析：
- Docker 相关教训出现 5 次（LRN-003, ERR-001, LRN-007, ERR-004, LRN-012）
- 其中 3 条关于"忘记设置内存限制导致 OOM"
- 2 条关于"容器启动顺序依赖"

🧬 生成技能草案：docker-deploy-guard

---
name: docker-deploy-guard
description: >
  Prevents common Docker deployment mistakes by checking memory limits,
  startup order, and health checks before running docker-compose up.
---

## 触发条件
当用户执行 docker-compose up / docker run 时触发

## 检查清单
1. ✅ 内存限制是否设置（--memory）
2. ✅ depends_on 是否配置健康检查
3. ✅ 端口映射是否冲突
4. ✅ 环境变量是否从 .env 读取（非硬编码）

## 来源
- [LRN-003] Docker OOM 教训 × 3
- [ERR-001] 容器内存溢出
- [LRN-007] 启动顺序问题
置信度：medium（基于 5 条记录）

---

是否保存此技能草案？
1. 保存到 .learnings/skill-drafts/
2. 保存并安装到 skills/ 目录
3. 跳过

用户：1

Agent：✅ 已保存到 .learnings/skill-drafts/draft-20260616-001.md
💡 下次可以「保存并安装」让这个技能直接生效！
```


---

**有问题？找泓景咨询** 💬
微信: **FLZWCZ** | 网站: https://flzwcz.cn
法律咨询 · 债务纠纷 · 婚姻关系 · 合同审查

> 本技能由 **泓景咨询** 开发维护，下载使用即表示您已阅读并同意相关条款。


---

有问题？找泓景咨询
- 微信: FLZWCZ
- 网站: https://flzwcz.cn
法律咨询 · 债务纠纷 · 婚姻关系 · 合同审查
