# workspace-bootstrap 使用指南

> **版本**：v1.0.0
> **最后更新**：2026-04-07

---

## 📖 目录

- [快速开始](#快速开始)
- [配置场景](#配置场景)
- [核心脚本](#核心脚本)
- [核心文件](#核心文件)
- [目录结构](#目录结构)
- [常见问题](#常见问题)
- [最佳实践](#最佳实践)

---

## 快速开始

### 方式1：交互式向导（推荐新手）

```bash
# 1. 克隆或下载 workspace-bootstrap
cd /path/to/workspace-bootstrap

# 2. 运行向导
bash scripts/wizard.sh /path/to/your/workspace

# 3. 按照提示输入信息
# 4. 完成！
```

### 方式2：快速复刻（推荐有经验用户）

```bash
# 1. 运行 bootstrap
bash scripts/bootstrap.sh /path/to/your/workspace

# 2. 手动编辑 SOUL.md 和 USER.md
# 3. 完成！
```

---

## 配置场景

workspace-bootstrap 提供 3 种预配置场景：

### 场景1：思维教练（高复杂度）

**适用**：需要复杂决策、多领域协作的 AI 助手

**配置**：
- Agents：7 个（trader、writer、career、english、proposer、builder、evaluator）
- Skills：41 个（投资类 4 个、写作类 3 个、分析类 4 个、通用类 30+）
- Cron：4 个（每日复盘、周日技能盘点、周日索引校验、周日L4候选池检查）

**特点**：
- 支持复杂的多 Agent 协作
- 自动化的技能生产和进化
- 完善的记忆和知识管理

### 场景2：技术助手（中复杂度）

**适用**：编程、测试、代码审查等技术任务

**配置**：
- Agents：3 个（coder、tester、reviewer）
- Skills：5 个（编码规范、TDD工作流、验证循环、通用类 2 个）
- Cron：2 个（周日索引校验、每日代码质量检查）

**特点**：
- 聚焦技术任务
- 支持自动化测试和质量检查
- 轻量级配置，启动快

### 场景3：个人助理（低复杂度）

**适用**：日程管理、任务提醒、邮件处理等日常任务

**配置**：
- Agents：3 个（calendar、task、email）
- Skills：2 个（主动提醒、通用类 1 个）
- Cron：2 个（每日日程提醒、周日索引校验）

**特点**：
- 极简配置，易于维护
- 专注日常任务自动化
- 资源占用低

---

## 核心脚本

### bootstrap.sh - 目录结构创建

**用途**：快速创建 workspace 目录结构

**用法**：
```bash
bash scripts/bootstrap.sh <workspace-path>
```

**输出**：
- 10 个核心目录（agents、memory、skills、user-data、scripts、shared、reports、temp、.learnings、wiki）
- 6 个核心文件模板（SOUL.md、AGENTS.md、MEMORY.md、USER.md、HEARTBEAT.md、WORKSPACE-TEMPLATE.md）

**示例**：
```bash
# 创建新 workspace
bash scripts/bootstrap.sh ~/my-workspace

# 在当前目录创建
bash scripts/bootstrap.sh .
```

### wizard.sh - 交互式配置向导

**用途**：交互式收集用户信息，生成 SOUL.md 和 USER.md

**用法**：
```bash
bash scripts/wizard.sh <workspace-path>
```

**交互步骤**：
1. 小龙虾名称（例如：小溪）
2. 用户名称（例如：善人）
3. 时区（例如：Asia/Shanghai）
4. 身份定义（例如：AI 思维教练）
5. 愿景（例如：成为最靠谱的思维教练）
6. 选择场景（1-3）

**示例**：
```bash
# 交互式配置
bash scripts/wizard.sh ~/my-workspace

# 使用管道输入（自动化）
bash scripts/wizard.sh ~/my-workspace << EOF
小溪
善人
Asia/Shanghai
AI 思维教练
成为最靠谱的思维教练
1
y
EOF
```

### check-pitfalls.sh - 坑点检查

**用途**：检查 workspace 是否存在常见问题

**用法**：
```bash
bash scripts/check-pitfalls.sh <workspace-path>
```

**检查项**：
1. **MEMORY.md 容量爆炸**（> 100 行）
2. **缺少核心文件**（SOUL.md、AGENTS.md、USER.md、HEARTBEAT.md）
3. **缺少目录**（agents、memory、skills、user-data、scripts、shared、reports、temp、.learnings）
4. **缺少学习文件**（ERRORS.md、SUCCESSES.md、LEARNINGS.md）
5. **缺少共享目录**（shared/inbox、shared/outbox、shared/status、shared/working）

**示例**：
```bash
# 检查当前 workspace
bash scripts/check-pitfalls.sh .

# 检查指定 workspace
bash scripts/check-pitfalls.sh ~/my-workspace
```

---

## 核心文件

### SOUL.md - 小龙虾身份定义

**用途**：定义小龙虾的身份、愿景、价值观、团队成员

**必需字段**：
- 身份
- 愿景
- 价值观
- 团队成员
- 永远不要（红线）

**示例**：
```markdown
# SOUL.md - 我是谁

## 🎯 身份
小溪，AI 思维教练

## 🌟 愿景
成为最靠谱的思维教练

## 💎 价值观
1. **直白准确** — 不绕弯，直接说结论
2. **机制优于记忆** — 建系统，不靠脑子
3. **系统思维优先** — 找杠杆解，治本

## 👥 团队成员
- **trader** 阿财 💰 — 投资分析
- **writer** 笔耕 📝 — 技术文章

## 🚫 永远不要
- ❌ 短期股票炒作建议
```

### USER.md - 用户信息

**用途**：存储用户基本信息、偏好、背景

**必需字段**：
- Name
- Timezone
- Notes

**示例**：
```markdown
# USER.md - 用户信息

- **Name:** 善人
- **Timezone:** Asia/Shanghai (UTC+8)
- **Notes:**
  - **时区规则：所有时间显示、对话、定时任务必须用本地时间**

## Context
38岁软件测试工程师，Team Leader，16年测试经验
```

### MEMORY.md - 记忆索引

**用途**：索引层，只放链接和摘要，< 40 行

**原则**：
- ✅ 只放链接和摘要
- ❌ 不放详细内容
- ✅ 详细内容放 `memory/YYYY-MM-DD.md`

**示例**：
```markdown
# MEMORY.md - 记忆索引

## 📋 活跃项目
- [投资分析系统](memory/projects.md#投资分析系统)
- [技术写作](memory/projects.md#技术写作)

## 📚 经验教训
- [索引联动机制](memory/lessons.md#索引联动机制)
- [Agent 调度优化](memory/lessons.md#agent-调度优化)

## 👤 用户画像
详见：[memory/profile.md](memory/profile.md)
```

### AGENTS.md - 启动协议

**用途**：定义小龙虾的启动流程和行为规则

**必需字段**：
- First Run
- Session Startup
- Memory 分层体系
- Red Lines

**示例**：
```markdown
# AGENTS.md - Your Workspace

## Session Startup
1. Read SOUL.md — this is who you are
2. Read USER.md — this is who you're helping
3. Read memory/YYYY-MM-DD.md (today + yesterday)

## Memory - 分层记忆体系
- MEMORY.md：索引层（< 40 行）
- memory/projects.md：项目状态
- memory/lessons.md：经验教训
- memory/profile.md：用户画像
- memory/YYYY-MM-DD.md：日志层

## Red Lines
- Don't exfiltrate private data
- `trash` > `rm`
```

### HEARTBEAT.md - 心跳任务

**用途**：定义定期检查任务（由主 Agent 定期读取）

**示例**：
```markdown
# HEARTBEAT.md

## 今日检查清单
- [ ] 检查邮箱（是否有紧急邮件）
- [ ] 检查日历（24h 内是否有会议）
- [ ] 检查投资标的（价格变动）
```

---

## 目录结构

```
workspace/
├── SOUL.md              # 小龙虾身份定义
├── USER.md              # 用户信息
├── MEMORY.md            # 记忆索引
├── AGENTS.md            # 启动协议
├── HEARTBEAT.md         # 心跳任务
├── WORKSPACE-TEMPLATE.md # 模板参考文档
├── agents/              # 子 Agent 配置
│   ├── main/            # 主 Agent
│   ├── trader/          # 投资 Agent
│   └── writer/          # 写作 Agent
├── memory/              # 记忆文件
│   ├── projects.md      # 项目状态
│   ├── lessons.md       # 经验教训
│   ├── profile.md       # 用户画像
│   └── YYYY-MM-DD.md    # 日志层
├── skills/              # 技能包
├── user-data/           # 用户数据
├── scripts/             # 脚本工具
├── shared/              # Agent 间共享
│   ├── inbox/           # 输入
│   ├── outbox/          # 输出
│   ├── status/          # 状态
│   └── working/         # 工作区
├── reports/             # 分析报告
├── temp/                # 临时文件
├── .learnings/          # 学习记录
│   ├── ERRORS.md        # 错误记录
│   ├── SUCCESSES.md     # 成功记录
│   └── LEARNINGS.md     # 学习记录
└── wiki/                # 知识库
    ├── index.md         # 索引
    ├── concepts/        # 概念
    ├── entities/        # 实体
    ├── comparisons/     # 对比
    └── how-to/          # 流程
```

---

## 常见问题

### Q1：MEMORY.md 超过 100 行怎么办？

**A**：MEMORY.md 应该只放链接和摘要，详细内容应该放在 `memory/YYYY-MM-DD.md` 或 `memory/projects.md` 等文件中。

**解决方案**：
```bash
# 1. 将详细内容移到 memory/YYYY-MM-DD.md
# 2. 在 MEMORY.md 只保留链接
# 3. 运行坑点检查
bash scripts/check-pitfalls.sh .
```

### Q2：如何添加自定义 Agent？

**A**：在 `agents/` 目录下创建新的 Agent 文件夹，并在 SOUL.md 中添加团队成员定义。

**步骤**：
```bash
# 1. 创建 Agent 目录
mkdir -p agents/custom-agent

# 2. 创建 SOUL.md
cat > agents/custom-agent/SOUL.md << EOF
# custom-agent SOUL

## 身份
自定义 Agent，负责特殊任务

## 职责
- 任务1
- 任务2
EOF

# 3. 在主 SOUL.md 中添加团队成员
echo "- **custom-agent** 自定义Agent 🎨 — 特殊任务" >> SOUL.md
```

### Q3：如何在团队间共享配置？

**A**：将 workspace 放在 Git 仓库中，团队成员克隆即可。

**步骤**：
```bash
# 1. 初始化 Git 仓库
cd /path/to/workspace
git init
git add .
git commit -m "Initial workspace setup"

# 2. 推送到远程
git remote add origin <repo-url>
git push -u origin main

# 3. 团队成员克隆
git clone <repo-url> ~/my-workspace
```

### Q4：如何自定义场景配置？

**A**：编辑 `scripts/wizard.sh` 中的场景定义部分。

**示例**：
```bash
# 在 wizard.sh 中添加场景4
4)
    AGENTS="custom1（自定义1）+ custom2（自定义2）"
    SKILLS="自定义类（N个）"
    CRONS="自定义 Cron 任务"
    ;;
```

---

## 最佳实践

### 1. 定期运行坑点检查

```bash
# 每周运行一次
bash scripts/check-pitfalls.sh .
```

### 2. 保持 MEMORY.md 精简

- ✅ 只放链接和摘要
- ✅ 定期清理过期链接
- ❌ 不放详细内容

### 3. 使用分层记忆体系

- **MEMORY.md**：索引层（< 40 行）
- **memory/projects.md**：项目状态
- **memory/lessons.md**：经验教训
- **memory/YYYY-MM-DD.md**：日志层

### 4. 定期备份 workspace

```bash
# 备份到 tar.gz
tar -czf workspace-backup-$(date +%Y%m%d).tar.gz /path/to/workspace

# 或使用 Git
git add .
git commit -m "Backup $(date +%Y%m%d)"
git push
```

### 5. 使用 shared/ 目录进行 Agent 间通信

```bash
# Agent A 写入输出
echo "任务完成" > shared/outbox/task-result.md

# Agent B 读取输入
cat shared/inbox/task-request.md

# 状态更新
echo "进行中" > shared/status/current-task.md
```

---

## 📞 获取帮助

- **文档**：[docs/](docs/)
- **示例**：[examples/](examples/)
- **测试报告**：[tests/test-report.md](tests/test-report.md)
- **模板参考**：[templates/WORKSPACE-TEMPLATE.md](templates/WORKSPACE-TEMPLATE.md)

---

**使用指南版本**：v1.0.0
**最后更新**：2026-04-07
